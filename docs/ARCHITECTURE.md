# Architecture

## 1. Goals

Research AI Hub coordinates model-assisted research without coupling the scientific calculation layer to a particular model vendor. It supports subscription-backed official command-line clients and direct API providers through one provider interface.

## 2. High-level components

    Research task
        |
        v
    Task router ---- configuration (providers + routes)
        |
        +---- Subscription CLI providers
        |         +-- Codex CLI
        |         +-- Claude Code
        |         +-- Gemini CLI
        |
        +---- API providers
                  +-- DeepSeek (OpenAI-compatible API)
                  +-- additional compatible API endpoints
        |
        v
    Normalized provider response
        |
        +---- comparison / independent review
        +---- artifact and provenance recorder
        +---- scientific tools (Python, Mathematica, local runners)
        |
        v
    GitHub research repository / report

## 3. Provider contract

Every provider receives a CompletionRequest containing a prompt and optional model, system prompt, temperature, and token limit. It returns a CompletionResponse with provider ID, model ID, text, and optional usage metadata.

Provider adapters own authentication and transport details. The router should not know whether a provider uses a subscription CLI or an API key.

## 4. Two authentication modes

### Subscription CLI

A command provider invokes an installed official CLI using an argument array (not a shell string). The provider's own login flow manages subscription authentication. The adapter does not read browser cookies, scrape web sessions, or access private credential stores.

CLI command templates are configuration-driven because command flags can change across tool versions. Before enabling a template, verify it against the installed CLI's official documentation and --help.

### API

An openai_compatible_api provider sends a Chat Completions request to a configured base URL. The API key is read at runtime from the environment variable named in configuration. The DeepSeek entry is a normal, first-class API provider, not a disabled example.

The generic adapter is intended for services that implement the OpenAI-compatible Chat Completions schema. Providers with a different protocol can receive a dedicated adapter without changing the orchestration interface.

## 5. Routing and cost control

- Explicit task routing takes precedence over defaults.
- Provider availability and authentication mode are visible in configuration.
- Automatic fallback from subscription CLI to a billable API is disabled by default.
- If a CLI fails, report the failure. Do not silently incur API charges.
- A user may explicitly enable a fallback route in local configuration after choosing the provider and budget policy.
- Store provider ID, model ID, access mode, timing, and usage metadata with each run.

## 6. Research workflow

A planned research task lifecycle:

1. Define the question, inputs, expected deliverables, and acceptance tests.
2. Route independent subtasks to selected providers.
3. Collect normalized outputs and provenance.
4. Compare claims, equations, code, and citations.
5. Run deterministic numerical checks outside the language model.
6. Record accepted results, unresolved discrepancies, and generated artifacts.
7. Commit reproducible outputs to the relevant research repository.

Model agreement is not a substitute for mathematical derivation or numerical validation.

## 7. Planned layers

- Task planner and dependency graph.
- Parallel execution with concurrency and rate limits.
- Independent-review and disagreement reports.
- Persistent run ledger and prompt/version provenance.
- Python and Mathematica execution adapters.
- GitHub issue/branch/PR workflow integration.
- Web research and citation verification.
