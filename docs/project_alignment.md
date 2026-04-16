# Project Alignment

This repository is now aligned against the project text you provided directly in chat. That lets the docs be much more specific about scope, data contracts, and the intended modeling path.

## Aim 1

Aim 1 is the data foundation for localization-aware modeling of post-transcriptional regulation.

In repo terms, it means:

- retrieve curated human transcript annotations and sequences
- focus initially on 3'UTRs as the main regulatory integration region
- assemble RBP, miRNA, and RNA-structure features
- attach experimentally derived localization labels
- produce a structured, machine-learning-ready dataset with retained provenance

The most important design point from the project text is that features should be position-aligned along each transcript or 3'UTR rather than collapsed too early into simple counts.

Current repo support:

- manifest definition
- transcript JSONL validation
- basic CLI utilities

Planned Aim 1 extension:

- source-specific ingestion adapters
- harmonization of transcript IDs and coordinates
- per-position feature channel construction
- export of standardized processed datasets and metadata

## Aim 2

Aim 2 is the predictive modeling layer.

Based on the project text, the preferred baseline is:

- a Transformer encoder over 3'UTR sequence plus aligned annotation channels
- transcript-level pooling
- localization prediction heads

The first concrete tasks remain:

- `p_body_vs_non_p_body`
- `stress_granule_vs_non_stress`

The evaluation expectations are now clearer too:

- held-out transcript evaluation
- cross-dataset robustness when multiple sources exist
- analysis across transcript length, annotation density, and feature composition

## Aim 3 handoff

Aim 3 is not implemented yet, but the architecture now explicitly reserves outputs that it will need:

- transcript-level predictions
- hidden states or pooled embeddings
- attribution maps
- metadata-rich feature summaries

That should prevent Aim 2 from becoming a black box that is hard to interpret later.

## Scope of the current repo pass

This pass does not implement the full pipeline yet. It does:

- align docs to the provided project text
- expand the flowcharts into architecture-oriented diagrams
- define a recommended code layout for Aim 1, Aim 2, and the Aim 3 handoff

## Related docs

- `docs/architecture.md`
- `docs/flowchart.md`
- `docs/module_layout.md`
