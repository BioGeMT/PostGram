import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from postgram.config import EXAMPLE_CONFIG, load_project_config, write_example_config


class ConfigTests(unittest.TestCase):
    def test_load_project_config_reads_expected_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "project.toml"
            config_path.write_text(EXAMPLE_CONFIG, encoding="utf-8")

            config = load_project_config(config_path)

            self.assertEqual(config.project_name, "PostGram")
            self.assertEqual(len(config.tasks), 2)
            self.assertEqual(len(config.sources), 5)

    def test_write_example_config_refuses_to_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "project.toml"
            write_example_config(config_path)

            with self.assertRaises(FileExistsError):
                write_example_config(config_path)


if __name__ == "__main__":
    unittest.main()
