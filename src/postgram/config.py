from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import tomllib

SUPPORTED_TASKS = {
    "p_body_vs_non_p_body",
    "stress_granule_vs_non_stress",
}

EXAMPLE_CONFIG = """project_name = "PostGram"
species = "homo_sapiens"
release = "draft-aim1-aim2"
tasks = ["p_body_vs_non_p_body", "stress_granule_vs_non_stress"]
output_dir = "outputs"

[[sources]]
name = "ensembl_transcripts"
kind = "reference"
path = "data/raw/ensembl/transcripts.fa"
description = "Transcript annotations and 3'UTR-aware sequences"

[[sources]]
name = "localization_labels"
kind = "localization"
path = "data/raw/localization/labels.tsv"
description = "Transcript or gene-level localization labels for P-bodies and stress granules"

[[sources]]
name = "encode_eclip"
kind = "binding"
path = "data/raw/encode/eclip.tsv"
description = "RBP binding events from eCLIP"

[[sources]]
name = "tarbase"
kind = "interaction"
path = "data/raw/tarbase/interactions.tsv"
description = "Experimentally supported miRNA-target interactions"

[[sources]]
name = "utr_motifs"
kind = "annotation"
path = "data/raw/motifs/utr_annotations.tsv"
description = "Motif-centric regulatory annotations mapped onto transcript UTRs"
"""


@dataclass(frozen=True)
class SourceConfig:
    name: str
    kind: str
    path: str
    description: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "SourceConfig":
        name = str(data.get("name", "")).strip()
        kind = str(data.get("kind", "")).strip()
        path = str(data.get("path", "")).strip()
        description = str(data.get("description", "")).strip()
        if not name:
            raise ValueError("Source entries must include a non-empty 'name'.")
        if not kind:
            raise ValueError(f"Source '{name}' must include a non-empty 'kind'.")
        if not path:
            raise ValueError(f"Source '{name}' must include a non-empty 'path'.")
        return cls(name=name, kind=kind, path=path, description=description)


@dataclass(frozen=True)
class ProjectConfig:
    project_name: str
    species: str
    release: str
    tasks: tuple[str, ...]
    output_dir: str = "outputs"
    sources: tuple[SourceConfig, ...] = ()

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "ProjectConfig":
        project_name = str(data.get("project_name", "")).strip()
        species = str(data.get("species", "")).strip()
        release = str(data.get("release", "")).strip()
        output_dir = str(data.get("output_dir", "outputs")).strip() or "outputs"
        tasks = tuple(str(task).strip() for task in data.get("tasks", []))
        sources = tuple(SourceConfig.from_dict(item) for item in data.get("sources", []))
        config = cls(
            project_name=project_name,
            species=species,
            release=release,
            tasks=tasks,
            output_dir=output_dir,
            sources=sources,
        )
        config.validate()
        return config

    def validate(self) -> None:
        if not self.project_name:
            raise ValueError("Project config must include 'project_name'.")
        if not self.species:
            raise ValueError("Project config must include 'species'.")
        if not self.release:
            raise ValueError("Project config must include 'release'.")
        if not self.tasks:
            raise ValueError("Project config must define at least one task.")
        unsupported = sorted(set(self.tasks) - SUPPORTED_TASKS)
        if unsupported:
            raise ValueError(
                "Unsupported tasks in config: " + ", ".join(unsupported)
            )
        if len(set(self.tasks)) != len(self.tasks):
            raise ValueError("Project config tasks must be unique.")
        source_names = [source.name for source in self.sources]
        if len(set(source_names)) != len(source_names):
            raise ValueError("Source names must be unique within the config.")

    def to_dict(self) -> dict[str, object]:
        return {
            "project_name": self.project_name,
            "species": self.species,
            "release": self.release,
            "tasks": list(self.tasks),
            "output_dir": self.output_dir,
            "sources": [asdict(source) for source in self.sources],
        }


def load_project_config(path: str | Path) -> ProjectConfig:
    config_path = Path(path)
    data = tomllib.loads(config_path.read_text(encoding="utf-8"))
    return ProjectConfig.from_dict(data)


def write_example_config(path: str | Path, force: bool = False) -> Path:
    target = Path(path)
    if target.exists() and not force:
        raise FileExistsError(
            f"Refusing to overwrite existing config: {target}. Use force=True to replace it."
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(EXAMPLE_CONFIG, encoding="utf-8")
    return target
