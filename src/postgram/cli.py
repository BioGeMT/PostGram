from __future__ import annotations

import argparse
import json
from pathlib import Path

from postgram.config import ProjectConfig, load_project_config, write_example_config
from postgram.dataset import load_transcript_records, summarize_records


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="postgram",
        description="Utilities for building localization-aware PostGram datasets.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_config = subparsers.add_parser(
        "init-config", help="Write an example project manifest."
    )
    init_config.add_argument("path", type=Path, help="Where to write the TOML manifest.")
    init_config.add_argument(
        "--force",
        action="store_true",
        help="Overwrite the target file if it already exists.",
    )

    validate_manifest = subparsers.add_parser(
        "validate-manifest", help="Load and validate a TOML project manifest."
    )
    validate_manifest.add_argument("path", type=Path, help="Path to a TOML manifest.")

    summarize_dataset = subparsers.add_parser(
        "summarize-dataset",
        help="Summarize transcript-level JSONL records for inspection.",
    )
    summarize_dataset.add_argument("path", type=Path, help="Path to a JSONL dataset.")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "init-config":
        target = write_example_config(args.path, force=args.force)
        print(json.dumps({"written": str(target)}, indent=2))
        return 0

    if args.command == "validate-manifest":
        config = load_project_config(args.path)
        print(json.dumps(_config_summary(config), indent=2))
        return 0

    if args.command == "summarize-dataset":
        records = load_transcript_records(args.path)
        print(json.dumps(summarize_records(records), indent=2))
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


def _config_summary(config: ProjectConfig) -> dict[str, object]:
    return {
        "project_name": config.project_name,
        "species": config.species,
        "release": config.release,
        "task_count": len(config.tasks),
        "tasks": list(config.tasks),
        "source_count": len(config.sources),
        "sources": [source.name for source in config.sources],
        "output_dir": config.output_dir,
    }
