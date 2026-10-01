import os
from pathlib import Path

MODEL_ID = "claude-sonnet-5-5"
SECRETS = Path.home() / ".config/lilced/secrets.env"

def _load_secret_env():
    if not SECRETS.exists():
        return
    for raw in SECRETS.read_text(errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key and key not in os.environ:
            os.environ[key] = value

def configured():
    _load_secret_env()
    return bool(os.environ.get("ANTHROPIC_API_KEY"))

def ask(prompt: str) -> str:
    _load_secret_env()
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return "SAFE_NO_MODEL: ANTHROPIC_API_KEY is not configured."
    from anthropic import Anthropic
    client = Anthropic(api_key=key)
    msg = client.messages.create(
        model=MODEL_ID,
        max_tokens=1024,
        system=(
            "You are Lil Ced, Ced's standalone Dr.D personal operations assistant. "
            "Human Command is final consequential authority. FACT BEFORE CLAIM. "
            "UNKNOWN is not PASS. Never claim execution without evidence. "
            "Do not expose secrets. Do not perform tool actions from this model call."
        ),
        messages=[{"role": "user", "content": prompt}],
    )
    parts = [b.text for b in msg.content if getattr(b, "type", "") == "text"]
    return "\n".join(parts).strip() or "MODEL_EMPTY_RESPONSE"