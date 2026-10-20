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
        self.canonical = []
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
        if tag == "link" and attr.get("rel") == "canonical":
            self.canonical.append(attr.get("href"))
        if tag == "a" and "href" in attr:
            self.links.append(attr["href"])
        if tag == "link" and attr.get("rel") in ("stylesheet", "icon"):
            self.links.append(attr["href"])
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
    for path, page in pages.items():
        label = path.relative_to(ROOT)
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
        check(page.meta.get("DC.publisher") == "Zenodo", f"{paper['slug']}: incorrect publisher")
        check("citation_author" not in page.meta, f"{paper['slug']}: unsupported scientific-author assertion")
        visible_text = " ".join(" ".join(page.text).split())
        check(paper["abstract"] in visible_text, f"{paper['slug']}: exact abstract missing")
        check(paper["provenance"] in visible_text, f"{paper['slug']}: exact disclosure missing")
        article = page.schema[0]
        check(article["@type"] == "ScholarlyArticle", "Article schema type incorrect")
        check(article["abstract"] == paper["abstract"], "Schema abstract mismatch")
        check(article["encoding"]["contentUrl"] == page.meta["citation_pdf_url"], "Schema PDF mismatch")
        check(article["identifier"]["value"] == paper["doi"], "Schema DOI mismatch")
        check("author" not in article, "Unsupported schema author assertion")
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
    check(len(urls) == len(DATA["papers"]) + 1, "Sitemap URL count invalid")
    for url in urls:
        check(local_target(url, ROOT / "index.html")[0] in pages, "Sitemap target invalid")
    check(f"Sitemap: {BASE}/sitemap.xml" in (ROOT / "robots.txt").read_text(), "Robots sitemap missing")
    check((ROOT / ".nojekyll").is_file(), "GitHub Pages .nojekyll missing")
    print(f"PASS: {len(pages)} HTML pages, {link_count} local links/anchors/assets, {len(DATA['papers'])} unchanged PDFs, exact abstracts and disclosures, citation exports, JSON-LD, canonical/scholarly metadata, sitemap and robots.txt.")
    print("LIMIT: author metadata intentionally absent because manuscripts specify contact-only role; no search-engine indexing claim.")


if __name__ == "__main__":
    main()
