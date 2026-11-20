import subprocess

from research_ai_hub.providers import CommandProvider, CompletionRequest
from research_ai_hub.providers.command import _redact_diagnostic


def test_command_provider_runs_without_shell_and_combines_system_prompt(monkeypatch):
    captured = {}

    def fake_run(command, **kwargs):
        captured["command"] = command
        captured.update(kwargs)
        return subprocess.CompletedProcess(command, 0, stdout="answer\n", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    provider = CommandProvider("codex", ["codex", "exec", "{prompt}"])
    response = provider.complete(
        CompletionRequest(prompt="Check this", system_prompt="You are a reviewer")
    )

    assert captured["command"] == [
        "codex", "exec", "You are a reviewer\n\nCheck this"
    ]
    assert captured["shell"] is False
    assert response.content == "answer"


def test_cli_error_diagnostics_redact_common_credentials():
    text = "Authorization: Bearer abc123 api_key=sk-abcdefghijklmnop token=ds-abcdefghijklmnop"
    redacted = _redact_diagnostic(text)
    assert "abc123" not in redacted
    assert "sk-abcdefghijklmnop" not in redacted
    assert "ds-abcdefghijklmnop" not in redacted
