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
        if tag == "img" and "src" in attr:
            self.links.append(attr['src'])
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
    papers = DATA['papers']
    pages = {p.resolve(): Page(p) for p in ROOT.rglob('*.html')}
    home = pages[(ROOT / 'index.html').resolve()]
    revision = hashlib.sha256((ROOT / 'assets/style.css').read_bytes()).hexdigest()[:12]
    check(home.meta.get('google-site-verification') == DATA['google_site_verification'], 'Ownership tag changed')
    link_count = 0
    for path, page in pages.items():
        label = str(path.relative_to(ROOT))
        check(page.stylesheets == ['/assets/style.css?v=' + revision], label + ': stale stylesheet')
        check(page.language == 'en' and page.h1_count == 1, label + ': language/title structure')
        check(not page.duplicate_ids, label + ': duplicate IDs')
        check('width=device-width' in page.meta.get('viewport', ''), label + ': missing viewport')
        check(bool(page.meta.get('description')), label + ': missing description')
        check(len(page.canonical) == 1 and page.canonical[0].startswith(BASE + '/'), label + ': invalid canonical')
        check('main' in page.ids, label + ': missing skip destination')
        for url in page.links:
            result = local_target(url, path)
            if result is None:
                continue
            target, fragment = result
            check(target.is_relative_to(ROOT) and target.is_file(), label + ': missing local target ' + url)
            if fragment and target.suffix == '.html':
                check(fragment in pages[target].ids, label + ': missing fragment ' + url)
            link_count += 1
    check('papers' in home.ids and 'about' in home.ids, 'Unified collection or about section missing')
    html = (ROOT / 'index.html').read_text()
    check(html.count('class="paper-entry"') == len(papers), 'Collection has duplicate or missing papers')
    check('<details class="paper-folder" open>' in html, 'Native accessible collection missing')
    for phrase in ('Selected research', 'Publications &amp; manuscripts', 'About the AI-generated manuscripts'):
        check(phrase not in html, 'Legacy categorisation remains: ' + phrase)
    check(len(set(p['title'] for p in papers)) == len(papers), 'Duplicate paper titles')
    ack = DATA['ai_acknowledgement']
    for paper in papers:
        route = '/' + paper['collection'] + '/' + paper['slug'] + '/'
        directory = ROOT / route.lstrip('/')
        page = pages[(directory / 'index.html').resolve()]
        text = ' '.join(page.text)
        check(route in home.links, paper['slug'] + ': not linked from collection')
        check(paper['summary'] in ' '.join(home.text), paper['slug'] + ': missing synopsis')
        check(page.canonical == [BASE + route], paper['slug'] + ': wrong canonical')
        check(page.meta['description'] == paper['summary'], paper['slug'] + ': wrong search description')
        check(not re.search(r'\b(AI|GPT|files?|downloads?|provenance)\b', paper['summary'], re.I), 'Description contains administrative material')
        check(page.meta['citation_title'] == paper['title'], paper['slug'] + ': scholarly title mismatch')
        check(page.meta['citation_pdf_url'] == BASE + route + paper['pdf_filename'], paper['slug'] + ': PDF URL mismatch')
        check(page.meta['citation_publication_date'] == paper['publication_date'].replace('-', '/'), 'Publication date mismatch')
        check(page.meta_values.get('citation_author', []) == paper['authors'], 'Author metadata changed')
        check(page.meta_values.get('DC.creator', []) == paper['authors'], 'Dublin Core author metadata changed')
        check(ack in text and text.count(ack) == 1, paper['slug'] + ': common acknowledgement missing or duplicated')
        check(paper['abstract'] in text, paper['slug'] + ': abstract changed')
        raw = (directory / 'index.html').read_text()
        for anchor, key in [('result','result'),('method','mechanism'),('scope','scope')]:
            check(anchor in page.ids, paper['slug'] + ': missing reader section ' + anchor)
            check(len(paper['reader_overview'][key]) >= 1, 'Empty reader explanation')
            for paragraph in paper['reader_overview'][key]:
                check(paragraph in text, paper['slug'] + ': reader explanation missing')
        check('<summary id="abstract-heading">Technical abstract</summary>' in raw, 'Technical abstract disclosure missing')
        check(raw.index('id="result"') < raw.index('id="method"') < raw.index('id="scope"') < raw.index('id="abstract"'), 'Inconsistent reader section order')
        check(raw.index('id="abstract-heading"') < raw.index('id="resources"') < raw.index('id="acknowledgements"'), 'Acknowledgement must follow mathematical content and resources')
        check(paper['summary'] not in ack, 'Description corrupted')
        article = next(s for s in page.schema if s.get('@type') == 'ScholarlyArticle')
        check(article['abstract'] == paper['abstract'], 'Schema abstract mismatch')
        check(article['encoding']['contentUrl'] == page.meta['citation_pdf_url'], 'Schema PDF mismatch')
        check([p['name'] for p in article.get('author', [])] == paper['authors'], 'Schema invents or removes authors')
        check(article['creditText'] == ack, 'Schema AI acknowledgement mismatch')
        if paper.get('doi'):
            check(page.meta.get('citation_doi') == paper['doi'], 'DOI mismatch')
            check(article['identifier']['value'] == paper['doi'], 'Schema DOI mismatch')
        for filename, key in [(paper['pdf_filename'], 'pdf'), ('citation.bib', 'bib'), ('citation.ris', 'ris')]:
            body = (directory / filename).read_bytes()
            check(hashlib.sha256(body).hexdigest() == paper[key + '_sha256'], paper['slug'] + ': altered asset ' + filename)
            if key == 'pdf':
                check(body.startswith(b'%PDF-') and len(body) == paper['pdf_bytes'], 'Invalid PDF')
        for asset in paper.get('assets', []):
            body = (directory / asset['filename']).read_bytes()
            check(len(body) == asset['bytes'] and hashlib.sha256(body).hexdigest() == asset['sha256'], 'Preserved release asset changed: ' + asset['filename'])
        if paper.get('source_filename'):
            with zipfile.ZipFile(directory / paper['source_filename']) as archive:
                check(archive.testzip() is None, 'Source archive CRC failed')
                check(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in archive.namelist()), 'Unsafe ZIP member')
        if paper.get('companion'):
            other = next(p for p in papers if p['slug'] == paper['companion']['slug'])
            check('/' + other['collection'] + '/' + other['slug'] + '/' in page.links, 'Missing companion link')
    group = next(p for p in papers if p['slug'] == 'non-sofic-hyperbolic-group')
    check(group['authors'] == ['Harjas Sandhu', 'Andreas Thom'], 'Published coauthorship must remain intact')
    group_page = pages[(ROOT / 'publications/non-sofic-hyperbolic-group/index.html').resolve()]
    check(group['acknowledgement_note'] in ' '.join(group_page.text), 'Coauthor contribution clarification missing')
    icon = (ROOT / 'assets/favicon.svg').read_text()
    ET.fromstring(icon)
    check('<text' not in icon, 'Favicon should use the geometric site mark')
    check((ROOT / 'favicon.ico').read_bytes().startswith(b'\x00\x00\x01\x00'), 'ICO fallback invalid')
    for filename in ('favicon-32.png', 'apple-touch-icon.png'):
        check((ROOT / 'assets' / filename).read_bytes().startswith(b'\x89PNG'), 'PNG icon fallback invalid')
    icon_revision = hashlib.sha256((ROOT / 'assets/favicon.svg').read_bytes()).hexdigest()[:12]
    for page_path in pages:
        check('/assets/favicon.svg?v=' + icon_revision in page_path.read_text(), 'Stale favicon URL')
    urls = [node.text for node in ET.parse(ROOT / 'sitemap.xml').getroot().findall('{*}url/{*}loc')]
    expected = [BASE + '/'] + [BASE + '/' + p['collection'] + '/' + p['slug'] + '/' for p in papers] + [BASE + '/acknowledgements/']
    check(urls == expected and len(set(urls)) == len(urls), 'Sitemap missing canonical pages or includes duplicates')
    check((ROOT / 'sitemap.txt').read_text().splitlines() == urls, 'Text sitemap mismatch')
    for url in urls:
        check(local_target(url, ROOT / 'index.html')[0] in pages, 'Broken sitemap target')
    check((ROOT / '.nojekyll').is_file(), 'Missing .nojekyll')
    print(f'Checked {len(pages)} HTML pages, {len(papers)} unique papers and {link_count} local links; metadata, acknowledgements, PDF/citation integrity and source archives passed.')


if __name__ == '__main__':
    main()
