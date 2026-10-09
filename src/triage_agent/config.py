"""Explicit environment configuration, independent of provider requests."""

import os
from collections.abc import Mapping
from dataclasses import dataclass, field


class ConfigurationError(ValueError):
    """Live execution is missing required configuration."""


@dataclass(frozen=True, slots=True)
class Settings:
    api_key: str | None = field(default=None, repr=False)
    model: str | None = None

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "Settings":
        values = os.environ if environ is None else environ
        return cls(
            api_key=values.get("OPENAI_API_KEY", "").strip() or None,
            model=values.get("OPENAI_MODEL", "").strip() or None,
        )

    def require_live_credentials(self) -> tuple[str, str]:
        missing = []
        if not self.api_key:
            missing.append("OPENAI_API_KEY")
        if not self.model:
            missing.append("OPENAI_MODEL")
        if missing:
            raise ConfigurationError("Set " + " and ".join(missing) + " for live execution.")
        assert self.api_key is not None and self.model is not None
        return self.api_key, self.model

    def chat_model(self, *, http_client=None):
        from langchain_openai import ChatOpenAI

        key, model = self.require_live_credentials()
        return ChatOpenAI(
            api_key=key,
            model=model,
            timeout=30,
            max_retries=0,
            max_completion_tokens=4096,
            store=False,
            http_client=http_client,
        )
