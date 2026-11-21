"""Shared provider request and response types."""

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(frozen=True)
class CompletionRequest:
    prompt: str
    model: str | None = None
    system_prompt: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CompletionResponse:
    provider: str
    model: str
    content: str
    usage: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] | str | None = None


class Provider(Protocol):
    name: str

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Run one completion and return a normalized response."""
