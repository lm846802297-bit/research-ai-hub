import pytest

from research_ai_hub.providers import CompletionRequest, CompletionResponse
from research_ai_hub.registry import ProviderRegistry
from research_ai_hub.router import TaskRouter


class FakeProvider:
    def __init__(self, name, content="ok", error=None):
        self.name = name
        self.content = content
        self.error = error
        self.calls = 0

    def complete(self, request):
        self.calls += 1
        if self.error:
            raise self.error
        return CompletionResponse(self.name, "test-model", self.content)


def make_router():
    deepseek = FakeProvider("deepseek", "cross-check")
    codex = FakeProvider("codex", "code-review")
    registry = ProviderRegistry({"deepseek": deepseek, "codex": codex})
    router = TaskRouter(
        registry,
        {
            "routing": {
                "fallback_policy": "manual_only",
                "default_provider": "codex",
                "task_routes": {"independent_cross_check": "deepseek"},
            }
        },
    )
    return router, deepseek, codex


def test_router_uses_task_specific_provider():
    router, deepseek, codex = make_router()
    result = router.complete(
        "independent_cross_check", CompletionRequest(prompt="review")
    )
    assert result.provider == "deepseek"
    assert deepseek.calls == 1
    assert codex.calls == 0


def test_explicit_provider_override_is_respected():
    router, deepseek, codex = make_router()
    result = router.complete(
        "independent_cross_check",
        CompletionRequest(prompt="review"),
        provider_override="codex",
    )
    assert result.provider == "codex"
    assert codex.calls == 1
    assert deepseek.calls == 0


def test_failed_provider_does_not_trigger_implicit_fallback():
    failing = FakeProvider("deepseek", error=RuntimeError("provider unavailable"))
    fallback = FakeProvider("codex")
    router = TaskRouter(
        ProviderRegistry({"deepseek": failing, "codex": fallback}),
        {
            "routing": {
                "fallback_policy": "manual_only",
                "default_provider": "codex",
                "task_routes": {"independent_cross_check": "deepseek"},
            }
        },
    )
    with pytest.raises(RuntimeError, match="provider unavailable"):
        router.complete("independent_cross_check", CompletionRequest(prompt="review"))
    assert failing.calls == 1
    assert fallback.calls == 0


def test_automatic_fallback_policy_is_rejected():
    registry = ProviderRegistry({"codex": FakeProvider("codex")})
    with pytest.raises(ValueError, match="manual_only"):
        TaskRouter(registry, {"routing": {"fallback_policy": "automatic"}})
