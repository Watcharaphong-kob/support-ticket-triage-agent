import unittest

from triage_agent.config import ConfigurationError, Settings


class SettingsTests(unittest.TestCase):
    def test_missing_credentials_are_allowed_for_offline_startup(self):
        settings = Settings.from_env({})
        self.assertIsNone(settings.api_key)
        self.assertIsNone(settings.model)

    def test_whitespace_values_are_missing(self):
        settings = Settings.from_env({"OPENAI_API_KEY": "  ", "OPENAI_MODEL": "\t"})
        with self.assertRaisesRegex(ConfigurationError, "OPENAI_API_KEY and OPENAI_MODEL"):
            settings.require_live_credentials()

    def test_model_and_key_are_trimmed_and_returned_for_live_use(self):
        settings = Settings.from_env(
            {"OPENAI_API_KEY": " test-only-secret ", "OPENAI_MODEL": " chosen-model "}
        )
        self.assertEqual(settings.require_live_credentials(), ("test-only-secret", "chosen-model"))

    def test_key_is_not_in_repr_or_configuration_error(self):
        settings = Settings.from_env({"OPENAI_API_KEY": "test-only-secret"})
        self.assertNotIn("test-only-secret", repr(settings))
        with self.assertRaises(ConfigurationError) as caught:
            settings.require_live_credentials()
        self.assertNotIn("test-only-secret", str(caught.exception))
        self.assertIn("OPENAI_MODEL", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
