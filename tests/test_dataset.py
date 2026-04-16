import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from postgram.dataset import load_transcript_records, summarize_records


SAMPLE_DATASET = """{"transcript_id":"T1","gene_name":"GENE1","sequence":"AUGCUA","labels":{"p_body_enriched":true},"feature_tracks":[{"name":"eclip_binding_sites","source":"ENCODE","kind":"intervals","count":2}]}
{"transcript_id":"T2","gene_name":"GENE2","sequence":"AUGCUAGG","labels":{"p_body_enriched":false},"feature_tracks":[{"name":"mirna_target_sites","source":"TarBase","kind":"intervals","count":3}]}"""


class DatasetTests(unittest.TestCase):
    def test_load_transcript_records_and_summarize(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            dataset_path = Path(tmpdir) / "dataset.jsonl"
            dataset_path.write_text(SAMPLE_DATASET, encoding="utf-8")

            records = load_transcript_records(dataset_path)
            summary = summarize_records(records)

            self.assertEqual(summary["transcript_count"], 2)
            self.assertEqual(summary["gene_count"], 2)
            self.assertEqual(summary["feature_tracks_by_source"]["TarBase"], 3)
            self.assertEqual(summary["label_distribution"]["p_body_enriched"]["true"], 1)
            self.assertEqual(summary["label_distribution"]["p_body_enriched"]["false"], 1)

    def test_invalid_sequence_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            dataset_path = Path(tmpdir) / "dataset.jsonl"
            dataset_path.write_text(
                '{"transcript_id":"T1","gene_name":"GENE1","sequence":"AUGX","labels":{"p_body_enriched":true}}',
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_transcript_records(dataset_path)


if __name__ == "__main__":
    unittest.main()
