# PostGram Flowcharts

These flowcharts now follow the pasted project description more closely. The first one is the end-to-end architecture. The second one zooms in on the modeling pipeline.

## End-to-end pipeline

```mermaid
flowchart TD
    A[Project brief and localization questions] --> B[Define manifest and task scope]
    B --> C[Collect raw sources]

    C --> C1[Ensembl transcripts and 3UTRs]
    C --> C2[APEX-seq and fractionation labels]
    C --> C3[RBP annotations and eCLIP]
    C --> C4[miRNA interaction resources]
    C --> C5[RNA structure from RNAfold]

    C1 --> D[Normalize IDs coordinates and provenance]
    C2 --> D
    C3 --> D
    C4 --> D
    C5 --> D

    D --> E[Build transcript-centered records]
    E --> F[Attach position-aligned feature channels]
    F --> G[Validate dataset and inspect coverage]

    G --> H[Build model-ready tensors]
    H --> I[Train localization model]
    I --> J[Evaluate held-out performance]
    J --> K[Cross-dataset robustness checks]

    I --> L[Export predictions hidden states and attributions]
    L --> M[Generate profile summaries]
    M --> N[Interpret localization-associated patterns]
    N --> O[Refine data features and model design]
    O --> E
```

## Aim 2 modeling pipeline

```mermaid
flowchart LR
    A[Processed transcript records] --> B[Tokenize 3UTR sequence]
    B --> C[Add annotation channels]
    C --> C1[RBP channels]
    C --> C2[miRNA channels]
    C --> C3[Structure channels]
    C1 --> D[Tensor builder]
    C2 --> D
    C3 --> D

    D --> E[Batching padding masking]
    E --> F[Transformer encoder]
    F --> G[Global pooling]
    G --> H[Localization task heads]

    H --> I1[P-body vs non-P-body]
    H --> I2[Stress granule vs non-stress]

    I1 --> J[Loss and optimization]
    I2 --> J
    J --> K[Checkpoint selection]
    K --> L[Held-out metrics]
    L --> M[Robustness slices]
    M --> N[Export predictions and attribution inputs]
```

## Reading the flow

- The end-to-end diagram shows how Aim 1 outputs become Aim 2 inputs and eventually feed Aim 3 interpretation.
- The Aim 2 diagram focuses on the tensorization and Transformer training path.
- The feedback loop is intentional: interpretation should help refine data channels and model choices rather than sit outside the pipeline.
