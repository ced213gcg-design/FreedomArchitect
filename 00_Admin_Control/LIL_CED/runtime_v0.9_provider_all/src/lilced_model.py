from lilced_providers import ask_with_provider, statuses, configured_names

PROVIDER_MODE = "all"
MODEL_ID = "provider-all"

def configured():
    return bool(configured_names())

def provider_statuses():
    return statuses()

def ask(prompt: str, provider: str = PROVIDER_MODE):
    text, used = ask_with_provider(prompt, provider=provider)
    return text, used