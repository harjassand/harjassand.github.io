# Harjas Sandhu — personal research website

A small, buildless academic website for `https://harjassand.github.io/`.
The repository root is ready for GitHub Pages. There is no framework,
dependency installation, analytics, external font, or runtime JavaScript.

## Preview and maintain

From this directory, use a working Python 3 interpreter:

```sh
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/`. The checked-in HTML is served directly.
To change text or metadata, edit `data/publications.json` or
`tools/build_site.py`, then regenerate and check:

```sh
python3 tools/build_site.py
python3 tools/check_site.py
```

The PDF and citation files are not rewritten by generation. Publication
landing pages, their PDFs, and citation downloads share a directory.
Each paper has its own stable URL and full visible abstract. Navigation,
abstracts, PDF links, and citations work without JavaScript.
The full abstract precedes dates and download controls so readers and crawlers
can reach it immediately. Existing OpenAIRE and OpenAlex catalogue records
are linked; these are discovery records rather than peer-review endorsements.

The home page's Search Console ownership tag is generated from
`google_site_verification` in `data/publications.json`. Keep that value and
the tag when rebuilding; removing either can invalidate ownership verification.
The public tag is specific to this website and is intended to be published.

## Deployment

Use the public repository `harjassand/harjassand.github.io`, enable GitHub
Pages from `main` at `/ (root)`, and retain `.nojekyll`. All canonical and
scholarly URLs target `https://harjassand.github.io/`. If the domain changes,
change `base_url` in `data/publications.json`, regenerate, then verify live
links and update any repository cross-references.

## Sources and attribution

Metadata was retrieved from the public Zenodo records on 21 October 2026:

- https://zenodo.org/records/23349086
- https://zenodo.org/records/23349192

The exact abstracts and contact/provenance disclosure come from the deposited
manuscripts. Both manuscripts are dated 11 October 2026, while the Zenodo
publication date is 14 October 2026. Original PDF bytes and SHA-256 hashes
are retained; the check script verifies them. The existing Apache-2.0
manuscript licenses are identified without relicensing any manuscript.

Downloaded BibTeX files reproduce the Zenodo exports without modification.
RIS files reproduce DOI content negotiation through the DOI citation service
without modification. The exports identify
the repository creator as `Sandhu, Harjas`. Each citation section explicitly
distinguishes this from the contact-only role in the manuscripts.

No academic qualification beyond current University of Queensland mathematics
student status is asserted. No institutional endorsement, peer review,
independent verification, or priority assessment is asserted.

## Indexing scope and unresolved author requirement

Each landing page contains canonical and Open Graph tags, title, publication
date, direct local PDF URL, DOI, abstract URL, language, Dublin Core identifiers,
and JSON-LD `ScholarlyArticle` data. The home page contains `Person` and
`ProfilePage` structured data. A sitemap and permissive robots file support
discovery. PDFs are searchable deposited documents.

`citation_author` and structured-data `author` are deliberately omitted.
The manuscripts explicitly identify Harjas Sandhu solely as contact person,
and the Google Scholar inclusion guidance requires the author field to
contain actual authors only. Repository creator metadata does not establish
that scientific-author role. Full Google Scholar author-metadata compliance
cannot be claimed while that discrepancy remains. Do not insert an author,
institutional author affiliation, or ORCID to obtain indexing unless the
underlying authorship is verified and the user approves any manuscript change.

Reference: https://scholar.google.com/intl/en/scholar/inclusion.html

Static checks and successful hosting confirm implementation and availability.
They do not confirm Google Search or Google Scholar indexing; that requires
separate observation after crawling.

The sitemap deliberately lists the three canonical HTML URLs. The original
PDFs remain reachable through ordinary HTML links and `citation_pdf_url`;
alternate `/index.html` addresses are not added to the sitemap. GitHub Pages
sets the PDF HTTP headers, so an `_headers` file or HTML meta tag cannot add
an HTTP canonical header to a PDF on this host.
