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


if __name__ == "__main__":
    unittest.main()


def test_invalid_batch_fails_before_constructing_provider(tmp_path, monkeypatch, capsys):
    from triage_agent.config import Settings

    def forbidden_provider(self):
        raise AssertionError("Invalid input must not construct a provider")

    monkeypatch.setattr(Settings, "chat_model", forbidden_provider)
    path = tmp_path / "invalid.json"
    path.write_text("[]", encoding="utf-8")
    assert main(["--input", str(path)]) == 2
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
            "-c",
            "import sys; sys.path.insert(0, 'tests'); "
            "from test_agent import ScriptedChatModel, tool_requests; "
            "from triage_agent.config import Settings; "
            "from triage_agent.cli import main; "
            "Settings.chat_model = lambda self: ScriptedChatModel("
            "turns=[tool_requests('customer-002')]); sys.exit(main())",
            "--input",
            str(path),
            "--customers",
            str(root / "data/customers.json"),
            "--trace",
        ],
        env=environ,
        cwd=root,
        capture_output=True,
        timeout=30,
    )
    assert result.returncode == 1
    assert json.loads(result.stdout.decode("utf-8"))["results"][0]["ticket_id"] == "ตั๋ว-002"
    assert json.loads(result.stderr.decode("utf-8"))["ticket_id"] == "ตั๋ว-002"
