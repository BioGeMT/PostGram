# PostGram

PostGram is a research scaffold for modeling post-transcriptional regulation in transcript 3'UTRs with an explicit focus on RNA localization. The repository is now organized around the project text provided for the three aims, with immediate implementation emphasis on Aim 1 and Aim 2:

- Aim 1: collect, normalize, and inspect transcript-centered evidence for localization-linked regulation
- Aim 2: turn that representation into baseline predictive tasks for P-body and stress-granule biology
- Aim 3: prepare interpretable outputs and handoffs for downstream explainability tooling

The codebase is intentionally still lightweight. It gives us a clean place to define manifests, validate transcript records, and document the data-to-model pipeline before we add heavier ingestion and training code.

## What is in the repo

- A small `src/`-based Python package with a CLI
- A TOML manifest format for declaring tasks and upstream evidence sources
- A JSONL transcript record format for localization-aware examples
- Example config and example dataset files
- Unit tests for config loading, dataset validation, and CLI behavior
- Aim-aligned project docs and a first pipeline flowchart

## Quick start

```bash
PYTHONPATH=src python3 -m postgram init-config configs/local.toml
PYTHONPATH=src python3 -m postgram validate-manifest configs/project.example.toml
PYTHONPATH=src python3 -m postgram summarize-dataset examples/sample_transcripts.jsonl
```

If you prefer an editable install:

```bash
pip install -e .
python3 -m postgram summarize-dataset examples/sample_transcripts.jsonl
```

## Current structure

```text
PostGram/
├── configs/
│   └── project.example.toml
├── docs/
│   ├── flowchart.md
│   ├── project_alignment.md
│   └── roadmap.md
├── examples/
│   └── sample_transcripts.jsonl
├── src/postgram/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── config.py
│   └── dataset.py
└── tests/
```

## Working interpretation of Aim 1 and Aim 2

Aim 1 in this repo means building a transcript-level reference table that can combine sequence, localization labels, and post-transcriptional evidence layers into one inspectable object. The immediate data themes are:

- transcript references and 3'UTR sequences
- localization evidence for P-bodies and stress granules
- regulatory tracks from RBPs, miRNAs, and motif-centric annotations

Aim 2 means converting those transcript records into reproducible baseline learning tasks. The first contrasts already represented in the manifest are:

- `p_body_vs_non_p_body`
- `stress_granule_vs_non_stress`

## Manifest format

The manifest describes scope, tasks, and the upstream evidence expected for a project run.

```toml
project_name = "PostGram"
species = "homo_sapiens"
release = "draft-aim1-aim2"
tasks = ["p_body_vs_non_p_body", "stress_granule_vs_non_stress"]
output_dir = "outputs"

[[sources]]
name = "ensembl_transcripts"
kind = "reference"
path = "data/raw/ensembl/transcripts.fa"
description = "Transcript annotations and 3'UTR-aware sequence reference"
```

## Transcript dataset format

Each line in the dataset is a JSON object with:

- `transcript_id`
- `gene_name`
- `sequence`
- `labels`: localization labels or probabilities
- `feature_tracks`: summarized regulatory evidence attached to that transcript

Example:

```json
{
  "transcript_id": "ENST00000372836",
  "gene_name": "ELAVL1",
  "sequence": "AUGGCUAUGCUA",
  "labels": {
    "p_body_enriched": true,
    "stress_granule_enriched": false,
    "cytosol_probability": 0.72
  },
  "feature_tracks": [
    {
      "name": "eclip_binding_sites",
      "source": "ENCODE",
      "kind": "intervals",
      "count": 5
    }
  ]
}
```

## Project docs

- [Aim alignment](docs/project_alignment.md)
- [Architecture](docs/architecture.md)
- [Roadmap](docs/roadmap.md)
- [Flowchart](docs/flowchart.md)
- [Module layout](docs/module_layout.md)

## Next implementation steps

- Add ingestion adapters for transcript references, localization assays, RBP binding data, and miRNA interaction resources
- Add featurization that converts transcript records into model-ready matrices or tensors
- Add reproducible baseline train/evaluate loops for the two initial localization tasks
- Add interpretation and reporting modules after the first baseline is stable
