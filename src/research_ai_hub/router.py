"""Explicit task routing with no implicit paid-provider fallback."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .config import load_yaml
from .providers import CompletionRequest, CompletionResponse
from .registry import ProviderRegistry


class TaskRouter:
    """Route a task to one configured provider.

    A provider override is an explicit user choice. Provider failures are
    returned to the caller; this router never silently switches to another
    provider or incurs a second provider's API cost.
    """

    def __init__(
        self,
        registry: ProviderRegistry,
        routes: dict[str, Any],
    ) -> None:
        routing = routes.get("routing", {})
        if not isinstance(routing, dict):
            raise ValueError("Routes configuration must contain a routing mapping")

        self.registry = registry
        self.default_provider = routing.get("default_provider")
        task_routes = routing.get("task_routes", {})
        if not isinstance(task_routes, dict):
            raise ValueError("'routing.task_routes' must be a mapping")
        self.task_routes = task_routes

        self.fallback_policy = routing.get("fallback_policy", "manual_only")
        if self.fallback_policy != "manual_only":
            raise ValueError(
                "Only fallback_policy='manual_only' is currently supported; "
                "automatic fallback is intentionally disabled"
            )

    @classmethod
    def from_yaml(
        cls,
        providers_path: str | Path,
        routes_path: str | Path,
    ) -> "TaskRouter":
        registry = ProviderRegistry.from_yaml(providers_path)
        routes = load_yaml(routes_path)
        return cls(registry, routes)

    def select_provider(
        self,
        task_type: str,
        provider_override: str | None = None,
    ) -> str:
        if provider_override:
            selected = provider_override
        else:
            selected = self.task_routes.get(task_type, self.default_provider)

        if not selected:
            raise ValueError(
                f"No provider configured for task '{task_type}' and no default provider is set"
            )

        self.registry.get(selected)
        return selected

    def complete(
        self,
        task_type: str,
        request: CompletionRequest,
        *,
        provider_override: str | None = None,
    ) -> CompletionResponse:
        provider_name = self.select_provider(task_type, provider_override)
        return self.registry.get(provider_name).complete(request)
