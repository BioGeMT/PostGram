# Roadmap


## Aim 1: Data collection and representation

Current repository support:

- standard TOML manifests for declaring data sources and tasks
- transcript-level JSONL records with localization labels and regulatory feature summaries
- validation and inspection tools through the CLI

Next additions:

- ingestion adapters for transcript references and 3'UTR sequences
- importers for localization evidence linked to P-bodies and stress granules
- importers for RBP binding, miRNA interactions, and motif annotations
- harmonization rules for transcript identifiers, gene names, and evidence provenance

## Aim 2: Predictive modeling

Current repository support:

- the first baseline tasks are already named in config validation:
  - `p_body_vs_non_p_body`
  - `stress_granule_vs_non_stress`

Next additions:

- featurization from transcript JSONL records into model-ready matrices or tensors
- reproducible split generation
- baseline train/evaluate loops
- experiment tracking for metrics, feature sets, and release tags

## Interpretation handoff

Interpretation is not the focus of this pass, but Aim 2 should leave clean outputs for it:

- transcript-level prediction tables
- feature importance or attribution summaries
- comparison reports across evidence combinations
