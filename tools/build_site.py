#!/usr/bin/env python3
"""Build a static, accessible papers collection using only the standard library.

Published PDF, source, licence and citation bytes are preserved separately.
"""
from __future__ import annotations
from datetime import date
from html import escape
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data/publications.json").read_text())
BASE = DATA["base_url"].rstrip("/")
PAPERS = DATA["papers"]
PERSON_ID = BASE + "/#harjas-sandhu"
STYLE_REVISION = hashlib.sha256((ROOT / "assets/style.css").read_bytes()).hexdigest()[:12]

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
  <link rel="alternate" type="application/pdf" href="{BASE + pdf_path(paper)}" title="{'Manuscript PDF'}">
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
  <link rel="stylesheet" href="/assets/style.css?v={STYLE_REVISION}">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(description)}">
  <meta property="og:type" content="{'article' if paper else 'website'}">
  <meta property="og:url" content="{canonical}">
  <meta property="og:site_name" content="Harjas Sandhu">
  <meta property="og:locale" content="en_AU">{scholarly}
'''

def footer() -> str:
    return f'''  <footer class="site-footer">
    <p>A personal research website. University affiliation describes student status and does not imply University endorsement.</p>
    <div class="link-line">
      <a href="{e(DATA['scholar_profile_url'])}" rel="me">Google Scholar</a>
      <a href="https://github.com/harjassand/harjassand.github.io">Website source</a>
    </div>
  </footer>
</div>
</body>
</html>
'''

def render_reader_note(paper: dict) -> str:
    template = paper.get("reader_note_template")
    if not template:
        return ""
    body = (ROOT / "tools/templates" / template).read_text()
    for key, value in {"PDF": pdf_path(paper), "UPSTREAM": e(paper.get("based_on", {}).get("url", ""))}.items():
        body = body.replace("{{" + key + "}}", value)
    if re.search(r"\{\{[A-Z_]+\}\}", body):
        raise ValueError("Unfilled reader note template field")
    return body

def header() -> str:
    return '''<a class="skip-link" href="#main">Skip to content</a>
<div class="shell">
  <header class="site-header">
    <a class="wordmark" href="/">Harjas Sandhu</a>
    <nav aria-label="Main navigation">
      <a href="/#papers">Papers</a>
      <a href="/#about">About</a>
    </nav>
  </header>'''


def acknowledgement(paper: dict | None = None) -> str:
    note = f'<p>{e(paper["acknowledgement_note"])}</p>' if paper and paper.get('acknowledgement_note') else ''
    return f'''<section class="paper-section acknowledgement" id="acknowledgements" aria-labelledby="acknowledgements-heading">
        <h2 id="acknowledgements-heading">Acknowledgements and AI use</h2>
        <p>{e(DATA['ai_acknowledgement'])}</p>{note}
      </section>'''


def article_schema(paper: dict) -> dict:
    schema = {
        '@context': 'https://schema.org', '@type': 'ScholarlyArticle',
        '@id': 'https://doi.org/' + paper['doi'] if paper.get('doi') else BASE + paper_path(paper),
        'url': BASE + paper_path(paper), 'name': paper['title'], 'headline': paper['title'],
        'abstract': paper['abstract'], 'datePublished': paper['publication_date'],
        'inLanguage': 'en', 'version': paper['version'], 'genre': paper['display_type'],
        'creativeWorkStatus': paper['display_type'], 'creditText': DATA['ai_acknowledgement'],
        'keywords': paper['keywords'], 'isAccessibleForFree': True,
        'encoding': {'@type': 'MediaObject', 'encodingFormat': 'application/pdf',
                     'contentUrl': BASE + pdf_path(paper), 'contentSize': str(paper['pdf_bytes']) + ' bytes'},
    }
    if paper['authors']:
        schema['author'] = [person(name) for name in paper['authors']]
    contributor = paper.get('contact_name') or paper.get('contributor_name')
    if contributor:
        schema['contributor'] = person(contributor)
    if paper.get('doi'):
        schema['identifier'] = {'@type': 'PropertyValue', 'propertyID': 'DOI', 'value': paper['doi']}
    if paper.get('license_url'):
        schema['license'] = paper['license_url']
    if paper.get('record_url') != BASE + paper_path(paper):
        schema['sameAs'] = paper['record_url']
    if paper.get('based_on'):
        upstream = paper['based_on']
        schema['isBasedOn'] = {'@type': 'ScholarlyArticle', 'name': upstream['title'],
                               'url': upstream['url'], 'license': upstream['license']}
    return schema


def resources(paper: dict) -> list[tuple[str, str]]:
    path = paper_path(paper)
    links = [('Read PDF', pdf_path(paper))]
    if paper['record_url'] != BASE + path:
        links.append((paper['publisher'] + ' record', paper['record_url']))
    if paper.get('source_filename'):
        links.append(('LaTeX source', path + paper['source_filename']))
    for link in paper.get('resource_links', []):
        url = link['url']
        if not url.startswith(('/', 'https://')):
            url = path + url
        links.append((link['label'], url))
    return links


def render_entry(paper: dict, expanded: bool = False) -> str:
    path = paper_path(paper)
    link_items = [('Paper details', path), ('PDF', pdf_path(paper))]
    if paper.get('doi'):
        link_items.append(('DOI', 'https://doi.org/' + paper['doi']))
    links = '\n'.join(f'<a href="{e(url)}" aria-label="{e(label + ': ' + paper['title'])}">{e(label)}</a>' for label, url in link_items)
    return f'''<li>
          <details class="paper-entry"{' open' if expanded else ''}>
            <summary><span class="entry-title">{e(paper['title'])}</span><span class="entry-meta">{e(paper['subject'])} · {pretty_date(paper['publication_date'])}</span></summary>
            <div class="entry-body">
              <p class="pub-summary">{e(paper['summary'])}</p>
              <p class="pub-meta">{credit_line(paper)} · {e(paper['display_type'])}</p>
              <div class="link-line">{links}</div>
            </div>
          </details>
        </li>'''


def render_home() -> str:
    schema = {
        '@context': 'https://schema.org', '@type': 'ProfilePage', 'url': BASE + '/',
        'mainEntity': {'@type': 'Person', '@id': PERSON_ID, 'name': DATA['owner_name'],
                       'url': BASE + '/', 'sameAs': DATA['scholar_profile_url'],
                       'affiliation': {'@type': 'CollegeOrUniversity', 'name': 'The University of Queensland'}},
        'hasPart': {'@type': 'ItemList', 'name': 'Papers', 'numberOfItems': len(PAPERS),
                    'itemListElement': [{'@type': 'ListItem', 'position': i + 1,
                                         'url': BASE + paper_path(p), 'name': p['title']}
                                        for i, p in enumerate(PAPERS)]},
    }
    entries = '\n'.join(render_entry(p, i == 0) for i, p in enumerate(PAPERS))
    return head('Harjas Sandhu — Mathematics & Scientific Discovery',
                'Papers by and coordinated by Harjas Sandhu, spanning mathematical physics, quantum information and group theory.', '/') + schema_tag(schema) + '''
</head>
<body>
''' + header() + f'''
  <main id="main">
    <section class="intro" aria-labelledby="harjas-sandhu">
      <p class="eyebrow">Mathematics &amp; scientific discovery</p>
      <h1 id="harjas-sandhu">Harjas Sandhu</h1>
      <p class="position">Mathematics student · The University of Queensland</p>
      <div class="bio">
        <p>I study mathematics and Mathematical AI, with an interest in how computation can open new questions in mathematics and the physical sciences.</p>
      </div>
      <div class="intro-links"><a href="#papers">Browse the papers <span aria-hidden="true">↓</span></a><a href="{e(DATA['scholar_profile_url'])}">Google Scholar</a></div>
    </section>

    <section class="section-row papers-section" id="papers" aria-labelledby="papers-heading">
      <span class="legacy-anchor" id="selected-research"></span><span class="legacy-anchor" id="publications"></span>
      <div><h2 id="papers-heading">Papers</h2><p class="section-note">Mathematics, physics<br>and quantum information</p></div>
      <div class="section-copy">
        <details class="paper-folder" open>
          <summary><span class="folder-icon" aria-hidden="true"></span><span>All papers</span><span class="paper-count">{len(PAPERS)}</span></summary>
          <ol class="publication-list">{entries}</ol>
        </details>
      </div>
    </section>

    <section class="section-row" id="about" aria-labelledby="about-heading">
      <span class="legacy-anchor" id="research"></span>
      <h2 id="about-heading">About</h2>
      <div class="section-copy">
        <p>My interests include machine learning, mathematical physics and the use of AI in scientific discovery. I develop and coordinate AI research workflows that explore ideas, test arguments and build on earlier results.</p>
        <p>The papers collected here cover quantum information, the limits of computation and structural questions in mathematics. The group-theory preprint is joint work with Andreas Thom; individual paper pages retain their published authorship and contact roles.</p>
        <p class="about-link"><a href="/acknowledgements/">Acknowledgements and AI use</a></p>
      </div>
    </section>
  </main>
''' + footer()


def render_paper(paper: dict) -> str:
    path = paper_path(paper)
    directory = ROOT / path.lstrip('/')
    action_links = []
    for i, (label, url) in enumerate(resources(paper)):
        css_class = ' class="pdf-link"' if i == 0 else ''
        action_links.append(f'<a{css_class} href="{e(url)}">{e(label)}</a>')
    actions = '\n'.join(action_links)
    if paper.get('license_url'):
        rights = f'<a href="{e(paper["license_url"])}">{e(paper["license_name"])}</a>'
    else:
        rights = e(paper['rights_notice'])
    doi_details = f'<dt>DOI</dt><dd><a href="https://doi.org/{e(paper["doi"])}">{e(paper["doi"])}</a></dd>' if paper.get('doi') else ''
    cite_names = ' and '.join(paper['authors'])
    cite = (e(cite_names) + '. ' if cite_names else '') + f'({paper["publication_date"][:4]}). <cite>{e(paper["title"])}</cite>. Version {e(paper["version"])}.'
    related = ''
    if paper.get('companion'):
        other = next(p for p in PAPERS if p['slug'] == paper['companion']['slug'])
        related = f'<section class="paper-section companion"><h2>Related paper</h2><p>{e(paper["companion"]["description"])}</p><p><a href="{paper_path(other)}">{e(other["title"])}</a></p></section>'
    technical_note = ''
    if paper['slug'] == 'gibbs-uniqueness':
        technical_note = '''<section class="paper-section" aria-labelledby="ideas-heading"><h2 id="ideas-heading">The central construction</h2>
        <p>A finite computation becomes a finite accepting certificate. Exact finite-group cancellation removes invalid histories from the expansion, even though all physical Boltzmann weights remain positive. A valid certificate creates a phase-selection bias; an independent disagreement argument then controls every local physical observable.</p>
        <p>The main construction fixes inverse temperature one and uses only local energies 0, 1 and 20. The alphabet varies effectively with the computation. A separate soft-certificate construction works with the same interaction table at every finite inverse temperature at least 2/5.</p>
        <p>Finite-volume convergence is proved for specified boundary conventions. Exponential clustering of the infinite-volume equilibrium does not assert strong spatial mixing for arbitrary boundaries. Pressure smoothness and perturbation results retain the hypotheses stated in the paper.</p></section>'''
    return head(paper['title'] + ' — Harjas Sandhu', paper['summary'], path, paper) + schema_tag(article_schema(paper)) + f'''
</head>
<body>
''' + header() + f'''
  <main class="paper-main" id="main">
    <p class="breadcrumb"><a href="/#papers">← All papers</a></p>
    <article aria-labelledby="paper-title">
      <header class="paper-header">
        <p class="eyebrow">{e(paper['display_type'])} · {e(paper['subject'])}</p>
        <h1 id="paper-title">{e(paper['title'])}</h1>
        <p class="contact-credit">{credit_line(paper, linked=True)}</p>
        <p class="paper-dates"><time datetime="{paper['publication_date']}">{pretty_date(paper['publication_date'])}</time> · Version {e(paper['version'])}</p>
        <div class="paper-actions"><a class="pdf-link" href="{pdf_path(paper)}">Read PDF</a><a href="#resources">All downloads</a><a href="#citation">Cite</a></div>
      </header>
      <section class="paper-section paper-abstract" aria-labelledby="abstract-heading">
        <h2 id="abstract-heading">Abstract</h2><p class="abstract-text">{e(paper['abstract'])}</p>
      </section>
      {technical_note}
      {render_reader_note(paper)}
      <section class="paper-section" id="resources" aria-labelledby="resources-heading">
        <h2 id="resources-heading">Read and download</h2><div class="paper-actions">{actions}</div>
      </section>
      <section class="paper-section" aria-labelledby="details-heading">
        <h2 id="details-heading">Publication details</h2>
        <dl class="paper-details"><dt>Type</dt><dd>{e(paper['display_type'])}</dd><dt>Repository</dt><dd>{e(paper['publisher'])}</dd>{doi_details}<dt>Version</dt><dd>{e(paper['version'])}</dd><dt>License</dt><dd>{rights}</dd></dl>
      </section>
      <section class="paper-section" id="citation" aria-labelledby="citation-heading">
        <h2 id="citation-heading">Citation</h2><p class="citation-text">{cite}</p>
        <div class="link-line"><a href="{path}citation.bib" download>BibTeX</a><a href="{path}citation.ris" download>RIS</a></div>
      </section>
      {related}
      {acknowledgement(paper)}
    </article>
  </main>
''' + footer()


def main() -> None:
    slugs = [p['slug'] for p in PAPERS]
    assert len(set(slugs)) == len(slugs), 'Duplicate paper'
    for paper in PAPERS:
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', paper['slug'])
        assert bool(paper['authors']) == (paper['credit_role'] == 'author'), 'Author/contact roles must remain explicit'
        directory = ROOT / paper_path(paper).lstrip('/')
        write_page(directory / 'index.html', render_paper(paper))
    write_page(ROOT / 'index.html', render_home())
    ackdir = ROOT / 'acknowledgements'
    ackdir.mkdir(exist_ok=True)
    write_page(ackdir / 'index.html', head('Acknowledgements and AI use — Harjas Sandhu',
               'Acknowledgement of AI assistance in the mathematical development and writing of the papers collected on this website.', '/acknowledgements/') + '</head>\n<body>\n' + header() +
               '<main class="paper-main" id="main"><p class="breadcrumb"><a href="/#papers">← All papers</a></p><h1>Acknowledgements and AI use</h1><p class="acknowledgement-lede">' + e(DATA['ai_acknowledgement']) + '</p><p>Individual paper pages retain their published authorship, contact roles and credits to earlier work. The joint paper with Andreas Thom also records his subsequent work on the proof and exposition.</p></main>' + footer())
    # Preserve the former duplicate address and all downloadable proof files.
    legacy = '/research/catalytic-tensor-conversion/'
    canonical = '/research/exact-catalytic-tensor-restriction/'
    redirect = head('Exact catalytic tensor restriction — Harjas Sandhu',
                    'The paper and its proof are collected under exact catalytic tensor restriction.', canonical)
    write_page(ROOT / legacy.lstrip('/') / 'index.html', redirect + '</head>\n<body>\n' + header() +
               f'<main class="paper-main" id="main"><h1>Exact catalytic tensor restriction</h1><p class="acknowledgement-lede">This paper is now collected on one page.</p><p><a href="{canonical}">Read the paper and proof</a> · <a href="manuscript.md">Expanded proof text</a></p></main>' + footer())
    write_page(ROOT / '404.html', head('Page not found — Harjas Sandhu', 'Return to the papers collection.', '/404.html').replace('content="index,follow,max-snippet:-1,max-image-preview:large"', 'content="noindex,follow"') + '</head>\n<body>\n' + header() + '<main class="error-main" id="main"><h1>Page not found</h1><p><a href="/#papers">Browse all papers</a></p></main>' + footer())
    urls = [BASE + '/'] + [BASE + paper_path(p) for p in PAPERS] + [BASE + '/acknowledgements/']
    (ROOT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{url}</loc></url>\n' for url in urls) + '</urlset>\n')
    (ROOT / 'sitemap.txt').write_text('\n'.join(urls) + '\n')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\nSitemap: {BASE}/sitemap.txt\n')
    print(f'Generated {len(PAPERS)} paper pages, one collection, acknowledgements and sitemaps.')


if __name__ == '__main__':
    main()
