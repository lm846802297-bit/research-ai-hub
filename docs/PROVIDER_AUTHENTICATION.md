# Provider authentication and access modes

Research AI Hub supports both subscription-backed official CLI authentication and direct API access. Subscription CLI is the preferred path when the provider offers a CLI compatible with the user's plan. API access remains a first-class, enabled route.

## Subscription-backed official CLI

| Provider | Non-interactive command | Login ownership |
|---|---|---|
| Codex | codex exec <prompt> | Codex CLI |
| Claude Code | claude -p <prompt> | Claude Code |
| Gemini CLI | gemini -p <prompt> | Gemini CLI |

The application launches the configured executable. The user signs in through the provider's official login flow. For Codex, codex login supports ChatGPT OAuth and codex login status reports the active authentication method.

Model overrides supplied through the hub are passed to each CLI with its --model option. When no override is supplied, the optional model argument is omitted and the CLI uses its own default. Command syntax is configurable in config/providers.example.yaml. The templates use the providers' documented print/exec modes.

## Direct API access

API support is retained as a first-class capability. DeepSeek is included and enabled in the example configuration.

| Provider | API endpoint | Environment variable | Default model |
|---|---|---|---|
| DeepSeek | https://api.deepseek.com/chat/completions | DEEPSEEK_API_KEY | deepseek-v4-pro |

Set DEEPSEEK_MODEL=deepseek-flash to select the flash model, or pass --model for a one-request override. The CLI loads .env from the current working directory. The adapter reads the key from the environment at request time and never writes it to configuration or response metadata.

DeepSeek's official Chat Completions endpoint accepts the standard messages array and bearer-key authentication. See the [official API reference](https://api-docs.deepseek.com/api/create-chat-completion/).

## Selection policy

1. Use the task route selected by the user or local routing configuration.
2. Prefer subscription CLI for providers configured that way.
3. Keep API providers available for tasks that require them or when explicitly selected.
4. Do not silently switch from a failed subscription request to a paid API request.
5. Log provider/model identifiers and usage metadata, but never log authorization headers or secrets.

## Cost and quota controls

The initial default is fallback_policy: manual_only. The router rejects automatic fallback policies until an explicit budget ceiling and user opt-in are implemented.
