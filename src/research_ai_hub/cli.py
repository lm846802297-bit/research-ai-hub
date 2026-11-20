"""Command-line interface for Research AI Hub."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from dotenv import load_dotenv

from .config import load_yaml, validate_provider_definitions
from .providers import CompletionRequest
from .router import TaskRouter


def _default_path(explicit: str | None, local_name: str, example_name: str) -> Path:
    if explicit:
        return Path(explicit)
    local = Path("config") / local_name
    if local.exists():
        return local
    return Path("config") / example_name


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="research-ai-hub",
        description="Route research tasks across subscription CLIs and API providers.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    providers = subparsers.add_parser("providers", help="List configured providers")
    providers.add_argument("--config", dest="providers_config")

    run = subparsers.add_parser("run", help="Run one task through its configured provider")
    run.add_argument("--task", required=True, help="Task route key, e.g. independent_cross_check")
    run.add_argument("--prompt", required=True, help="Prompt to send to the selected provider")
    run.add_argument("--system-prompt")
    run.add_argument("--provider", help="Explicitly override the configured task route")
    run.add_argument("--model", help="Override the configured model")
    run.add_argument("--temperature", type=float)
    run.add_argument("--max-tokens", type=int)
    run.add_argument("--providers-config")
    run.add_argument("--routes-config")
    run.add_argument("--json", action="store_true", help="Print response metadata as JSON")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    load_dotenv(Path.cwd() / ".env", override=False)
    args = _parser().parse_args(argv)

    if args.command == "providers":
        config_path = _default_path(
            args.providers_config, "providers.local.yaml", "providers.example.yaml"
        )
        definitions = validate_provider_definitions(load_yaml(config_path))
        for name, definition in definitions.items():
            state = "enabled" if definition.get("enabled", True) else "disabled"
            print(
                f"{name}\t{definition.get('auth_mode', 'unknown')}\t"
                f"{definition.get('type', 'unknown')}\t{state}"
            )
        return 0

    providers_path = _default_path(
        args.providers_config, "providers.local.yaml", "providers.example.yaml"
    )
    routes_path = _default_path(
        args.routes_config, "routes.local.yaml", "routes.example.yaml"
    )
    router = TaskRouter.from_yaml(providers_path, routes_path)
    response = router.complete(
        args.task,
        CompletionRequest(
            prompt=args.prompt,
            system_prompt=args.system_prompt,
            model=args.model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        ),
        provider_override=args.provider,
    )

    if args.json:
        print(
            json.dumps(
                {
                    "provider": response.provider,
                    "model": response.model,
                    "content": response.content,
                    "usage": response.usage,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(response.content)
    return 0
