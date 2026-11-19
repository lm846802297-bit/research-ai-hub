"""Construct provider adapters from YAML configuration."""

from __future__ import annotations

from pathlib import Path

from .config import load_yaml, validate_provider_definitions
from .providers import CommandProvider, OpenAICompatibleProvider, Provider


class ProviderRegistry:
    def __init__(self, providers: dict[str, Provider]) -> None:
        self._providers = providers

    @classmethod
    def from_yaml(cls, path: str | Path) -> "ProviderRegistry":
        config = load_yaml(path)
        definitions = validate_provider_definitions(config)
        instances: dict[str, Provider] = {}

        for name, definition in definitions.items():
            if definition.get("enabled", True) is False:
                continue
            provider_type = definition["type"]
            timeout = int(definition.get("timeout_seconds", 180))

            if provider_type == "command":
                instances[name] = CommandProvider(
                    name,
                    definition["command"],
                    model=definition.get("model"),
                    timeout_seconds=timeout,
                )
            elif provider_type == "openai_compatible_api":
                instances[name] = OpenAICompatibleProvider(
                    name,
                    definition["base_url"],
                    api_key_env=definition["api_key_env"],
                    model=definition["model"],
                    model_env=definition.get("model_env"),
                    timeout_seconds=timeout,
                )

        return cls(instances)

    def get(self, name: str) -> Provider:
        try:
            return self._providers[name]
        except KeyError as exc:
            raise KeyError(f"Unknown or disabled provider: {name}") from exc

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._providers))
