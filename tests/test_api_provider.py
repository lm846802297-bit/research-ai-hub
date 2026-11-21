from __future__ import annotations

import pytest

from research_ai_hub.providers import CompletionRequest, OpenAICompatibleProvider


class FakeResponse:
    def raise_for_status(self):
        return None

    def json(self):
        return {
            "model": "deepseek-v4-pro",
            "choices": [{"message": {"content": "independent check complete"}}],
            "usage": {"prompt_tokens": 12, "completion_tokens": 8, "total_tokens": 20},
        }


def test_deepseek_api_request_uses_configured_key_and_model(monkeypatch):
    import httpx

    monkeypatch.setenv("TEST_DEEPSEEK_KEY", "test-secret")
    monkeypatch.setenv("TEST_DEEPSEEK_MODEL", "deepseek-v4-pro")
    calls = {}

    def fake_post(url, **kwargs):
        calls["url"] = url
        calls.update(kwargs)
        return FakeResponse()

    monkeypatch.setattr(httpx, "post", fake_post)
    provider = OpenAICompatibleProvider(
        "deepseek",
        "https://api.deepseek.com/",
        api_key_env="TEST_DEEPSEEK_KEY",
        model="deepseek-flash",
        model_env="TEST_DEEPSEEK_MODEL",
    )
    response = provider.complete(
        CompletionRequest(prompt="Check this derivation", system_prompt="Act as a reviewer")
    )

    assert calls["url"] == "https://api.deepseek.com/chat/completions"
    assert calls["headers"]["Authorization"] == "Bearer test-secret"
    assert calls["json"]["model"] == "deepseek-v4-pro"
    assert calls["json"]["messages"] == [
        {"role": "system", "content": "Act as a reviewer"},
        {"role": "user", "content": "Check this derivation"},
    ]
    assert response.provider == "deepseek"
    assert response.content == "independent check complete"
    assert response.usage["total_tokens"] == 20


def test_deepseek_api_requires_key_before_network_call(monkeypatch):
    monkeypatch.delenv("TEST_DEEPSEEK_KEY", raising=False)
    provider = OpenAICompatibleProvider(
        "deepseek",
        "https://api.deepseek.com",
        api_key_env="TEST_DEEPSEEK_KEY",
        model="deepseek-v4-pro",
    )
    with pytest.raises(RuntimeError, match="TEST_DEEPSEEK_KEY"):
        provider.complete(CompletionRequest(prompt="hello"))


def test_deepseek_api_rejects_empty_choices(monkeypatch):
    import httpx

    monkeypatch.setenv("TEST_DEEPSEEK_KEY", "test-secret")

    class EmptyResponse(FakeResponse):
        def json(self):
            return {"choices": []}

    monkeypatch.setattr(httpx, "post", lambda *args, **kwargs: EmptyResponse())
    provider = OpenAICompatibleProvider(
        "deepseek",
        "https://api.deepseek.com",
        api_key_env="TEST_DEEPSEEK_KEY",
        model="deepseek-v4-pro",
    )
    with pytest.raises(RuntimeError, match="no completion choices"):
        provider.complete(CompletionRequest(prompt="hello"))
