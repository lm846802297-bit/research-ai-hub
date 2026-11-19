# Provider authentication and access modes

Research AI Hub supports two co-equal technical access modes, with a subscription-first preference where the provider offers an official CLI suitable for the user's plan.

## Subscription-backed official CLI

| Provider | Local command entry | Login ownership |
|---|---|---|
| Codex | configurable command template | Codex CLI |
| Claude Code | configurable command template | Claude Code |
| Gemini CLI | configurable command template | Gemini CLI |

The application launches the configured executable. The user signs in through that tool's official login flow. This avoids requiring a separate API key when subscription access is supported.

Command syntax is intentionally configurable. CLI flags and subscription entitlements can change; confirm the installed version's official documentation before activating a template. The application must not imitate browser logins or extract session cookies.

## Direct API access

API support is retained as a first-class capability. DeepSeek is included in the starter configuration.

| Provider | Access mode | Environment variable |
|---|---|---|
| DeepSeek | OpenAI-compatible Chat Completions | DEEPSEEK_API_KEY |
| Generic compatible endpoint | OpenAI-compatible Chat Completions | configurable |

The API adapter reads credentials only at request time. Put keys in environment variables or a local secret manager, never in committed configuration.

## Selection policy

1. Use the task route selected by the user or local routing configuration.
2. Prefer subscription CLI for providers configured that way.
3. Keep API providers available for tasks that require them or when explicitly selected.
4. Do not silently switch from a failed subscription request to a paid API request.
5. Log the selected access mode and provider/model identifiers, but never log authorization headers or secrets.

## Cost and quota controls

The initial default is fallback_policy: manual_only. A future automatic fallback feature must require an explicit opt-in, a named fallback provider, and a configured spending ceiling.
