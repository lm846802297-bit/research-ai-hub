# Research AI Hub

**Subscription-first, API-supported multi-model research orchestration.**

Research AI Hub is a local-first workspace for routing research tasks to multiple model providers, collecting their outputs, comparing independent analyses, and preserving reproducible research records.

The project deliberately supports BOTH subscription-authenticated official CLIs and direct API providers. Subscription use is the default preference where an official CLI supports the user's plan; API access remains a first-class, configurable route. DeepSeek API support is retained explicitly.

## Design principles

- Prefer official subscription-backed CLI login when it is available and suitable.
- Keep API providers enabled as an explicit alternative; never delete or hide API configuration.
- Never silently switch a failed subscription request to a billable API. Automatic paid fallback is disabled by default.
- Use official provider CLIs and documented APIs. Do not scrape browser sessions, copy cookies, or bypass provider controls.
- Keep credentials in environment variables or a local secret manager; never commit API keys.
- Separate model orchestration from scientific computation. Python/Mathematica and local compute runners remain responsible for deterministic calculations.
- Preserve prompts, model/provider identifiers, timestamps, outputs, and validation results for reproducibility.

## Provider access modes

| Provider entry | Access mode | Authentication |
|---|---|---|
| Codex | subscription_cli | Official Codex CLI login |
| Claude Code | subscription_cli | Official Claude Code login |
| Gemini CLI | subscription_cli | Official Gemini CLI login |
| DeepSeek | api | DEEPSEEK_API_KEY |
| Other compatible APIs | api | Provider-specific environment variable |

The CLI command templates are configurable in config/providers.example.yaml; verify them against the installed CLI version's --help output before enabling a provider.

## Quick start

1. Install Python 3.11 or newer.
2. Create an environment and install the project:

       python -m venv .venv
       # Windows PowerShell: .venv\Scripts\Activate.ps1
       # macOS/Linux: source .venv/bin/activate
       python -m pip install -e ".[dev]"

3. Copy the example configuration:

       # Windows PowerShell
       Copy-Item config/providers.example.yaml config/providers.local.yaml
       Copy-Item config/routes.example.yaml config/routes.local.yaml
       Copy-Item .env.example .env
       # macOS/Linux
       cp config/providers.example.yaml config/providers.local.yaml
       cp config/routes.example.yaml config/routes.local.yaml
       cp .env.example .env

4. Sign in through the official CLI for the subscription providers you want to use.
5. For DeepSeek API, set DEEPSEEK_API_KEY in the process environment or your local secret manager. Do not put the key in a committed YAML file.
6. Edit local provider commands and task routes, then run tests:

       pytest

## Configuration

- config/providers.example.yaml: provider definitions, authentication modes, CLI commands, API base URLs, and environment-variable names.
- config/routes.example.yaml: task-to-provider routing and fallback policy.
- .env.example: names of supported environment variables only; it contains no secrets.

Local files named *.local.yaml and .env are ignored by Git.

## Current implementation

- Provider interface and normalized completion request/response objects.
- Configurable command-line provider adapter for subscription-authenticated official CLIs.
- OpenAI-compatible API adapter, including a named DeepSeek configuration.
- Provider registry and configuration validation.
- Initial unit tests and GitHub Actions test workflow.

The first milestone is provider connectivity and safe routing. Multi-agent debate, research memory, citation auditing, scientific-computation adapters, and a user interface will be added as separate, testable layers.

## Repository layout

    config/                 Example provider and routing configuration
    docs/                   Architecture and provider-authentication notes
    src/research_ai_hub/    Orchestrator package and provider adapters
    tests/                  Unit tests
    .github/workflows/      Continuous integration

## Security

Never commit API keys, access tokens, CLI credentials, browser profiles, or provider session files. Subscription CLI authentication is managed by each provider's official tool; this project only launches the configured command and captures its output.
