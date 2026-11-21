"""OpenAI-compatible Chat Completions API adapter."""

from __future__ import annotations

import os
from typing import Any

import httpx

from .base import CompletionRequest, CompletionResponse


class OpenAICompatibleProvider:
    """Call an OpenAI-compatible API, including the configured DeepSeek API.

    The API key is loaded from the environment at request time and is never
    included in response objects or log messages.
    """

    def __init__(
        self,
        name: str,
        base_url: str,
        *,
        api_key_env: str,
        model: str,
        model_env: str | None = None,
        timeout_seconds: int = 180,
    ) -> None:
        self.name = name
        self.base_url = base_url.rstrip("/")
        self.api_key_env = api_key_env
        self.model = model
        self.model_env = model_env
        self.timeout_seconds = timeout_seconds

    def _api_key(self) -> str:
        key = os.getenv(self.api_key_env, "").strip()
        if not key:
            raise RuntimeError(
                f"Missing API credential: set environment variable {self.api_key_env}"
            )
        return key

    def _selected_model(self, request: CompletionRequest) -> str:
        if request.model:
            return request.model
        if self.model_env:
            configured = os.getenv(self.model_env, "").strip()
            if configured:
                return configured
        return self.model

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        messages: list[dict[str, Any]] = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})

        payload: dict[str, Any] = {
            "model": self._selected_model(request),
            "messages": messages,
        }
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        if request.max_tokens is not None:
            payload["max_tokens"] = request.max_tokens

        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self._api_key()}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()
        choices = data.get("choices") or []
        if not choices:
            raise RuntimeError(f"Provider '{self.name}' returned no completion choices")

        message = choices[0].get("message") or {}
        content = message.get("content") or ""
        if not isinstance(content, str):
            content = str(content)

        usage = data.get("usage") or {}
        return CompletionResponse(
            provider=self.name,
            model=data.get("model") or payload["model"],
            content=content,
            usage=usage,
            raw=data,
        )
