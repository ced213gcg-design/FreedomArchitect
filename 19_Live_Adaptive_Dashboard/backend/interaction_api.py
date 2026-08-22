from __future__ import annotations
from datetime import datetime, timezone
import uuid

ALLOWED_ACTIONS = {
    "SELECT_OBJECT", "OPEN_WORLD", "OPEN_VM", "OPEN_EVIDENCE", "OPEN_COMMAND_DECK",
    "CLOSE_COMMAND_DECK", "OPEN_CONTEXT_LENS", "CLOSE_CONTEXT_LENS", "RETURN_HOME",
    "CHANGE_PERFORMANCE_MODE", "OPEN_EXECUTIVE_MODE", "OPEN_OPERATOR_MODE", "REQUEST_SOC_TEST",
    "REQUEST_VM_START", "REQUEST_VM_STOP", "APPROVAL_REQUEST", "APPROVAL_RESULT",
}

CONSEQUENTIAL = {"REQUEST_SOC_TEST", "REQUEST_VM_START", "REQUEST_VM_STOP", "APPROVAL_REQUEST", "APPROVAL_RESULT"}
FORBIDDEN_KEYS = {
    "password", "passwd", "secret", "token", "private_key", "credential", "clipboard",
    "raw_key", "raw_keystroke", "keystrokes", "pointer_coordinates", "screen_capture",
}


def _contains_forbidden(value) -> bool:
    if not isinstance(value, dict):
        return False
    for key, item in value.items():
        if str(key).lower() in FORBIDDEN_KEYS:
            return True
        if isinstance(item, dict) and _contains_forbidden(item):
            return True
    return False


def validate_interaction(payload: dict) -> tuple[bool, str]:
    if not isinstance(payload, dict):
        return False, "INVALID_PAYLOAD"
    if payload.get("action_type") not in ALLOWED_ACTIONS:
        return False, "UNREGISTERED_SEMANTIC_ACTION"
    if _contains_forbidden(payload):
        return False, "FORBIDDEN_RAW_OR_SECRET_INPUT"
    for required in ("source_context", "target_object"):
        if not payload.get(required):
            return False, f"MISSING_{required.upper()}"
    return True, "SEMANTIC_INTERACTION_VALID"


def normalize_interaction(payload: dict, operator_session: str | None = None) -> dict:
    valid, reason = validate_interaction(payload)
    if not valid:
        return {"accepted": False, "reason": reason}
    action = payload["action_type"]
    consequential = action in CONSEQUENTIAL
    return {
        "accepted": True,
        "interaction_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "operator_session": operator_session or payload.get("operator_session") or "local-dashboard-session",
        "action_type": action,
        "source_context": str(payload.get("source_context")),
        "target_object": str(payload.get("target_object")),
        "requested_effect": payload.get("requested_effect"),
        "authority_required": bool(payload.get("authority_required", consequential)),
        "state_before": payload.get("state_before"),
        "state_after": payload.get("state_after"),
        "result": payload.get("result") or "REQUEST_RECORDED" if consequential else "LOCAL_TELEMETRY_RECORDED",
        "evidence_ref": payload.get("evidence_ref"),
        "run_id": payload.get("run_id"),
        "route": "LEDGER_REQUIRED" if consequential else "LOCAL_TELEMETRY_ONLY",
        "privacy": "SEMANTIC_ONLY_NO_RAW_INPUT",
    }


def interaction_contract() -> dict:
    return {
        "state": "VERIFY",
        "allowed_actions": sorted(ALLOWED_ACTIONS),
        "consequential_actions": sorted(CONSEQUENTIAL),
        "forbidden_capture": sorted(FORBIDDEN_KEYS),
        "routing": {
            "navigation_only": "LOCAL_TELEMETRY_ONLY",
            "consequential_request": "LEDGER_REQUIRED",
            "state_changing_approved_action": "LEDGER_REQUIRED",
            "private_input": "DO_NOT_CAPTURE",
        },
    }
