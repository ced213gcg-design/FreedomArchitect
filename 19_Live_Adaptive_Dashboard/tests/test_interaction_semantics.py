from pathlib import Path
import sys

BACKEND = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND))

from interaction_api import normalize_interaction, validate_interaction


def base(action="OPEN_WORLD"):
    return {"action_type": action, "source_context": "CCC_HORIZON", "target_object": "SOC"}


def test_navigation_stays_local_telemetry():
    event = normalize_interaction(base())
    assert event["accepted"] is True
    assert event["route"] == "LOCAL_TELEMETRY_ONLY"
    assert event["authority_required"] is False


def test_consequential_request_routes_to_ledger_not_execution():
    event = normalize_interaction(base("REQUEST_SOC_TEST"))
    assert event["accepted"] is True
    assert event["route"] == "LEDGER_REQUIRED"
    assert event["authority_required"] is True
    assert event["result"] == "REQUEST_RECORDED"


def test_raw_secret_or_input_capture_is_rejected():
    payload = {**base(), "password": "do-not-capture"}
    valid, reason = validate_interaction(payload)
    assert valid is False
    assert reason == "FORBIDDEN_RAW_OR_SECRET_INPUT"


def test_unregistered_action_is_default_deny():
    valid, reason = validate_interaction(base("EXECUTE_ARBITRARY_SHELL"))
    assert valid is False
    assert reason == "UNREGISTERED_SEMANTIC_ACTION"
