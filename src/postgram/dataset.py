from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class FeatureTrack:
    name: str
    source: str
    kind: str
    count: int

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "FeatureTrack":
        name = str(data.get("name", "")).strip()
        source = str(data.get("source", "")).strip()
        kind = str(data.get("kind", "")).strip()
        count = int(data.get("count", 0))
        if not name:
            raise ValueError("Feature track entries must include a non-empty 'name'.")
        if not source:
            raise ValueError(f"Feature track '{name}' must include a non-empty 'source'.")
        if not kind:
            raise ValueError(f"Feature track '{name}' must include a non-empty 'kind'.")
        if count < 0:
            raise ValueError(f"Feature track '{name}' must not have a negative count.")
        return cls(name=name, source=source, kind=kind, count=count)


@dataclass(frozen=True)
class TranscriptRecord:
    transcript_id: str
    gene_name: str
    sequence: str
    labels: dict[str, object]
    feature_tracks: tuple[FeatureTrack, ...] = ()

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "TranscriptRecord":
        transcript_id = str(data.get("transcript_id", "")).strip()
        gene_name = str(data.get("gene_name", "")).strip()
        sequence = str(data.get("sequence", "")).strip().upper()
        labels = data.get("labels", {})
        feature_tracks = tuple(
            FeatureTrack.from_dict(item) for item in data.get("feature_tracks", [])
        )
        if not transcript_id:
            raise ValueError("Transcript records must include 'transcript_id'.")
        if not gene_name:
            raise ValueError(f"Transcript '{transcript_id}' must include 'gene_name'.")
        if not sequence:
            raise ValueError(f"Transcript '{transcript_id}' must include 'sequence'.")
        if not set(sequence) <= {"A", "C", "G", "T", "U", "N"}:
            raise ValueError(
                f"Transcript '{transcript_id}' contains non-IUPAC RNA/DNA characters."
            )
        if not isinstance(labels, dict) or not labels:
            raise ValueError(f"Transcript '{transcript_id}' must include non-empty 'labels'.")
        feature_names = [track.name for track in feature_tracks]
        if len(set(feature_names)) != len(feature_names):
            raise ValueError(
                f"Transcript '{transcript_id}' contains duplicate feature track names."
            )
        normalized_labels = {
            str(name).strip(): value
            for name, value in labels.items()
            if str(name).strip()
        }
        if not normalized_labels:
            raise ValueError(
                f"Transcript '{transcript_id}' must include at least one named label."
            )
        return cls(
            transcript_id=transcript_id,
            gene_name=gene_name,
            sequence=sequence,
            labels=normalized_labels,
            feature_tracks=feature_tracks,
        )


def load_transcript_records(path: str | Path) -> list[TranscriptRecord]:
    records: list[TranscriptRecord] = []
    dataset_path = Path(path)
    for line_number, line in enumerate(dataset_path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            payload = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Invalid JSON on line {line_number} of {dataset_path}: {exc.msg}"
            ) from exc
        records.append(TranscriptRecord.from_dict(payload))
    if not records:
        raise ValueError(f"No transcript records were found in {dataset_path}.")
    return records


def summarize_records(records: list[TranscriptRecord]) -> dict[str, object]:
    if not records:
        raise ValueError("Cannot summarize an empty record list.")

    label_distribution: dict[str, Counter[str]] = defaultdict(Counter)
    feature_sources: Counter[str] = Counter()
    feature_kinds: Counter[str] = Counter()
    feature_names: Counter[str] = Counter()

    for record in records:
        for label_name, value in record.labels.items():
            label_distribution[label_name][_stringify_label_value(value)] += 1
        for track in record.feature_tracks:
            feature_sources[track.source] += track.count
            feature_kinds[track.kind] += track.count
            feature_names[track.name] += track.count

    average_sequence_length = round(
        sum(len(record.sequence) for record in records) / len(records), 2
    )
    return {
        "transcript_count": len(records),
        "gene_count": len({record.gene_name for record in records}),
        "average_sequence_length": average_sequence_length,
        "label_distribution": {
            label: dict(counts) for label, counts in sorted(label_distribution.items())
        },
        "feature_tracks_by_source": dict(feature_sources.most_common()),
        "feature_tracks_by_kind": dict(feature_kinds.most_common()),
        "top_feature_tracks": dict(feature_names.most_common(5)),
    }


def _stringify_label_value(value: object) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, float):
        return f"{value:.3f}"
    return str(value)
