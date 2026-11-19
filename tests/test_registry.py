from pathlib import Path

import pytest

from research_ai_hub.config import load_yaml, validate_provider_definitions
from research_ai_hub.providers import CommandProvider, CompletionRequest
from research_ai_hub.registry import ProviderRegistry


ROOT = Path(__file__).parents[1]


def test_example_configuration_keeps_subscription_and_api_modes():
    config = load_yaml(ROOT / "config" / "providers.example.yaml")
    definitions = validate_provider_definitions(config)

    assert definitions["codex"]["auth_mode"] == "subscription_cli"
    assert definitions["claude"]["auth_mode"] == "subscription_cli"
    assert definitions["gemini"]["auth_mode"] == "subscription_cli"
    assert definitions["deepseek"]["auth_mode"] == "api"
    assert definitions["deepseek"]["enabled"] is True


def test_registry_builds_deepseek_without_reading_secret():
    registry = ProviderRegistry.from_yaml(ROOT / "config" / "providers.example.yaml")

    assert "deepseek" in registry.names()
    assert registry.get("deepseek").name == "deepseek"


def test_command_provider_substitutes_prompt_without_shell():
    provider = CommandProvider("test", ["fake-cli", "--prompt", "{prompt}"])
    command = provider.build_command(CompletionRequest(prompt="check the equation"))

    assert command == ["fake-cli", "--prompt", "check the equation"]


def test_invalid_auth_mode_is_rejected():
    config = {
        "providers": {
            "broken": {
                "type": "openai_compatible_api",
                "auth_mode": "subscription_cli",
                "base_url": "https://example.invalid",
                "api_key_env": "EXAMPLE_KEY",
                "model": "example-model",
            }
        }
    }
    with pytest.raises(ValueError, match="must use api auth"):
        validate_provider_definitions(config)
