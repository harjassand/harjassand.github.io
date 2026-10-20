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

On 21 October 2026, Harjas explicitly corrected the earlier contact-only
attribution and confirmed that he is the author. The website names him as
author and manuscript contact and describes his development and coordination
of the agentic system. The dated correction is separate from the verbatim
original manuscript disclosure. Original PDFs and citation exports remain
unchanged; their earlier contact-only wording is disclosed rather than hidden.
AI-developed results and proofs and pending independent review remain explicit.

For the two quantum papers, downloaded BibTeX files reproduce the Zenodo exports without modification.
Their RIS files reproduce DOI content negotiation through the DOI citation service
without modification. The exports identify
the repository creator as `Sandhu, Harjas`. Each citation section explains the
dated author correction and the historical wording in the original PDFs.

The joint Sandhu–Thom paper has a separate page at
`/publications/non-sofic-hyperbolic-group/`. Both authors, the abstract,
17 October 2026 arXiv posting date, version and CC BY 4.0 license follow
https://arxiv.org/abs/2610.24836. Its unchanged eight-page PDF comes from
https://arxiv.org/pdf/2610.24836v1; SHA-256 is recorded and checked.
The acknowledgments excerpt and drafting-disclosure summary retain the
AI provenance and the different contributions. Its BibTeX/RIS downloads were
prepared from the public arXiv metadata rather than claimed as source exports.
The hosted commentary listed on Andreas Thom's Scholar profile with the date
13 October is linked as another version of the same work. No new arXiv
submission, manuscript alteration, or claim of independent proof certification
is involved in this website addition.

No academic qualification beyond current University of Queensland mathematics
student status is asserted. No institutional endorsement, peer review,
independent verification, or priority assessment is asserted.

## Indexing scope and attribution correction

Each landing page contains canonical and Open Graph tags, title, publication
date, direct local PDF URL, DOI, abstract URL, language, Dublin Core identifiers,
and JSON-LD `ScholarlyArticle` data. The home page contains `Person` and
`ProfilePage` structured data. A sitemap and permissive robots file support
discovery. PDFs are searchable deposited documents.

For the two quantum papers, `citation_author`, `DC.creator` and JSON-LD `author` reflect Harjas's explicit
authorship correction. Author names also appear visibly below every title.
The original quantum PDFs still contain their earlier contact-only footnote; the dated
landing-page correction explains that historical wording and retains the full
AI disclosure. This is an attribution update, not independent verification of
proofs or priority, and does not establish Google Scholar inclusion. No ORCID
or qualification is invented, and no new manuscript version is published.

Reference: https://scholar.google.com/intl/en/scholar/inclusion.html

Static checks and successful hosting confirm implementation and availability.
They do not confirm Google Search or Google Scholar indexing; that requires
separate observation after crawling.

The sitemap deliberately lists the homepage and three canonical publication HTML URLs. The original
PDFs remain reachable through ordinary HTML links and `citation_pdf_url`;
alternate `/index.html` addresses are not added to the sitemap. GitHub Pages
sets the PDF HTTP headers, so an `_headers` file or HTML meta tag cannot add
an HTTP canonical header to a PDF on this host.

The generator also creates `sitemap.txt`, Google's supported plain-text format,
from the same canonical URL list. Both formats are declared in `robots.txt`.
The text version provides an alternative submission while the XML submission
has an unresolved Search Console fetch report despite successful live fetching.
The validator checks that the two formats contain identical URLs. Neither a
valid sitemap nor a submission acknowledgement confirms Google has processed
the sitemap or indexed its pages.
