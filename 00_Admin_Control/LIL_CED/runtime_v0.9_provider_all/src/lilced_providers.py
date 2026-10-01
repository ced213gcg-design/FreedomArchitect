import json
import os
import urllib.request
from pathlib import Path

SECRETS = Path.home() / ".config/lilced/secrets.env"

SYSTEM_PROMPT = (
    "You are Lil Ced, Ced's standalone Dr.D personal operations assistant. "
    "Human Command is final consequential authority. FACT BEFORE CLAIM. "
    "UNKNOWN is not PASS. Never claim execution without evidence. "
    "Do not expose secrets. Do not perform tool actions from a model-only call."
)

PROVIDERS = {
    "anthropic": {
        "key_env": "ANTHROPIC_API_KEY",
        "model_env": "ANTHROPIC_MODEL",
        "default_model": "claude-sonnet-5-5",
        "adapter": "anthropic",
    },
    "openai": {
        "key_env": "OPENAI_API_KEY",
        "model_env": "OPENAI_MODEL",
        "default_model": "gpt-6-astra",
        "adapter": "openai",
    },
    "google": {
        "key_env": "GEMINI_API_KEY",
        "model_env": "GEMINI_MODEL",
        "default_model": "gemini-3.8-flash",
        "adapter": "google",
    },
    "xai": {
        "key_env": "XAI_API_KEY",
        "model_env": "XAI_MODEL",
        "default_model": "grok-4.7",
        "adapter": "openai_compatible",
        "base_url": "https://api.x.ai/v1",
    },
    "compatible": {
        "key_env": "COMPAT_API_KEY",
        "model_env": "COMPAT_MODEL",
        "default_model": "",
        "adapter": "openai_compatible",
        "base_url_env": "COMPAT_BASE_URL",
    },
    "ollama": {
        "key_env": None,
        "model_env": "OLLAMA_MODEL",
        "default_model": "",
        "adapter": "ollama",
        "base_url_env": "OLLAMA_BASE_URL",
        "default_base_url": "http://127.0.0.1:11434",
    },
}

PRIORITY = ["anthropic", "openai", "google", "xai", "compatible", "ollama"]

def load_secret_env():
    if not SECRETS.exists():
        return
    for raw in SECRETS.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key and key not in os.environ:
            os.environ[key] = value

def _model(name):
    spec = PROVIDERS[name]
    return os.environ.get(spec["model_env"], spec["default_model"]).strip()

def _base_url(name):
    spec = PROVIDERS[name]
    if spec.get("base_url"):
        return spec["base_url"]
    env = spec.get("base_url_env")
    return os.environ.get(env, spec.get("default_base_url", "")).strip() if env else ""

def provider_status(name):
    load_secret_env()
    spec = PROVIDERS[name]
    model = _model(name)
    if name == "ollama":
        state = "CONFIGURED" if model else "UNCONFIGURED"
    else:
        key = os.environ.get(spec["key_env"], "") if spec["key_env"] else ""
        state = "CONFIGURED" if key and model else "UNCONFIGURED"
    return {
        "provider": name,
        "state": state,
        "model": model or None,
        "adapter": spec["adapter"],
        "base_url": _base_url(name) or None,
        "credential_env": spec.get("key_env"),
    }

def statuses():
    return {name: provider_status(name) for name in PRIORITY}

def configured_names():
    return [n for n in PRIORITY if provider_status(n)["state"] == "CONFIGURED"]

def _anthropic(prompt, model, key):
    from anthropic import Anthropic
    client = Anthropic(api_key=key)
    msg = client.messages.create(
        model=model,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    parts = [b.text for b in msg.content if getattr(b, "type", "") == "text"]
    return "\n".join(parts).strip() or "MODEL_EMPTY_RESPONSE"

def _openai(prompt, model, key, base_url=None):
    from openai import OpenAI
    client = OpenAI(api_key=key, base_url=base_url) if base_url else OpenAI(api_key=key)
    response = client.responses.create(
        model=model,
        instructions=SYSTEM_PROMPT,
        input=prompt,
    )
    return (getattr(response, "output_text", "") or "").strip() or "MODEL_EMPTY_RESPONSE"

def _google(prompt, model, key):
    from google import genai
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model=model,
        contents=f"{SYSTEM_PROMPT}\n\nUSER:\n{prompt}",
    )
    return (getattr(response, "text", "") or "").strip() or "MODEL_EMPTY_RESPONSE"

def _ollama(prompt, model, base_url):
    payload = json.dumps({
        "model": model,
        "prompt": f"{SYSTEM_PROMPT}\n\nUSER:\n{prompt}",
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        base_url.rstrip("/") + "/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        body = json.loads(r.read().decode())
    return str(body.get("response", "")).strip() or "MODEL_EMPTY_RESPONSE"

def ask_with_provider(prompt, provider="all"):
    load_secret_env()
    allowed = PRIORITY if provider in {"all", "auto"} else [provider]
    unknown = [p for p in allowed if p not in PROVIDERS]
    if unknown:
        return f"SAFE_NO_MODEL: unknown provider {unknown[0]}.", None
    available = [p for p in allowed if provider_status(p)["state"] == "CONFIGURED"]
    if not available:
        return "SAFE_NO_MODEL: no configured provider is available.", None

    name = available[0]
    spec = PROVIDERS[name]
    model = _model(name)
    try:
        if name == "anthropic":
            text = _anthropic(prompt, model, os.environ["ANTHROPIC_API_KEY"])
        elif name == "openai":
            text = _openai(prompt, model, os.environ["OPENAI_API_KEY"])
        elif name == "google":
            text = _google(prompt, model, os.environ["GEMINI_API_KEY"])
        elif name == "xai":
            text = _openai(prompt, model, os.environ["XAI_API_KEY"], _base_url(name))
        elif name == "compatible":
            text = _openai(prompt, model, os.environ["COMPAT_API_KEY"], _base_url(name))
        elif name == "ollama":
            text = _ollama(prompt, model, _base_url(name))
        else:
            return f"SAFE_NO_MODEL: adapter missing for {name}.", None
        return text, name
    except Exception as exc:
        return f"PROVIDER_ERROR[{name}]: {type(exc).__name__}: {exc}", name