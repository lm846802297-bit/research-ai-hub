# Research AI Hub

## Research execution policy

Follow the mandatory [RESEARCH_COMPUTE_POLICY.md](RESEARCH_COMPUTE_POLICY.md): ordinary GPT chat uses ChatGPT Linux for primary scientific calculations; Codex/Work may use the user's Windows local environment or a GPT-managed cloud computer; GitHub is the canonical source/result archive; GitHub Actions is reserved for independent verification and CI.

**Subscription-first, API-supported multi-model research orchestration.**

Research AI Hub is a local-first workspace for routing research tasks to multiple model providers, collecting their outputs, comparing independent analyses, and preserving reproducible research records.

The project supports BOTH subscription-authenticated official CLIs and direct API providers. Subscription CLI access is preferred where an official client supports the user's plan; direct API access remains a first-class route. **DeepSeek API is enabled and retained.**

## Design principles

- Prefer official subscription-backed CLI login when it is available and suitable.
- Keep API providers enabled as an explicit alternative; never delete or hide API configuration.
- Never silently switch a failed subscription request to a billable API. Automatic paid fallback is disabled.
- Use official provider CLIs and documented APIs. Do not scrape browser sessions, copy cookies, or bypass provider controls.
- Keep credentials in environment variables or a local secret manager; never commit API keys.
- Separate model orchestration from scientific computation. Python/Mathematica and local compute runners remain responsible for deterministic calculations.
- Preserve provider/model identifiers, prompts, outputs, and usage metadata for reproducibility.

## Provider access modes

| Provider | Access mode | Authentication |
|---|---|---|
| Codex CLI | subscription_cli | Official Codex CLI login with ChatGPT |
| Claude Code | subscription_cli | Official Claude Code login |
| Gemini CLI | subscription_cli | Official Gemini CLI login |
| DeepSeek | api | DEEPSEEK_API_KEY |
| Other compatible APIs | api | Provider-specific environment variable |

The example command templates use the documented non-interactive modes: codex exec, claude -p, and gemini -p. See the [Codex CLI reference](https://learn.chatgpt.com/docs/cli/reference), [Claude Code CLI reference](https://docs.anthropic.com/en/docs/claude-code/cli-usage), and [Gemini CLI reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/cli-reference.md).

## Quick start

Install Python 3.11 or newer, then install the project:

    python -m venv .venv
    # Windows PowerShell: .venv\Scripts\Activate.ps1
    # macOS/Linux: source .venv/bin/activate
    python -m pip install -e ".[dev]"

Copy the example configuration:

    # Windows PowerShell
    Copy-Item config/providers.example.yaml config/providers.local.yaml
    Copy-Item config/routes.example.yaml config/routes.local.yaml
    Copy-Item .env.example .env

    # macOS/Linux
    cp config/providers.example.yaml config/providers.local.yaml
    cp config/routes.example.yaml config/routes.local.yaml
    cp .env.example .env

Sign in with the official CLI tools you want to use. For Codex, codex login supports ChatGPT sign-in; check the active method with codex login status.

For DeepSeek API, set the key in your local .env file or shell. The default model is deepseek-v4-pro; set DEEPSEEK_MODEL=deepseek-flash when you prefer the flash model. The model can also be overridden per request.

Windows PowerShell:

    $env:DEEPSEEK_API_KEY = "your-key"
    $env:DEEPSEEK_MODEL = "deepseek-v4-pro"

macOS/Linux:

    export DEEPSEEK_API_KEY="your-key"
    export DEEPSEEK_MODEL="deepseek-v4-pro"

The CLI loads a .env file from the current working directory automatically.

List providers and their access modes:

    research-ai-hub providers

Run a task through its configured route:

    research-ai-hub run --task independent_cross_check --prompt "Independently check this derivation: ..."

Choose a provider explicitly for one request:

    research-ai-hub run --task literature_survey --provider deepseek --prompt "Compare these papers ..."

Select a model for one request:

    research-ai-hub run --task independent_cross_check --provider codex --model gpt-model-name --prompt "Check this calculation"

Print provider/model/usage metadata as JSON:

    research-ai-hub run --task independent_cross_check --prompt "Check the calculation" --json

## Testing

Run the test suite in the active Python environment:

    python -m pytest -q

Run the complete Python 3.11 / 3.12 / 3.13 matrix locally on Windows with uv:

    .\scripts\test-python-matrix.ps1

The script uses isolated environments and does not rely on GitHub-hosted runner minutes. See [CI troubleshooting](docs/CI_TROUBLESHOOTING.md) for pre-runner failures and billing checks.

## Configuration

- config/providers.example.yaml: provider definitions, authentication modes, CLI commands, API base URLs, and environment-variable names.
- config/routes.example.yaml: task-to-provider routing and fallback policy.
- .env.example: environment variable names only; it contains no secrets.

Copy the examples to *.local.yaml and .env. Local files are ignored by Git.

### Routing and cost policy

The default fallback_policy is manual_only. If a subscription CLI fails, the error is returned. The hub does not silently send the same prompt to a paid API provider. A provider can be selected explicitly with --provider.

## Current implementation

- Normalized provider request/response interface.
- Subscription CLI adapter for Codex, Claude Code, and Gemini CLI.
- OpenAI-compatible API adapter with enabled DeepSeek configuration.
- YAML provider validation and provider registry.
- Task router with explicit task routes and manual provider override.
- CLI for listing providers and running routed tasks.
- .env loading, per-request model selection, and secret-redacted CLI diagnostics.
- Unit tests for configuration, routing, command invocation, and mocked API requests.

The next layers—parallel multi-agent runs, independent disagreement reports, research memory, citation auditing, and scientific-computation adapters—will be added separately and validated with dedicated tests.

## Repository layout

    config/                 Example provider and routing configuration
    docs/                   Architecture and provider-authentication notes
    scripts/                Local validation scripts
    src/research_ai_hub/    Orchestrator package, router, CLI, and provider adapters
    tests/                  Unit and integration-mock tests
    .github/workflows/      Continuous integration

## Security

Never commit API keys, access tokens, CLI credentials, browser profiles, or provider session files. Subscription CLI authentication is managed by each provider's official tool; this project only launches the configured command and captures its output. Common credential patterns are redacted from surfaced CLI diagnostics.
