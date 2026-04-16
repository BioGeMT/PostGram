import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from postgram.cli import main


class CliTests(unittest.TestCase):
    def test_init_config_and_validate_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = Path(tmpdir) / "project.toml"

            init_stdout = io.StringIO()
            with contextlib.redirect_stdout(init_stdout):
                exit_code = main(["init-config", str(config_path)])
            self.assertEqual(exit_code, 0)

            validate_stdout = io.StringIO()
            with contextlib.redirect_stdout(validate_stdout):
                exit_code = main(["validate-manifest", str(config_path)])
            self.assertEqual(exit_code, 0)
            payload = json.loads(validate_stdout.getvalue())
            self.assertEqual(payload["project_name"], "PostGram")
            self.assertEqual(payload["source_count"], 5)


if __name__ == "__main__":
    unittest.main()
