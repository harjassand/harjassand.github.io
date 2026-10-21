#!/usr/bin/env python3
"""Regenerate the buildless website from its small public metadata file.

Python's standard library is sufficient. PDF and citation bytes are separate,
checked assets: this script never rewrites them.
"""
from __future__ import annotations

from datetime import date
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data/publications.json").read_text())
BASE = DATA["base_url"].rstrip("/")
PAPERS = DATA["papers"]
RESEARCH = DATA.get("selected_research", [])
WORKS = PAPERS + RESEARCH
PERSON_ID = BASE + "/#harjas-sandhu"


def e(value: str) -> str:
    return escape(str(value), quote=True)


def pretty_date(value: str) -> str:
    day = date.fromisoformat(value)
    return f"{day.day} {day.strftime('%B %Y')}"


def paper_path(paper: dict) -> str:
    return f"/{paper.get('collection', 'publications')}/{paper['slug']}/"


def pdf_path(paper: dict) -> str:
    return paper_path(paper) + paper["pdf_filename"]


def person(name: str) -> dict:
    result = {"@type": "Person", "name": name}
    if name == DATA["owner_name"]:
        result.update({"@id": PERSON_ID, "url": BASE + "/"})
    return result


def credit_line(paper: dict, linked: bool = False) -> str:
    names = paper["authors"] or [paper.get("contact_name") or paper["contributor_name"]]
    formatted = [f'<a href="/">{e(name)}</a>' if linked and name == DATA["owner_name"] else e(name) for name in names]
    prefix = {"contact": "Manuscript contact: ", "coordinator": "Research direction and coordination: "}.get(paper["credit_role"], "")
    return prefix + " and ".join(formatted)


def publication_label(paper: dict) -> str:
    if paper["credit_role"] == "contact":
        return "AI-generated manuscript"
    return "Coauthored preprint" if len(paper["authors"]) > 1 else "Preprint"


def schema_tag(schema: dict) -> str:
    return '<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=2).replace("</", "<\\/") + "\n</script>"


def write_page(path: Path, html: str) -> None:
    path.write_text("\n".join(line.rstrip() for line in html.splitlines()) + "\n", encoding="utf-8")


def head(title: str, description: str, path: str, paper: dict | None = None) -> str:
    canonical = BASE + path
    verification = ""
    if path == "/" and DATA.get("google_site_verification"):
        verification = f'\n  <meta name="google-site-verification" content="{e(DATA["google_site_verification"])}">'
    scholarly = ""
    if paper:
        author_tags = "\n".join(f'  <meta name="citation_author" content="{e(name)}">' for name in paper["authors"])
        creator_tags = "\n".join(f'  <meta name="DC.creator" content="{e(name)}">' for name in paper["authors"])
        contributor = paper.get("contact_name") or paper.get("contributor_name")
        contributor_tag = f'\n  <meta name="DC.contributor" content="{e(contributor)}">' if contributor else ""
        doi_tag = f'\n  <meta name="citation_doi" content="{e(paper["doi"])}">' if paper.get("doi") else ""
        identifier = "https://doi.org/" + paper["doi"] if paper.get("doi") else canonical
        publisher_tag = f'\n  <meta name="DC.publisher" content="{e(paper["publisher"])}">' if paper.get("publisher") else ""
        rights = paper.get("license_url") or paper.get("rights_notice", "")
        scholarly = f'''\n  <meta name="citation_title" content="{e(paper['title'])}">
{author_tags}
  <meta name="citation_publication_date" content="{paper['publication_date'].replace('-', '/')}">
  <meta name="citation_online_date" content="{paper['publication_date'].replace('-', '/')}">
  <meta name="citation_pdf_url" content="{BASE + pdf_path(paper)}">
{doi_tag}
  <meta name="citation_abstract_html_url" content="{canonical}">
  <meta name="citation_language" content="en">
  <meta name="DC.title" content="{e(paper['title'])}">
{creator_tags}
  <meta name="DC.identifier" content="{e(identifier)}">
  <meta name="DC.date" content="{paper['publication_date']}">
  <meta name="DC.issued" content="{paper['publication_date']}">
{publisher_tag}{contributor_tag}
  <meta name="DC.rights" content="{e(rights)}">
  <meta name="DC.type" content="Text">
  <meta name="DC.language" content="en">
  <link rel="alternate" type="application/pdf" href="{BASE + pdf_path(paper)}" title="{'Original manuscript PDF' if paper in RESEARCH else 'Original deposited manuscript'}">
  <meta name="keywords" content="{e(', '.join(paper['keywords']))}">'''
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="theme-color" content="#fbfaf7">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">{verification}
  <meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
  <link rel="canonical" href="{canonical}">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/assets/style.css">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:type" content="{'article' if paper else 'website'}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="Harjas Sandhu">
  <meta property="og:locale" content="en_AU">{scholarly}
'''


def header() -> str:
    return '''<a class="skip-link" href="#main">Skip to content</a>
<div class="shell">
  <header class="site-header">
    <a class="wordmark" href="/">Harjas Sandhu</a>
    <nav aria-label="Main navigation">
      <a href="/#research">Interests</a>
      <a href="/#selected-research">Selected research</a>
      <a href="/#publications">Publications</a>
    </nav>
  </header>'''


def footer() -> str:
    return '''  <footer class="site-footer">
    <p>A personal research website. University affiliation describes student status and does not imply University endorsement.</p>
    <a href="https://github.com/harjassand/harjassand.github.io">Website source</a>
  </footer>
</div>
</body>
</html>
'''


def render_home() -> str:
    person = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Person",
                "@id": PERSON_ID,
                "name": "Harjas Sandhu",
                "url": BASE + "/",
                "description": "Mathematics student at the University of Queensland, majoring in Mathematical AI, with interests in machine learning and AI for scientific discovery in physics, energy, and materials science.",
                "affiliation": {"@type": "CollegeOrUniversity", "name": "The University of Queensland", "url": "https://www.uq.edu.au/"},
                "knowsAbout": ["Machine learning", "AI for scientific discovery", "Physics", "Energy", "Materials science"],
            },
            {"@type": "ProfilePage", "@id": BASE + "/#profile", "url": BASE + "/", "name": "Harjas Sandhu", "mainEntity": {"@id": PERSON_ID}},
        ],
    }
    entries = []
    for paper in PAPERS:
        repository_link = f'<a href="{e(paper["record_url"])}" aria-label="arXiv: {e(paper["title"])}">arXiv</a>' if paper.get("arxiv_id") else ""
        entries.append(f'''          <li>
            <h3><a href="{paper_path(paper)}">{e(paper['title'])}</a></h3>
            <p class="pub-meta">{credit_line(paper)}<br>{publication_label(paper)} · {e(paper['publisher'])} · {pretty_date(paper['publication_date'])} · Version {e(paper['version'])}</p>
            <p class="pub-summary">{e(paper['summary'])}</p>
            <div class="link-line">
              <a href="{paper_path(paper)}">Abstract &amp; details</a>
              <a href="{pdf_path(paper)}" aria-label="PDF: {e(paper['title'])}">PDF</a>
              {repository_link}
              <a href="https://doi.org/{e(paper['doi'])}" aria-label="DOI: {e(paper['title'])}">DOI</a>
              <a href="{paper_path(paper)}#citation" aria-label="Citation: {e(paper['title'])}">Cite</a>
            </div>
          </li>''')
    selected = ""
    if RESEARCH:
        features = []
        for work in RESEARCH:
            features.append(f'''        <div class="publication-list research-feature">
          <h3><a href="{paper_path(work)}">{e(work['title'])}</a></h3>
          <p class="pub-meta">AI-generated mathematical manuscript · {pretty_date(work['manuscript_date'])} · Proof candidate</p>
          <p class="pub-summary">{e(work['summary'])}</p>
          <div class="link-line">
            <a href="{paper_path(work)}">Read the explanation &amp; manuscript</a>
            <a href="{pdf_path(work)}" aria-label="PDF: {e(work['title'])}">PDF</a>
            <a href="{paper_path(work)}{e(work['source_filename'])}" aria-label="LaTeX source: {e(work['title'])}">LaTeX source</a>
          </div>
        </div>''')
        selected = '''
    <section class="section-row" id="selected-research" aria-labelledby="selected-research-heading">
      <div>
        <h2 id="selected-research-heading">Selected research</h2>
        <p class="section-note">Manuscripts and mathematical ideas</p>
      </div>
      <div class="section-copy">
''' + "\n".join(features) + '''
      </div>
    </section>
'''
    return head("Harjas Sandhu — AI for Scientific Discovery", "Harjas Sandhu studies mathematics at the University of Queensland, majoring in Mathematical AI, with interests in machine learning and AI for scientific discovery.", "/") + schema_tag(person) + '''
</head>
<body>
''' + header() + '''
  <main id="main">
    <section class="intro" aria-labelledby="harjas-sandhu">
      <p class="eyebrow">Mathematics &amp; scientific discovery</p>
      <h1 id="harjas-sandhu">Harjas Sandhu</h1>
      <p class="position">Mathematics Student | AI &amp; Scientific Discovery</p>
      <div class="bio">
        <p>I'm studying mathematics at the University of Queensland, majoring in Mathematical AI. I'm interested in how AI could help us solve difficult problems in mathematics and science, particularly those that are beyond what current methods can achieve.</p>
        <p>I developed and coordinated an agentic AI system for independent investigations in mathematics and the physical sciences. I'm interested in how these systems can support reliable scientific research and build on previous discoveries.</p>
      </div>
    </section>

    <section class="section-row" id="research" aria-labelledby="research-heading">
      <h2 id="research-heading">Research interests</h2>
      <div class="section-copy">
        <p>My main interests are machine learning and AI for scientific discovery. I'm particularly interested in applying advances in AI and computation to problems in physics, energy, and materials science.</p>
        <p>I'm also interested in what it would take for AI systems to carry out reliable scientific research: developing new ideas, testing them, recognising mistakes, and building on previous discoveries.</p>
      </div>
    </section>

''' + selected + '''
    <section class="section-row" id="publications" aria-labelledby="publications-heading">
      <div>
        <h2 id="publications-heading">Publications &amp; manuscripts</h2>
        <p class="section-note">2026 · ''' + str(sum(p['credit_role'] == 'author' for p in PAPERS)) + ''' coauthored preprint · ''' + str(sum(p['credit_role'] == 'contact' for p in PAPERS)) + ''' AI-generated manuscripts</p>
      </div>
      <div class="section-copy">
        <p class="publication-context">The group-theory preprint is joint work with Andreas Thom. For the two AI-generated quantum-information manuscripts, I developed and coordinated the agentic system and serve solely as contact. Each page describes the work’s contribution and provenance.</p>
        <ol class="publication-list">
''' + "\n".join(entries) + '''
        </ol>
      </div>
    </section>

    <section class="section-row" aria-labelledby="provenance-heading">
      <h2 id="provenance-heading">About the quantum manuscripts</h2>
      <div class="section-copy status-note">
        <p>The two quantum-information manuscripts attribute their new results and proofs to AI systems. My contribution was developing and coordinating the agentic system, and I serve solely as the manuscript contact. Independent specialist review and priority assessment are pending. Each manuscript page reproduces the original disclosure.</p>
      </div>
    </section>
  </main>
''' + footer()


def article_schema(paper: dict) -> dict:
    schema = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "@id": "https://doi.org/" + paper["doi"] if paper.get("doi") else BASE + paper_path(paper) + "#manuscript",
        "url": BASE + paper_path(paper),
        "name": paper["title"],
        "headline": paper["title"],
        "abstract": paper["abstract"],
        "datePublished": paper["publication_date"],
        "inLanguage": "en",
        "version": paper["version"],
        "genre": "Preprint",
        "creativeWorkStatus": "Preprint",
        "creditText": " ".join(filter(None, [paper.get("contribution"), paper["provenance"], paper.get("provenance_summary")])),
        "keywords": paper["keywords"],
        "isAccessibleForFree": True,
        "encoding": {"@type": "MediaObject", "encodingFormat": "application/pdf",
                     "contentUrl": BASE + pdf_path(paper), "contentSize": str(paper["pdf_bytes"]) + " bytes"},
    }
    if paper.get("doi"):
        schema["identifier"] = {"@type": "PropertyValue", "propertyID": "DOI", "value": paper["doi"]}
    if paper.get("publisher"):
        schema["publisher"] = {"@type": "Organization", "name": paper["publisher"], "url": paper["publisher_url"]}
    if paper.get("license_url"):
        schema["license"] = paper["license_url"]
    if paper.get("record_url"):
        schema["sameAs"] = paper["record_url"]
    if paper["authors"]:
        schema["author"] = [person(name) for name in paper["authors"]]
    if paper.get("contact_name"):
        schema["contributor"] = person(paper["contact_name"])
        schema["creativeWorkStatus"] = "Preprint; independent specialist review and priority assessment pending"
    if paper.get("contributor_name"):
        schema["contributor"] = person(paper["contributor_name"])
        schema["genre"] = "Research manuscript"
        schema["creativeWorkStatus"] = paper["verification_status"]
        schema["identifier"] = {"@type": "PropertyValue", "propertyID": "SHA-256", "value": paper["pdf_sha256"]}
        schema["isBasedOn"] = {"@type": "ScholarlyArticle", "name": paper["based_on"]["title"], "url": paper["based_on"]["url"], "license": paper["based_on"]["license"], "author": {"@type": "Organization", "name": "OpenAI"}}
    relation = paper.get("companion")
    if relation and relation.get("cites"):
        companion = next(p for p in PAPERS if p["slug"] == relation["slug"])
        schema["citation"] = {"@type": "ScholarlyArticle", "@id": "https://doi.org/" + companion["doi"], "name": companion["title"]}
    return schema


def render_paper(paper: dict) -> str:
    path = paper_path(paper)
    title = paper["title"]
    bib = (ROOT / path.lstrip("/") / "citation.bib").read_text()
    is_arxiv = bool(paper.get("arxiv_id"))
    if is_arxiv:
        provenance = f'''<blockquote>{e(paper['provenance'])}</blockquote>
        <p>{e(paper['provenance_summary'])}</p>
        <p class="abstract-label">The quotation is an excerpt from the paper’s acknowledgments. “The second author” refers to Andreas Thom. <a href="https://arxiv.org/html/{e(paper['arxiv_id'])}v{e(paper['version'])}">Read the full paper and acknowledgments.</a></p>'''
        source_details = f'''<dt>Identifier</dt><dd><a href="{e(paper['record_url'])}">arXiv:{e(paper['arxiv_id'])} [math.GR]</a></dd>
          <dt>PDF source</dt><dd><a href="{e(paper['pdf_source_url'])}">Unmodified arXiv v{e(paper['version'])} PDF</a>, by {e(' and '.join(paper['authors']))}</dd>'''
        version_note = f'''<p class="abstract-label">The <a href="{e(paper['commentary_url'])}">hosted commentary</a> is also listed on <a href="{e(paper['commentary_scholar_url'])}">Andreas Thom’s Scholar profile</a> with the date {pretty_date(paper['commentary_date'])}. These are versions of the same work.</p>'''
        citation = f"{e(' and '.join(paper['authors']))}. ({paper['publication_date'][:4]}). <cite>{e(title)}</cite>. arXiv:{e(paper['arxiv_id'])}v{e(paper['version'])}."
        citation_note = "Citation downloads prepared from the public arXiv record."
        citation_caveat = ""
    else:
        provenance = f'''<p class="contributor-credit">{e(paper['contribution'])}</p>
        <blockquote>{e(paper['provenance'])}</blockquote>
        <p>The quotation reproduces the manuscript’s title-page footnote. The original deposited PDF is unchanged.</p>'''
        discovery_links = " · ".join(f'<a href="{e(record["url"])}">{e(record["name"])}</a>' for record in paper.get("discovery_records", []))
        source_details = f'''<dt>Original files</dt><dd><a href="{e(paper['record_url'])}#files">PDF and LaTeX source on Zenodo</a></dd>'''
        if discovery_links:
            source_details += f"<dt>Catalogue records</dt><dd>{discovery_links}</dd>"
        version_note = ""
        citation = f"<cite>{e(title)}</cite>. ({paper['publication_date'][:4]}). Version {e(paper['version'])}. {e(paper['publisher'])}."
        citation_note = "BibTeX from Zenodo; RIS from the DOI citation service. Both downloads preserve the source exports."
        citation_caveat = '<p class="citation-note">The title-first reference above follows the manuscript’s contact-only credit. The source citation exports below name Harjas Sandhu in the repository creator field; that repository metadata differs from the scientific authorship disclosed in the manuscript.</p>'
    relation = paper.get("companion")
    related_section = ""
    if relation:
        companion = next(p for p in PAPERS if p["slug"] == relation["slug"])
        related_section = f'''
      <section class="paper-section companion" aria-labelledby="companion-heading">
        <h2 id="companion-heading">Companion manuscript</h2>
        <p>{e(relation['description'])}</p>
        <p><a href="{paper_path(companion)}">{e(companion['title'])}</a></p>
      </section>'''
    return head(title + " — Harjas Sandhu", paper["abstract"], path, paper) + schema_tag(article_schema(paper)) + f'''
</head>
<body>
''' + header() + f'''
  <main class="paper-main" id="main">
    <p class="breadcrumb"><a href="/#publications">← Publications and manuscripts</a></p>
    <article aria-labelledby="paper-title">
      <header class="paper-header">
        <p class="eyebrow">{publication_label(paper)} · {e(paper['subject'])}</p>
        <h1 id="paper-title">{e(title)}</h1>
        <p class="contact-credit">{credit_line(paper, linked=True)}</p>
      </header>
      <section class="paper-section paper-abstract" aria-labelledby="abstract-heading">
        <h2 id="abstract-heading">Abstract</h2>
        <p class="abstract-text">{e(paper['abstract'])}</p>
        <p class="abstract-label">Abstract reproduced from the {e(paper['abstract_source'])}.</p>
      </section>
      <p class="paper-dates">Manuscript dated <time datetime="{paper['manuscript_date']}">{pretty_date(paper['manuscript_date'])}</time>.<br>{'Posted on' if is_arxiv else 'Published on'} {e(paper['publisher'])} <time datetime="{paper['publication_date']}">{pretty_date(paper['publication_date'])}</time> · Version {e(paper['version'])}</p>
      <div class="paper-actions">
        <a class="pdf-link" href="{pdf_path(paper)}">Read PDF <span class="file-detail">{round(paper['pdf_bytes'] / 1000)} kB</span></a>
        <a href="{e(paper['record_url'])}">{e(paper['publisher'])} record</a>
        <a href="https://doi.org/{e(paper['doi'])}">DOI</a>
        <a href="#citation">Cite</a>
      </div>
      <section class="paper-section provenance" aria-labelledby="provenance-heading">
        <h2 id="provenance-heading">Contribution and provenance</h2>
        {provenance}
      </section>
      <section class="paper-section" aria-labelledby="details-heading">
        <h2 id="details-heading">Publication details</h2>
        <dl class="paper-details">
          <dt>Repository</dt><dd>{e(paper['publisher'])}</dd>
          <dt>Type</dt><dd>Preprint</dd>
          <dt>DOI</dt><dd><a href="https://doi.org/{e(paper['doi'])}">{e(paper['doi'])}</a></dd>
          <dt>Version</dt><dd>{e(paper['version'])}</dd>
          <dt>License</dt><dd><a href="{e(paper['license_url'])}">{e(paper['license_name'])}</a> (as deposited)</dd>
          {source_details}
        </dl>
        {version_note}
      </section>
      <section class="paper-section" id="citation" aria-labelledby="citation-heading">
        <h2 id="citation-heading">Citation</h2>
        <p class="citation-text">{citation} <a href="https://doi.org/{e(paper['doi'])}">https://doi.org/{e(paper['doi'])}</a></p>
        {citation_caveat}
        <div class="link-line">
          <a href="{path}citation.bib" download>Download BibTeX</a>
          <a href="{path}citation.ris" download>Download RIS</a>
        </div>
        <details><summary>View BibTeX</summary><pre><code>{e(bib)}</code></pre></details>
        <p class="abstract-label">{citation_note}</p>
      </section>{related_section}
    </article>
  </main>
''' + footer()


def render_research(paper: dict) -> str:
    path = paper_path(paper)
    body = (ROOT / "tools/templates" / (paper["slug"] + ".html.in")).read_text()
    replacements = {
        "TITLE": e(paper["title"]), "CREDIT": credit_line(paper, linked=True),
        "DATE": pretty_date(paper["manuscript_date"]), "PAGES": str(paper["page_count"]),
        "PDF": pdf_path(paper), "PATH": path, "ABSTRACT": e(paper["abstract"]),
        "PROVENANCE": e(paper["provenance"]), "CONTRIBUTION": e(paper["contribution"]),
        "STATUS": e(paper["verification_status"]), "RIGHTS": e(paper["rights_notice"]),
        "UPSTREAM": e(paper["based_on"]["url"]), "VERSION_PDF": e(paper["version_pdf_url"]),
        "BIBTEX": e((ROOT / path.lstrip("/") / "citation.bib").read_text()),
    }
    for key, value in replacements.items():
        body = body.replace("{{" + key + "}}", value)
    if re.search(r"\{\{[A-Z_]+\}\}", body):
        raise ValueError("Unfilled research template field")
    return head(paper["title"] + " — Harjas Sandhu", paper["description"], path, paper) + schema_tag(article_schema(paper)) + "\n</head>\n<body>\n" + header() + "\n" + body + footer()


def main() -> None:
    slugs = [paper["slug"] for paper in WORKS]
    dois = [paper["doi"] for paper in WORKS if paper.get("doi")]
    if len(set(slugs)) != len(slugs) or len(set(dois)) != len(dois):
        raise ValueError("Each publication needs a unique slug and DOI")
    for paper in WORKS:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", paper["slug"]):
            raise ValueError("Invalid publication slug")
        if paper["credit_role"] not in ("author", "contact", "coordinator"):
            raise ValueError("Unknown credit role")
        if bool(paper["authors"]) != (paper["credit_role"] == "author"):
            raise ValueError("Scientific authors must be explicit; a contact cannot be an author fallback")
        if paper["credit_role"] == "contact" and not paper.get("contact_name"):
            raise ValueError("Contact-only manuscripts require a named contact")
        if paper["credit_role"] == "coordinator" and not paper.get("contributor_name"):
            raise ValueError("Coordinated research requires an explicit contributor")
        relation = paper.get("companion")
        if relation and (relation["slug"] not in slugs or relation["slug"] == paper["slug"]):
            raise ValueError("Companion must identify another publication by slug")
        expected_source = "manuscript_metadata" if paper in RESEARCH else "arxiv_metadata" if paper.get("arxiv_id") else "repository_exports"
        if paper["citation_source"] != expected_source:
            raise ValueError("Unsupported citation source")
    write_page(ROOT / "index.html", render_home())
    for paper in PAPERS:
        write_page(ROOT / paper_path(paper).lstrip("/") / "index.html", render_paper(paper))
    for paper in RESEARCH:
        write_page(ROOT / paper_path(paper).lstrip("/") / "index.html", render_research(paper))
    not_found = head("Page not found — Harjas Sandhu", "The requested page could not be found. Return to Harjas Sandhu’s research website.", "/404.html")
    not_found = not_found.replace('content="index,follow,max-snippet:-1,max-image-preview:large"', 'content="noindex,follow"')
    write_page(ROOT / "404.html", not_found + '''</head>
<body>
''' + header() + '''
  <main class="error-main" id="main">
    <p class="eyebrow">404</p>
    <h1>Page not found</h1>
    <p>The address may have changed. <a href="/">Return to the home page</a> or <a href="/#publications">browse the preprints</a>.</p>
  </main>
''' + footer())
    urls = [BASE + "/"] + [BASE + paper_path(paper) for paper in WORKS]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{url}</loc></url>\n" for url in urls) + "</urlset>\n")
    (ROOT / "sitemap.txt").write_text("\n".join(urls) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\nSitemap: {BASE}/sitemap.txt\n")
    print(f"Generated home, {len(PAPERS)} publication pages, {len(RESEARCH)} research pages, 404, robots.txt and XML/text sitemaps.")


if __name__ == "__main__":
    main()
