# Harjas Sandhu — research website

A static, accessible GitHub Pages site at https://harjassand.github.io/.
The homepage has one expandable **Papers** collection, ordered by date, and an
About section. No JavaScript or framework is required.

## Edit and build

`data/publications.json` is the catalogue. Add a paper there and place its PDF,
BibTeX, RIS and optional source archive in its existing publication directory.
Each record explicitly identifies its published authors or separate contact /
coordination role. Do not infer scientific authorship from repository metadata.

```sh
python3 tools/build_site.py
python3 tools/check_site.py
python3 -m http.server 8765
```

The builder produces all HTML, canonical URLs, scholarly metadata, JSON-LD and
sitemaps. Native HTML disclosure controls provide the expandable collection and
remain keyboard accessible without JavaScript. CSS is revisioned by content hash.
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
