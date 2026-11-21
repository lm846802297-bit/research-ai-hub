from pathlib import Path
import os

from research_ai_hub.cli import main


def test_cli_loads_dotenv_and_lists_subscription_and_api_providers(tmp_path, monkeypatch, capsys):
    (tmp_path / ".env").write_text("RESEARCH_HUB_TEST_VALUE=loaded\n", encoding="utf-8")
    monkeypatch.delenv("RESEARCH_HUB_TEST_VALUE", raising=False)
    monkeypatch.chdir(tmp_path)

    repo_root = Path(__file__).parents[1]
    assert main(["providers", "--config", str(repo_root / "config" / "providers.example.yaml")]) == 0

    output = capsys.readouterr().out
    assert "codex\tsubscription_cli" in output
    assert "deepseek\tapi" in output
    assert os.environ["RESEARCH_HUB_TEST_VALUE"] == "loaded"
