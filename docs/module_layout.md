# Recommended Module Layout

This document proposes how the repository can be organized as implementation grows. The goal is to keep Aim 1, Aim 2, and Aim 3 responsibilities separate while preserving a simple developer workflow.

## Proposed Python package layout

```text
src/postgram/
├── __init__.py
├── __main__.py
├── cli.py
├── config.py
├── dataset.py
├── schemas/
│   ├── manifest.py
│   ├── transcript.py
│   ├── intervals.py
│   └── labels.py
├── ingest/
│   ├── ensembl.py
│   ├── localization.py
│   ├── rbp.py
│   ├── mirna.py
│   └── structure.py
├── normalize/
│   ├── ids.py
│   ├── coordinates.py
│   ├── scores.py
│   └── provenance.py
├── features/
│   ├── channels.py
│   ├── tensorize.py
│   ├── tokenization.py
│   └── splits.py
├── modeling/
│   ├── datamodule.py
│   ├── transformer.py
│   ├── heads.py
│   ├── losses.py
│   └── train.py
├── evaluation/
│   ├── metrics.py
│   ├── robustness.py
│   └── reports.py
├── interpretation/
│   ├── attributions.py
│   ├── windows.py
│   ├── profiles.py
│   ├── rules.py
│   └── summaries.py
└── io/
    ├── jsonl.py
    ├── parquet.py
    └── artifacts.py
```

## Responsibilities by package

### `schemas/`

Owns the typed internal contracts. This is where we define what a transcript record, label set, or interval feature means in code.

### `ingest/`

Owns raw-source parsing. One source family per module is a good default because it keeps source-specific quirks isolated.

### `normalize/`

Owns cleanup and harmonization logic. This layer should resolve IDs, coordinates, scoring scales, and metadata consistency before the data reaches model-facing code.

### `features/`

Owns the conversion from biological records to model inputs. This is where sequence tokenization, aligned annotation channels, padding, masking, and split generation belong.

### `modeling/`

Owns Aim 2 model code. It should be possible to swap baselines here without changing the Aim 1 data model.

### `evaluation/`

Owns metrics, held-out evaluation, and robustness checks. Keeping this separate helps avoid mixing training logic with reporting logic.

### `interpretation/`

Owns Aim 3 outputs. This is where attribution extraction, motif-centered windows, rule mining, and textual summaries should live.

### `io/`

Owns file formats and artifact writing, so data persistence logic stays out of biological and modeling modules.

## Suggested CLI growth

The current CLI is small and that is good. It can expand along clear subcommands:

- `init-config`
- `validate-manifest`
- `summarize-dataset`
- `ingest-*`
- `build-dataset`
- `build-features`
- `train-localization`
- `evaluate-localization`
- `export-attributions`
- `summarize-localization`

## Suggested test layout

```text
tests/
├── test_config.py
├── test_dataset.py
├── test_cli.py
├── test_ingest_ensembl.py
├── test_ingest_localization.py
├── test_normalize_ids.py
├── test_feature_tensorize.py
├── test_model_train.py
├── test_evaluation_metrics.py
└── test_interpretation_profiles.py
```

## Recommended implementation order

1. `schemas/`
2. `ingest/`
3. `normalize/`
4. `features/`
5. `modeling/`
6. `evaluation/`
7. `interpretation/`
