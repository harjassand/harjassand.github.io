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

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data/publications.json").read_text())
BASE = DATA["base_url"].rstrip("/")
PAPERS = DATA["papers"]
PERSON_ID = BASE + "/#harjas-sandhu"


def e(value: str) -> str:
    return escape(str(value), quote=True)


def pretty_date(value: str) -> str:
    day = date.fromisoformat(value)
    return f"{day.day} {day.strftime('%B %Y')}"


def paper_path(paper: dict) -> str:
    return f"/publications/{paper['slug']}/"


def pdf_path(paper: dict) -> str:
    return paper_path(paper) + paper["pdf_filename"]


def schema_tag(schema: dict) -> str:
    return '<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=2).replace("</", "<\\/") + "\n</script>"


def head(title: str, description: str, path: str, paper: dict | None = None) -> str:
    canonical = BASE + path
    verification = ""
    if path == "/" and DATA.get("google_site_verification"):
        verification = f'\n  <meta name="google-site-verification" content="{e(DATA["google_site_verification"])}">'
    scholarly = ""
    if paper:
        # The manuscript identifies Harjas Sandhu solely as contact person.
        # Do not convert the repository creator field into an authorship claim.
        # Scholar requires an actual author: citation_author is deliberately absent.
        scholarly = f'''\n  <meta name="citation_title" content="{e(paper['title'])}">
  <meta name="citation_publication_date" content="{paper['publication_date'].replace('-', '/')}">
  <meta name="citation_online_date" content="{paper['publication_date'].replace('-', '/')}">
  <meta name="citation_pdf_url" content="{BASE + pdf_path(paper)}">
  <meta name="citation_doi" content="{e(paper['doi'])}">
  <meta name="citation_abstract_html_url" content="{canonical}">
  <meta name="citation_language" content="en">
  <meta name="DC.title" content="{e(paper['title'])}">
  <meta name="DC.identifier" content="https://doi.org/{e(paper['doi'])}">
  <meta name="DC.date" content="{paper['publication_date']}">
  <meta name="DC.issued" content="{paper['publication_date']}">
  <meta name="DC.publisher" content="Zenodo">
  <meta name="DC.contributor" content="Harjas Sandhu">
  <meta name="DC.rights" content="https://www.apache.org/licenses/LICENSE-2.0">
  <meta name="DC.type" content="Text">
  <meta name="DC.language" content="en">
  <link rel="alternate" type="application/pdf" href="{BASE + pdf_path(paper)}" title="Original deposited manuscript">
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
      <a href="/#research">Research</a>
      <a href="/#publications">Preprints</a>
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
        entries.append(f'''          <li>
            <h3><a href="{paper_path(paper)}">{e(paper['title'])}</a></h3>
            <p class="pub-meta">Preprint · Zenodo · October 2026 · Version {e(paper['version'])}</p>
            <p class="pub-summary">{e(paper['summary'])}</p>
            <div class="link-line">
              <a href="{paper_path(paper)}">Abstract &amp; details</a>
              <a href="{pdf_path(paper)}" aria-label="PDF: {e(paper['title'])}">PDF</a>
              <a href="https://doi.org/{e(paper['doi'])}" aria-label="DOI: {e(paper['title'])}">DOI</a>
              <a href="{paper_path(paper)}#citation" aria-label="Citation: {e(paper['title'])}">Cite</a>
            </div>
          </li>''')
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

    <section class="section-row" id="publications" aria-labelledby="publications-heading">
      <div>
        <h2 id="publications-heading">Preprints</h2>
        <p class="section-note">2026 · Two companion manuscripts</p>
      </div>
      <div class="section-copy">
        <p class="publication-context">For these companion quantum-information preprints, I developed and coordinated the agentic system used for the investigations and serve as manuscript contact. Each paper page describes my contribution and the manuscripts' provenance and review status.</p>
        <ol class="publication-list">
''' + "\n".join(entries) + '''
        </ol>
      </div>
    </section>

    <section class="section-row" aria-labelledby="provenance-heading">
      <h2 id="provenance-heading">About the manuscripts</h2>
      <div class="section-copy status-note">
        <p>The manuscripts attribute their new results and proofs to AI systems and identify me as contact person. Independent specialist review and priority assessment are pending. Each preprint page reproduces the original disclosure in full.</p>
      </div>
    </section>
  </main>
''' + footer()


def render_paper(paper: dict, companion: dict) -> str:
    path = paper_path(paper)
    bib = (ROOT / path.lstrip("/") / "citation.bib").read_text()
    title = paper["title"]
    canonical = BASE + path
    discovery_links = " · ".join(
        f'<a href="{e(record["url"])}">{e(record["name"])}</a>'
        for record in paper.get("discovery_records", [])
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "ScholarlyArticle",
        "@id": "https://doi.org/" + paper["doi"],
        "url": canonical,
        "name": title,
        "headline": title,
        "abstract": paper["abstract"],
        "datePublished": paper["publication_date"],
        "inLanguage": "en",
        "version": paper["version"],
        "genre": "Preprint",
        "creativeWorkStatus": "Preprint; independent specialist review and priority assessment pending",
        "identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": paper["doi"]},
        "publisher": {"@type": "Organization", "name": "Zenodo", "url": "https://zenodo.org/"},
        "contributor": {"@type": "Person", "@id": PERSON_ID, "name": "Harjas Sandhu", "url": BASE + "/"},
        "creditText": DATA["contributor_statement"] + " Original manuscript disclosure: " + paper["provenance"],
        "keywords": paper["keywords"],
        "isAccessibleForFree": True,
        "license": "https://www.apache.org/licenses/LICENSE-2.0",
        "sameAs": paper["record_url"],
        "encoding": {"@type": "MediaObject", "encodingFormat": "application/pdf", "contentUrl": BASE + pdf_path(paper), "contentSize": str(paper["pdf_bytes"]) + " bytes"},
    }
    if paper["record_id"] == 23349192:
        schema["citation"] = {"@type": "ScholarlyArticle", "@id": "https://doi.org/" + companion["doi"], "name": companion["title"]}
        relation_text = "This manuscript develops capacity and distillation consequences using the complete-order results of the companion preprint."
    else:
        relation_text = "The companion preprint develops capacity and one-way distillation consequences that depend on the order results presented here."
    kilobytes = round(paper["pdf_bytes"] / 1000)
    return head(title + " — Harjas Sandhu", paper["abstract"], path, paper) + schema_tag(schema) + f'''
</head>
<body>
''' + header() + f'''
  <main class="paper-main" id="main">
    <p class="breadcrumb"><a href="/#publications">← All preprints</a></p>
    <article aria-labelledby="paper-title">
      <header class="paper-header">
        <p class="eyebrow">Preprint · Quantum information</p>
        <h1 id="paper-title">{e(title)}</h1>
        <p class="contact-credit">Manuscript contact: <a href="/">Harjas Sandhu</a></p>
      </header>

      <section class="paper-section paper-abstract" aria-labelledby="abstract-heading">
        <h2 id="abstract-heading">Abstract</h2>
        <p class="abstract-text">{e(paper['abstract'])}</p>
        <p class="abstract-label">Abstract reproduced from the deposited manuscript.</p>
      </section>

      <p class="paper-dates">Manuscript dated <time datetime="{paper['manuscript_date']}">{pretty_date(paper['manuscript_date'])}</time>.<br>Published on Zenodo <time datetime="{paper['publication_date']}">{pretty_date(paper['publication_date'])}</time> · Version {e(paper['version'])}</p>
      <div class="paper-actions">
        <a class="pdf-link" href="{pdf_path(paper)}">Read PDF <span class="file-detail">{kilobytes} kB</span></a>
        <a href="https://doi.org/{e(paper['doi'])}">DOI</a>
        <a href="{e(paper['record_url'])}">Zenodo record</a>
        <a href="#citation">Cite</a>
      </div>

      <section class="paper-section provenance" aria-labelledby="provenance-heading">
        <h2 id="provenance-heading">Contribution and provenance</h2>
        <p class="contributor-credit">{e(DATA['contributor_statement'])}</p>
        <blockquote>{e(paper['provenance'])}</blockquote>
        <p>The quotation reproduces the original manuscript’s title-page footnote. The contribution statement above describes system development and coordination; it does not assert scientific authorship. The repository lists “Sandhu, Harjas” as creator.</p>
      </section>

      <section class="paper-section" aria-labelledby="details-heading">
        <h2 id="details-heading">Publication details</h2>
        <dl class="paper-details">
          <dt>Repository</dt><dd>Zenodo</dd>
          <dt>Type</dt><dd>Preprint</dd>
          <dt>DOI</dt><dd><a href="https://doi.org/{e(paper['doi'])}">{e(paper['doi'])}</a></dd>
          <dt>Version</dt><dd>{e(paper['version'])}</dd>
          <dt>License</dt><dd><a href="https://www.apache.org/licenses/LICENSE-2.0">Apache License 2.0</a> (as deposited)</dd>
          <dt>Original files</dt><dd><a href="{e(paper['record_url'])}#files">PDF and LaTeX source on Zenodo</a></dd>
          <dt>Catalogue records</dt><dd>{discovery_links}</dd>
        </dl>
      </section>

      <section class="paper-section" id="citation" aria-labelledby="citation-heading">
        <h2 id="citation-heading">Citation</h2>
        <p class="citation-text">Sandhu, Harjas. (2026). <cite>{e(title)}</cite> (Version {e(paper['version'])}). Zenodo. <a href="https://doi.org/{e(paper['doi'])}">https://doi.org/{e(paper['doi'])}</a></p>
        <p class="citation-note">This citation follows the repository’s creator metadata. It should be read together with the contact-only role and manuscript provenance disclosed above.</p>
        <div class="link-line">
          <a href="{path}citation.bib" download>Download BibTeX</a>
          <a href="{path}citation.ris" download>Download RIS</a>
        </div>
        <details>
          <summary>View BibTeX</summary>
          <pre><code>{e(bib)}</code></pre>
        </details>
        <p class="abstract-label">BibTeX from Zenodo; RIS from the DOI citation service. Both downloads preserve the source exports.</p>
      </section>

      <section class="paper-section companion" aria-labelledby="companion-heading">
        <h2 id="companion-heading">Companion preprint</h2>
        <p>{e(relation_text)}</p>
        <p><a href="{paper_path(companion)}">{e(companion['title'])}</a></p>
      </section>
    </article>
  </main>
''' + footer()


def main() -> None:
    (ROOT / "index.html").write_text(render_home())
    for index, paper in enumerate(PAPERS):
        (ROOT / paper_path(paper).lstrip("/") / "index.html").write_text(render_paper(paper, PAPERS[1 - index]))
    not_found = head("Page not found — Harjas Sandhu", "The requested page could not be found. Return to Harjas Sandhu’s research website.", "/404.html")
    not_found = not_found.replace('content="index,follow,max-snippet:-1,max-image-preview:large"', 'content="noindex,follow"')
    (ROOT / "404.html").write_text(not_found + '''</head>
<body>
''' + header() + '''
  <main class="error-main" id="main">
    <p class="eyebrow">404</p>
    <h1>Page not found</h1>
    <p>The address may have changed. <a href="/">Return to the home page</a> or <a href="/#publications">browse the preprints</a>.</p>
  </main>
''' + footer())
    urls = [BASE + "/"] + [BASE + paper_path(paper) for paper in PAPERS]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{url}</loc></url>\n" for url in urls) + "</urlset>\n")
    (ROOT / "sitemap.txt").write_text("\n".join(urls) + "\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\nSitemap: {BASE}/sitemap.txt\n")
    print(f"Generated home, {len(PAPERS)} publication pages, 404, robots.txt and XML/text sitemaps.")


if __name__ == "__main__":
    main()
