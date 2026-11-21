"""Provider adapters for subscription CLIs and direct APIs."""

from .base import CompletionRequest, CompletionResponse, Provider
from .command import CommandProvider
from .openai_compatible import OpenAICompatibleProvider

__all__ = [
    "CompletionRequest",
    "CompletionResponse",
    "Provider",
    "CommandProvider",
    "OpenAICompatibleProvider",
]
