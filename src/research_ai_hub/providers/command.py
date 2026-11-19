"""Adapter for official, locally authenticated command-line clients."""

from __future__ import annotations

import subprocess
from collections.abc import Sequence

from .base import CompletionRequest, CompletionResponse


class CommandProvider:
    """Run a configured CLI command without invoking a shell.

    The command is an argument sequence. The literal placeholders
    {prompt} and {model} are substituted per request. Authentication
    remains owned by the official CLI's own login mechanism.
    """

    def __init__(
        self,
        name: str,
        command: Sequence[str],
        *,
        model: str | None = None,
        timeout_seconds: int = 900,
    ) -> None:
        if not command:
            raise ValueError("command must contain at least one argument")
        if not any("{prompt}" in part for part in command):
            raise ValueError("command must contain a {prompt} placeholder")
        self.name = name
        self.command = tuple(command)
        self.model = model
        self.timeout_seconds = timeout_seconds

    def build_command(self, request: CompletionRequest) -> list[str]:
        selected_model = request.model or self.model or ""
        return [
            part.replace("{prompt}", request.prompt).replace("{model}", selected_model)
            for part in self.command
        ]

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        if request.system_prompt:
            prompt = f"{request.system_prompt}\n\n{request.prompt}"
            request = CompletionRequest(
                prompt=prompt,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                metadata=request.metadata,
            )

        result = subprocess.run(
            self.build_command(request),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=self.timeout_seconds,
            check=False,
            shell=False,
        )
        if result.returncode != 0:
            stderr = result.stderr.strip()[-4000:]
            raise RuntimeError(
                f"Provider '{self.name}' exited with code {result.returncode}: {stderr}"
            )

        return CompletionResponse(
            provider=self.name,
            model=request.model or self.model or "cli-default",
            content=result.stdout.strip(),
            raw=result.stdout,
        )
