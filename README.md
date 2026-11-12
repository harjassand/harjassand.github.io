# Harjas Sandhu — research website

A static, accessible GitHub Pages site at https://harjassand.github.io/.
The homepage has one **Papers** collection, ordered by date, and an About section.
A compact search field and topic dropdown filter the catalogue locally; a sort
menu selects newest first (the default), oldest first or title A–Z. Clearing
filters preserves the selected sort order. The static build also orders by date. The small
`assets/papers.js` enhancement uses no dependencies, trackers or network requests;
without JavaScript, every paper and its native disclosure remain accessible.

## Edit and build

`data/publications.json` is the catalogue. Add a paper there and place its PDF,
BibTeX, RIS and optional source archive in its existing publication directory.
Each record uses `browse_topics` for the topic menu and explicitly identifies its published authors or separate contact /
coordination role. Do not infer scientific authorship from repository metadata.

```sh
python3 tools/build_site.py
python3 tools/check_site.py
python3 -m http.server 8765
```

The builder produces all HTML, canonical URLs, scholarly metadata, JSON-LD and
sitemaps. Native HTML disclosure controls provide the expandable collection and
remain keyboard accessible without JavaScript. Search matches title, summary,
technical abstract, keywords and credited names, using all query words together.
The topic filter combines with search; a live count and clear control expose the
current result state. CSS is revisioned by content hash.
The checker validates local links and anchors, metadata, unique catalogue entries,
consistent acknowledgements and manuscript / citation hashes. It also checks the
preserved amplifier release assets and source archive integrity. These are site
implementation checks, not verification of the mathematical claims or indexing.

## Editorial conventions

Paper descriptions explain the mathematical result and its scope. Resources,
citations and acknowledgements are separate sections. All paper pages use the
shared `ai_acknowledgement` field near their end. For the joint paper with Andreas
Thom, an additional sentence identifies his later work on the proof and exposition;
the published coauthor list is retained. Original deposited PDFs and existing
citation exports are unchanged. Credits to prior work and inherited licence
notices are retained.

The Gibbs paper is hosted locally with its LaTeX manuscript and source archive,
and links to the versioned Zenodo DOI 10.5281/zenodo.23983514. Its main fixed
inverse-temperature-one construction and its distinct soft-certificate temperature
extension are identified separately. No arbitrary-boundary strong spatial mixing
claim is introduced.

The catalytic tensor work has one catalogue entry at
`/research/exact-catalytic-tensor-restriction/`. Its substantive proof explanation
is preserved in `tools/templates/catalytic-tensor-notes.html.in`; original and
expanded derivations remain downloadable. The older
`/research/catalytic-tensor-conversion/` address points readers to that entry and
retains its Markdown source. Older homepage anchors are also preserved.

The amplifier reader explanation remains in
`tools/templates/amplifier-entropy-notes.html.in`. The source bundle's LICENSE,
NOTICE.txt and bibliography are preserved byte for byte. Existing scientific
scope boundaries are retained in its explanation.

Deploy by publishing the generated tree to the repository's configured GitHub
Pages branch. No analytics, third-party fonts or client-side trackers are used.

## Research connections and homepage

`research_intro` contains the research-first introduction. `research_connections`
defines the expandable reading groups and the connected-paper lists on individual
pages. Each group names its papers by existing slug, with a short link label and
an explanation of the relationship. Use explicit dependencies only when documented;
keep thematic connections, different invariants and proposed constructions clear.
Every paper remains one entry in the searchable catalogue. The contact invitation
uses the published professional address in `contact_email`. No research-process
section has been added; the existing acknowledgements are retained.

## Reading format and site mark

Each paper uses a short result-focused summary followed by the same three sections:
The result, How the argument works, and Scope. Their text lives in each record's
`reader_overview`. Original technical abstracts and longer existing explanations
are retained in native expandable sections. Changes to this editorial text do not
rewrite any deposited manuscript.

The geometric linked-diamond mark is defined in `assets/favicon.svg` and is used
in the header and browser tab. Its URL is revisioned to refresh cached icons.
The ICO, 32-pixel PNG and Apple touch icon cover browser fallbacks. To regenerate
the raster icons after changing the matching vector geometry, run
`python3 tools/build_favicons.py` with Pillow installed. Ordinary site builds need
only Python's standard library.
