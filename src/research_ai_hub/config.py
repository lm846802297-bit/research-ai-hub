"""Configuration loading and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml


SUPPORTED_TYPES = {"command", "openai_compatible_api"}
SUPPORTED_AUTH_MODES = {"subscription_cli", "api"}


def load_yaml(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Configuration root must be a mapping: {path}")
    return data


def validate_provider_definitions(config: dict[str, Any]) -> dict[str, dict[str, Any]]:
    providers = config.get("providers")
    if not isinstance(providers, dict):
        raise ValueError("Configuration must contain a 'providers' mapping")

    for name, definition in providers.items():
        if not isinstance(definition, dict):
            raise ValueError(f"Provider '{name}' must be a mapping")
        if definition.get("enabled", True) is False:
            continue

        provider_type = definition.get("type")
        auth_mode = definition.get("auth_mode")
        if provider_type not in SUPPORTED_TYPES:
            raise ValueError(
                f"Provider '{name}' has unsupported type: {provider_type!r}"
            )
        if auth_mode not in SUPPORTED_AUTH_MODES:
            raise ValueError(
                f"Provider '{name}' has unsupported auth_mode: {auth_mode!r}"
            )

        timeout = definition.get("timeout_seconds", 180)
        if not isinstance(timeout, int) or timeout <= 0:
            raise ValueError(f"Provider '{name}' timeout_seconds must be a positive integer")

        if provider_type == "command":
            if auth_mode != "subscription_cli":
                raise ValueError(
                    f"Command provider '{name}' must use subscription_cli auth"
                )
            command = definition.get("command")
            if (
                not isinstance(command, list)
                or not command
                or not all(isinstance(part, str) for part in command)
            ):
                raise ValueError(f"Command provider '{name}' needs a non-empty string command list")
            if not any("{prompt}" in part for part in command):
                raise ValueError(f"Command provider '{name}' needs a {{prompt}} placeholder")

        if provider_type == "openai_compatible_api":
            if auth_mode != "api":
                raise ValueError(f"API provider '{name}' must use api auth")
            for required in ("base_url", "api_key_env", "model"):
                if not isinstance(definition.get(required), str) or not definition[required].strip():
                    raise ValueError(
                        f"API provider '{name}' is missing required field '{required}'"
                    )
            parsed_url = urlparse(definition["base_url"])
            if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
                raise ValueError(f"API provider '{name}' base_url must be an absolute HTTP(S) URL")
            model_env = definition.get("model_env")
            if model_env is not None and not isinstance(model_env, str):
                raise ValueError(f"API provider '{name}' model_env must be a string")

    return providers
