import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

from triage_agent.cli import main


class CliTests(unittest.TestCase):
    def test_no_arguments_shows_help_without_credentials(self):
        output = io.StringIO()
        with redirect_stdout(output):
            result = main([])
        self.assertEqual(result, 0)
        self.assertIn("--input", output.getvalue())
        self.assertIn("--trace", output.getvalue())

    def test_help_exits_successfully(self):
        with redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as caught:
            main(["--help"])
        self.assertEqual(caught.exception.code, 0)

    def test_version_exits_successfully(self):
        output = io.StringIO()
        with redirect_stdout(output), self.assertRaises(SystemExit) as caught:
            main(["--version"])
        self.assertEqual(caught.exception.code, 0)
        self.assertIn("0.1.0", output.getvalue())

    def test_missing_input_fails_visibly_without_fake_json(self):
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            result = main(["--input", "tickets.json", "--trace"])
        self.assertEqual(result, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("Input/configuration", errors.getvalue())

    def test_offline_mode_is_explicit_in_help(self):
        output = io.StringIO()
        with redirect_stdout(output):
            main([])
        self.assertIn("--offline", output.getvalue())


if __name__ == "__main__":
    unittest.main()


def test_offline_rejects_live_embedding_configuration_before_constructing_provider(
    monkeypatch, capsys
):
    from pathlib import Path

    import triage_agent.cli as cli

    monkeypatch.setenv("EMBEDDING_BACKEND", "openai")

    def forbidden_provider():
        raise AssertionError("Offline execution must not construct a live embedder")

    monkeypatch.setattr(cli, "configured_embedder", forbidden_provider)
    path = Path(__file__).resolve().parents[1] / "data/sample_tickets.json"
    assert cli.main(["--input", str(path), "--offline"]) == 2
    assert capsys.readouterr().out == ""


def test_redirected_windows_encoding_preserves_unicode_json(tmp_path):
    import json
    import os
    import subprocess
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    current = json.loads((root / "data/sample_tickets.json").read_text(encoding="utf-8"))[1]
    current["ticket_id"] = "ตั๋ว-002"
    path = tmp_path / "thai.json"
    path.write_text(json.dumps(current, ensure_ascii=False), encoding="utf-8")
    environ = dict(
        os.environ,
        PYTHONIOENCODING="cp1252",
        PGHOST="127.0.0.1",
        PGPORT="1",
        EMBEDDING_BACKEND="fake",
        EMBEDDING_MODEL="fake-token-v1",
        EMBEDDING_DIMENSION="64",
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "triage_agent",
            "--input",
            str(path),
            "--customers",
            str(root / "data/customers.json"),
            "--offline",
            "--trace",
        ],
        env=environ,
        capture_output=True,
        timeout=15,
    )
    assert result.returncode == 1
    assert json.loads(result.stdout.decode("utf-8"))["results"][0]["ticket_id"] == "ตั๋ว-002"
    assert json.loads(result.stderr.decode("utf-8"))["ticket_id"] == "ตั๋ว-002"
