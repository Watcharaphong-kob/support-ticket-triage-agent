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

    def test_unimplemented_processing_fails_visibly_without_fake_json(self):
        output, errors = io.StringIO(), io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            result = main(["--input", "tickets.json", "--trace"])
        self.assertEqual(result, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("not implemented", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
