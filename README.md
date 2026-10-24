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
The generator fingerprints the stylesheet URL so returning browsers receive
new styles when a release changes CSS, without relying on a manual cache reset.
The full abstract precedes dates and download controls so readers and crawlers
can reach it immediately. Existing OpenAIRE and OpenAlex catalogue records
are linked; these are discovery records rather than peer-review endorsements.

The home page's Search Console ownership tag is generated from
`google_site_verification` in `data/publications.json`. Keep that value and
the tag when rebuilding; removing either can invalidate ownership verification.
The public tag is specific to this website and is intended to be published.

`scholar_profile_url` links the public Google Scholar profile from every page's
footer and from the homepage's `Person.sameAs` metadata. The profile links back
to this website. These links connect the public research pages; they do not
establish inclusion of any manuscript in Scholar search.

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

The two quantum manuscripts credit Harjas solely as contact. His contribution
was developing and coordinating the agentic system. The website follows that
role, reproduces the original AI disclosure and does not name him as a scientific
author. Their title-page disclosures are authoritative for these roles.
AI-developed results and proofs and pending independent review remain explicit.

For the two quantum papers, downloaded BibTeX files reproduce the Zenodo exports without modification.
Their RIS files reproduce DOI content negotiation through the DOI citation service
without modification. The exports identify
the repository creator as `Sandhu, Harjas`. Each citation section explains the
difference between repository creator metadata and the manuscript's scientific
authorship. The visible reference is title-first, while source exports remain
unchanged for traceability.

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

## Publication data and generation

`data/publications.json` lists papers in display order. Every paper explicitly
declares its `authors`, `credit_role`, subject, publisher, license and source of
abstract/citation data. The site owner is not used as an author fallback.
Contact-only manuscripts have an empty author list and a separate `contact_name`
and contribution statement. A companion relationship is optional and identifies
the other paper by slug; `cites` distinguishes a directed citation from a
related-work link. There are no hard-coded record IDs or required paper count.

A shared renderer produces the three publication pages and their structured
metadata. The generator validates unique slugs/DOIs, explicit roles and companion
targets before writing pages. To add a paper, supply its metadata and checked
PDF/citation files in its publication directory. Keep source hashes intact.

`selected_research` is a separate collection in the same JSON file. It adds a
small homepage section without changing the order or attribution of formal
publications. A research record declares `collection: "research"`, a unique
slug, explicit roles and original asset hashes. Both collections use the same
homepage-entry and manuscript-page renderers: credit, dates and access links,
abstract, contribution and provenance, publication details, and citation.
An optional `reader_note_template` adds a manuscript-specific explanation after
these shared sections; it does not replace the page shell. The shared head,
navigation, structured metadata and sitemap support both collections. A DOI
must resolve to a published record before it is linked.

The amplifier manuscript lives at `/research/amplifier-entropy/`. Its 33-page
PDF and complete 22-file source ZIP are the original 21 October 2026 files.
The page distinguishes the proof candidate from established results, reproduces
the acknowledgment after the abstract and credits Harjas for developing and
coordinating the agentic research system. Scientific authors remain empty. The source
LICENSE and NOTICE retain their scope for incorporated OpenAI material; no new
license over the complete manuscript is asserted.

Its published record is https://zenodo.org/records/23526644, with version DOI
https://doi.org/10.5281/zenodo.23526644. The title-first BibTeX/RIS downloads now
use that permanent DOI. Zenodo credits Harjas Sandhu as the record creator;
the manuscript's scientific authorship and AI disclosure remain distinct.
The immutable Git copy remains available for byte-level version comparison.
The website release package and manifest include the updated DOI citations.
Files already archived on Zenodo retain their original pre-DOI citation snapshot.
For a later version, verify its live DOI before updating the reference, then
rebuild the manifest and release ZIP with fresh hashes. Do not amend a published
source snapshot or silently replace an earlier cited PDF.

`tools/check_site.py` checks links, fragments, exact abstracts and disclosures,
PDF/citation hashes, author versus contact/coordinator metadata, companion citation
direction, exact source abstract and notices, source/release ZIP integrity,
canonical URLs, navigation and identical XML/text sitemaps. It intentionally
does not rewrite manuscript or citation assets.

## Indexing scope and attribution

Each landing page contains canonical and Open Graph tags, title, publication
date, direct local PDF URL, abstract URL, language, Dublin Core identifiers,
and JSON-LD `ScholarlyArticle` data. The home page contains `Person` and
`ProfilePage` structured data. A sitemap and permissive robots file support
discovery. PDFs have extractable text. DOI tags appear only for published records.

The coauthored arXiv paper has a separate `citation_author` and `DC.creator` tag
for each verified author, matching its visible credit, citation downloads and
JSON-LD author list. Its local searchable PDF is linked from the abstract page
in the same directory. The posting date follows arXiv, distinct from the date
printed in the manuscript and the earlier hosted commentary.

For the two contact-only quantum manuscripts, `citation_author`, `DC.creator`
and JSON-LD `author` are omitted. `DC.contributor`, JSON-LD `contributor` and
visible text describe Harjas's actual role. Google Scholar requires an actual
author tag; these pages cannot honestly satisfy that requirement by relabeling
a contact. This limits their Scholar metadata eligibility, while ordinary web
discovery remains possible. No ORCID, qualification or independent verification
is invented, and no new manuscript version is published.

The amplifier manuscript follows the same attribution rule: it has contributor
metadata, no scientific-author tags, and both its published version DOI and PDF
SHA-256 in structured data. This supports ordinary web discovery but does not satisfy
Scholar's actual-author requirement. Its source attribution is represented with
`isBasedOn`; the inherited source license is not assigned to the entire article.

Reference: https://scholar.google.com/intl/en/scholar/inclusion.html

Static checks and successful hosting confirm implementation and availability.
They do not confirm Google Search or Google Scholar indexing; that requires
separate observation after crawling.

The sitemap deliberately lists the homepage, three canonical publication HTML URLs
and the selected-research manuscript page. The original
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

## Research proof-candidate notes (2026-10-24)

The site also hosts a standalone AI-generated mathematics proof-candidate reading edition at `/research/exact-catalytic-tensor-restriction/`, concerning Astra result N680. It includes a full HTML text, a PDF reading edition, the originating AI proof narrative and title-first citation. No scientific mathematical authorship, external review, DOI, or validated historic-priority claim is asserted. The `research_notes` records in `data/publications.json` are rendered on the home page through `tools/build_site.py`; the publication/manuscript assets already present on the site remain unchanged.
