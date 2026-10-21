#!/usr/bin/env python3
"""Check local links, metadata, citation exports and preserved manuscript bytes.

This is a static implementation check, not a search-engine indexing test.
"""
from __future__ import annotations

import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data/publications.json").read_text())
BASE = DATA["base_url"].rstrip("/")


class Page(HTMLParser):
    def __init__(self, path: Path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.links = []
        self.ids = set()
        self.duplicate_ids = []
        self.meta = {}
        self.meta_values = {}
        self.canonical = []
        self.stylesheets = []
        self.h1_count = 0
        self.schema = []
        self.script_type = None
        self.script_text = ""
        self.language = None
        self.text = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if "id" in attr:
            if attr["id"] in self.ids:
                self.duplicate_ids.append(attr["id"])
            self.ids.add(attr["id"])
        if tag == "html":
            self.language = attr.get("lang")
        if tag == "h1":
            self.h1_count += 1
        if tag == "meta" and "name" in attr:
            self.meta[attr["name"]] = attr.get("content", "")
            self.meta_values.setdefault(attr["name"], []).append(attr.get("content", ""))
        if tag == "link" and attr.get("rel") == "canonical":
            self.canonical.append(attr.get("href"))
        if tag == "a" and "href" in attr:
            self.links.append(attr["href"])
        if tag == "link" and attr.get("rel") in ("stylesheet", "icon"):
            self.links.append(attr["href"])
        if tag == "link" and attr.get("rel") == "stylesheet":
            self.stylesheets.append(attr["href"])
        if tag == "script":
            self.script_type = attr.get("type")
            self.script_text = ""

    def handle_endtag(self, tag):
        if tag == "script" and self.script_type == "application/ld+json":
            self.schema.append(json.loads(self.script_text))
            self.script_type = None

    def handle_data(self, text):
        if self.script_type:
            self.script_text += text
        else:
            self.text.append(text)


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def local_target(url, from_file):
    parts = urlsplit(url)
    if parts.netloc and parts.netloc != urlsplit(BASE).netloc:
        return None
    if parts.scheme not in ("", "http", "https"):
        return None
    url_path = unquote(parts.path)
    if url_path.startswith("/"):
        target = ROOT / url_path.lstrip("/")
    elif url_path:
        target = from_file.parent / url_path
    else:
        target = from_file
    if target.is_dir():
        target = target / "index.html"
    return target.resolve(), unquote(parts.fragment)


def main():
    pages = {p.resolve(): Page(p) for p in ROOT.rglob("*.html")}
    verification = DATA.get("google_site_verification")
    if verification:
        check(pages[(ROOT / "index.html").resolve()].meta.get("google-site-verification") == verification,
              "Search Console ownership tag missing or altered")
    link_count = 0
    style_revision = hashlib.sha256((ROOT / "assets/style.css").read_bytes()).hexdigest()[:12]
    for path, page in pages.items():
        label = path.relative_to(ROOT)
        check(page.stylesheets == ["/assets/style.css?v=" + style_revision], f"{label}: stale stylesheet reference")
        check(page.language == "en", f"{label}: missing language")
        check(page.h1_count == 1, f"{label}: expected exactly one h1")
        check(not page.duplicate_ids, f"{label}: duplicate ids {page.duplicate_ids}")
        check("width=device-width" in page.meta.get("viewport", ""), f"{label}: viewport missing")
        check(bool(page.meta.get("description")), f"{label}: missing description")
        check(len(page.canonical) == 1 and page.canonical[0].startswith(BASE + "/"), f"{label}: canonical invalid")
        check("main" in page.ids, f"{label}: skip destination missing")
        for url in page.links:
            result = local_target(url, path)
            if result is None:
                continue
            target, fragment = result
            check(target.is_relative_to(ROOT), f"{label}: link escapes site: {url}")
            check(target.is_file(), f"{label}: missing target: {url}")
            if fragment and target.suffix == ".html":
                check(fragment in pages[target].ids, f"{label}: missing fragment: {url}")
            link_count += 1

    for paper in DATA["papers"]:
        directory = ROOT / "publications" / paper["slug"]
        page = pages[(directory / "index.html").resolve()]
        url = BASE + "/publications/" + paper["slug"] + "/"
        check(page.canonical == [url], f"{paper['slug']}: canonical does not match landing page")
        check("noindex" not in page.meta.get("robots", ""), f"{paper['slug']}: indexing blocked")
        pdf = directory / paper["pdf_filename"]
        pdf_bytes = pdf.read_bytes()
        check(pdf_bytes.startswith(b"%PDF-"), f"{pdf.name}: invalid signature")
        check(len(pdf_bytes) == paper["pdf_bytes"], f"{pdf.name}: size changed")
        check(hashlib.sha256(pdf_bytes).hexdigest() == paper["pdf_sha256"], f"{pdf.name}: PDF bytes changed")
        check(page.meta.get("citation_title") == paper["title"], f"{paper['slug']}: incorrect citation title")
        check(page.meta.get("citation_doi") == paper["doi"], f"{paper['slug']}: incorrect DOI")
        check(page.meta.get("citation_publication_date") == paper["publication_date"].replace("-", "/"), f"{paper['slug']}: incorrect publication date")
        check(page.meta.get("citation_pdf_url") == url + paper["pdf_filename"], f"{paper['slug']}: invalid PDF URL")
        check(page.meta.get("citation_abstract_html_url") == url, f"{paper['slug']}: invalid abstract URL")
        check(page.meta.get("DC.issued") == paper["publication_date"], f"{paper['slug']}: incorrect issued date")
        check(page.meta.get("DC.publisher") == paper["publisher"], f"{paper['slug']}: incorrect publisher")
        authors = paper["authors"]
        check(page.meta_values.get("citation_author", []) == authors, f"{paper['slug']}: author metadata incorrect")
        check(page.meta_values.get("DC.creator", []) == authors, f"{paper['slug']}: Dublin Core authors incorrect")
        visible_text = " ".join(" ".join(page.text).split())
        check(paper["abstract"] in visible_text, f"{paper['slug']}: exact abstract missing")
        check(paper["provenance"] in visible_text, f"{paper['slug']}: exact disclosure missing")
        if paper["credit_role"] == "author":
            check(bool(authors), "Authored papers require verified author names")
            for name in authors:
                check(name in visible_text, "Verified author not visible")
            check(paper["provenance_summary"] in visible_text, "Joint paper AI-provenance summary missing")
            check(f"Unmodified arXiv v{paper['version']} PDF" in visible_text, "Joint paper source notice missing")
            check(paper["record_url"] in page.links, "arXiv record link missing")
            check("Andreas Thom" in visible_text, "Second author's contribution is not identified")
        else:
            check(not authors, "Contact-only manuscripts must not have scientific author metadata")
            check(paper["contribution"] in visible_text, f"{paper['slug']}: contribution statement missing")
            check("Manuscript contact: " + paper["contact_name"] in visible_text, "Contact role not visible beside title")
            check("original deposited PDF is unchanged" in visible_text, f"{paper['slug']}: original PDF notice missing")
            check("repository metadata differs from the scientific authorship" in visible_text, "Source citation discrepancy not explained")
            check("author correction" not in visible_text, "Stale authorship correction retained")
            check(page.meta.get("DC.contributor") == paper["contact_name"], "Contact metadata missing")
        article = page.schema[0]
        check(article["@type"] == "ScholarlyArticle", "Article schema type incorrect")
        check(article["abstract"] == paper["abstract"], "Schema abstract mismatch")
        check(article["encoding"]["contentUrl"] == page.meta["citation_pdf_url"], "Schema PDF mismatch")
        check(article["identifier"]["value"] == paper["doi"], "Schema DOI mismatch")
        schema_authors = article.get("author", [])
        check([a["name"] for a in schema_authors] == authors, "Schema authors incorrect")
        check(article["license"] == paper["license_url"], "Schema license incorrect")
        if paper["credit_role"] == "author":
            check(paper["provenance"] in article["creditText"], "Joint paper provenance missing from schema")
        else:
            check("author" not in article, "Contact-only manuscript has a schema author")
            check(article["contributor"]["name"] == paper["contact_name"], "Contributor name incorrect")
            check(paper["contribution"] in article["creditText"], "Schema contribution statement missing")
        relation = paper.get("companion")
        if relation:
            companion = next(p for p in DATA["papers"] if p["slug"] == relation["slug"])
            check("/publications/" + companion["slug"] + "/" in page.links, "Companion link missing")
            if relation.get("cites"):
                check(article["citation"]["@id"] == "https://doi.org/" + companion["doi"], "Companion citation incorrect")
            else:
                check("citation" not in article, "Companion relationship incorrectly claims a citation")
        bib = (directory / "citation.bib").read_bytes()
        ris = (directory / "citation.ris").read_bytes()
        check(hashlib.sha256(bib).hexdigest() == paper["bib_sha256"], "BibTeX export altered")
        check(hashlib.sha256(ris).hexdigest() == paper["ris_sha256"], "RIS export altered")
        check(paper["doi"].encode() in bib, "DOI missing from BibTeX")
        check(paper["doi"].lower() in ris.decode().lower(), "DOI missing from RIS")
        check(b"\\r\\n" not in ris, "RIS has escaped transport separators")
        check(re.search(rb"^TY  - \w+\r?\n", ris) is not None, "RIS record start invalid")
        check(ris.rstrip().endswith(b"ER  -"), "RIS record end invalid")

    sitemap = ET.parse(ROOT / "sitemap.xml")
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [element.text for element in sitemap.findall("s:url/s:loc", namespace)]
    research = DATA.get("selected_research", [])
    for work in research:
        path = "/" + work.get("collection", "research") + "/" + work["slug"] + "/"
        directory = ROOT / path.lstrip("/")
        page = pages[(directory / "index.html").resolve()]
        text = " ".join(" ".join(page.text).split())
        article = page.schema[0]
        check(page.canonical == [BASE + path], "Research canonical incorrect")
        check(page.meta.get("citation_title") == work["title"], "Research title metadata incorrect")
        check(page.meta.get("citation_pdf_url") == BASE + path + work["pdf_filename"], "Research PDF metadata incorrect")
        check(page.meta.get("citation_abstract_html_url") == BASE + path, "Research abstract URL incorrect")
        check(page.meta.get("citation_publication_date") == work["publication_date"].replace("-", "/"), "Research date incorrect")
        check("noindex" not in page.meta.get("robots", ""), "Research page indexing blocked")
        check(work["authors"] == [] and work["credit_role"] == "coordinator", "Research coordination role incorrect")
        check(not page.meta_values.get("citation_author") and not page.meta_values.get("DC.creator"), "Coordinator misrepresented as scientific author")
        check(page.meta.get("DC.contributor") == work["contributor_name"], "Research contributor metadata incorrect")
        check("author" not in article, "Research article invents an author")
        check(article["contributor"]["name"] == work["contributor_name"], "Research schema contributor incorrect")
        check(article["encoding"]["contentUrl"] == page.meta["citation_pdf_url"], "Research schema PDF incorrect")
        check(article["identifier"] == {"@type": "PropertyValue", "propertyID": "SHA-256", "value": work["pdf_sha256"]}, "Research integrity identifier incorrect")
        check(work["abstract"] == article["abstract"] and work["abstract"] in text, "Research abstract altered")
        check(work["provenance"] in text and work["contribution"] in text, "Research provenance or role missing")
        check(work["verification_status"] in text, "Research verification scope missing")
        check(article["isBasedOn"]["url"] == work["based_on"]["url"], "Inherited OpenAI source incorrect")
        check("license" not in article, "Research page must not expand the inherited license scope")
        if not work.get("doi"):
            check("citation_doi" not in page.meta, "Research page invents an unissued DOI")
        for asset in work["assets"]:
            file = directory / asset["filename"]
            body = file.read_bytes()
            check(len(body) == asset["bytes"] and hashlib.sha256(body).hexdigest() == asset["sha256"], f"Release asset altered: {file.name}")
        pdf = (directory / work["pdf_filename"]).read_bytes()
        check(pdf.startswith(b"%PDF-") and hashlib.sha256(pdf).hexdigest() == work["pdf_sha256"], "Latest research PDF altered")
        bib = (directory / "citation.bib").read_text()
        ris = (directory / "citation.ris").read_text()
        check(not re.search(r"^\s*(author|editor)\s*=", bib, re.M | re.I), "Research citation invents scientific authorship")
        check(not re.search(r"^A[U1-4]  -", ris, re.M), "Research RIS invents scientific authorship")
        check(work["version_pdf_url"] in bib and work["version_pdf_url"] in ris, "Research citations lack the fixed version URL")
        check(work["version_pdf_url"] in page.links, "Versioned PDF link missing")
        with zipfile.ZipFile(directory / work["source_filename"]) as archive:
            check(archive.testzip() is None, "Source ZIP CRC failed")
            check(len(archive.namelist()) == 22, "Delivered source archive file count changed")
            for name in archive.namelist():
                check(not Path(name).is_absolute() and ".." not in Path(name).parts, "Unsafe source ZIP member")
            abstract_source = archive.read("sections/abstract.tex").decode()
            abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", abstract_source, re.S).group(1)
            check(" ".join(abstract.split()) == work["abstract"], "Landing abstract differs from delivered source")
            for filename in ("references.bib", "LICENSE", "NOTICE.txt"):
                check(archive.read(filename) == (directory / filename).read_bytes(), f"Preserved source notice or bibliography changed: {filename}")
            for appendix in ("analytic", "domains", "interpolation", "stein-proof"):
                check("sections/" + appendix + ".tex" in archive.namelist(), "Proof appendix missing")
        with zipfile.ZipFile(directory / "release_bundle.zip") as archive:
            check(archive.testzip() is None, "Release bundle CRC failed")
            for name in archive.namelist():
                check(archive.read(name) == (directory / Path(name).name).read_bytes(), "Release bundle payload differs from downloads")
        manifest = json.loads((directory / "release-manifest.json").read_text())
        for item in manifest["payload_files"]:
            check(hashlib.sha256((directory / item["filename"]).read_bytes()).hexdigest() == item["sha256"], "Release manifest hash mismatch")
        check("{{" not in (directory / "index.html").read_text(), "Unfilled research template")
        check("explanation" in page.ids and "verification" in page.ids and "citation" in page.ids, "Research navigation destination missing")
        check("open" in text.lower() and "non-Gaussian equality" in text, "Research scope limits missing")

    expected_urls = [BASE + "/"] + [BASE + "/publications/" + p["slug"] + "/" for p in DATA["papers"]] + [BASE + "/" + p.get("collection", "research") + "/" + p["slug"] + "/" for p in research]
    check(urls == expected_urls and len(set(urls)) == len(urls), "Sitemap must contain exactly the canonical URLs without duplicates")
    for url in urls:
        check(local_target(url, ROOT / "index.html")[0] in pages, "Sitemap target invalid")
    check((ROOT / "sitemap.txt").read_text(encoding="utf-8").splitlines() == urls, "Text sitemap differs from canonical XML URLs")
    for filename in ("sitemap.xml", "sitemap.txt"):
        check(f"Sitemap: {BASE}/{filename}" in (ROOT / "robots.txt").read_text(), f"Robots reference missing: {filename}")
    check((ROOT / ".nojekyll").is_file(), "GitHub Pages .nojekyll missing")
    home = pages[(ROOT / "index.html").resolve()]
    if research:
        check("selected-research" in home.ids, "Selected Research section missing")
        for work in research:
            check("/" + work.get("collection", "research") + "/" + work["slug"] + "/" in home.links, "Research not discoverable from home")
    for paper in DATA["papers"]:
        check("/publications/" + paper["slug"] + "/" in home.links, "Publication not discoverable from home")
        if paper.get("arxiv_id"):
            check(paper["record_url"] in home.links, "Home page arXiv link missing")
    first_publication = next(url for url in home.links if url.startswith("/publications/"))
    check(first_publication == "/publications/" + DATA["papers"][0]["slug"] + "/", "Featured publication order incorrect")
    print(f"PASS: {len(pages)} HTML pages, {link_count} local links/anchors/assets, {len(DATA['papers']) + len(research)} unchanged PDFs, exact abstracts and disclosures, citations, source/release archives, JSON-LD, canonical/scholarly metadata, sitemap and robots.txt.")
    print("LIMIT: contact-only and coordinated manuscripts intentionally omit scientific-author tags. These implementation checks do not verify the mathematics or confirm search-engine indexing.")


if __name__ == "__main__":
    main()
