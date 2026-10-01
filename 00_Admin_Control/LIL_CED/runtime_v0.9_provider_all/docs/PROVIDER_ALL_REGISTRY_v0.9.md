# Lil Ced Provider-All Registry — v0.9

**Human Command:** Provider = ALL  
**Runtime:** Lil Ced standalone HP core  
**Policy:** All registered providers may be selected; only one model call may be in flight at a time. No provider is treated as ready without its own local credential/configuration.

## Registered providers

| Provider | Adapter | Credential env | Default model / configuration |
|---|---|---|---|
| Anthropic | native Anthropic SDK | ANTHROPIC_API_KEY | claude-sonnet-5-5 |
| OpenAI | native OpenAI Responses SDK | OPENAI_API_KEY | gpt-6-astra |
| Google Gemini | Google GenAI SDK | GEMINI_API_KEY | gemini-3.8-flash |
| xAI / Grok | OpenAI-compatible SDK | XAI_API_KEY | grok-4.7; https://api.x.ai/v1 |
| Generic OpenAI-compatible | OpenAI SDK with custom base URL | COMPAT_API_KEY | COMPAT_MODEL + COMPAT_BASE_URL required |
| Ollama local | local HTTP adapter | none | OLLAMA_MODEL required; default endpoint http://127.0.0.1:11434 |

## Routing
Default mode is `all`.
Routing priority:
1. anthropic
2. openai
3. google
4. xai
5. compatible
6. ollama

"All" means all registered providers are eligible. It does **not** mean fan-out to every provider for each prompt. That preserves the adopted one-call-at-a-time rule and prevents uncontrolled spend.

Human Command may change routing in the private terminal:
```
/providers
/provider all
/provider anthropic
/provider openai
/provider google
/provider xai
/provider compatible
/provider ollama
```

## Credential boundary
Credentials belong only in:
`~/.config/lilced/secrets.env`

Permissions remain 0600. Keys are never committed to GitHub, copied into the CCC cabinet, stored in memory, written to receipts, or printed by `/providers`.

## Current official API grounding
- OpenAI: current official Python examples use the OpenAI SDK and Responses API.
- Google Gemini: current official Python examples use `google-genai` and `client.models.generate_content`.
- xAI: official API documentation states the inference API is OpenAI-compatible; the inference base URL is `https://api.x.ai`, and the OpenAI-compatible v1 client route is supported.
- Anthropic: Lil Ced retains the already-adopted native Anthropic SDK lane.
- Generic OpenAI-compatible and Ollama are extensibility lanes; their endpoints/models are not invented when configuration is missing.

## Truth rule
INSTALLED != CONFIGURED
CONFIGURED != REACHABLE
REACHABLE != AUTHORIZED FOR A TASK
EXECUTED != VERIFIED

A provider without required configuration reports `UNCONFIGURED`.