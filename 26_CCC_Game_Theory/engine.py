from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4

ALLOWED_RECOMMENDATIONS = {
    "ACT", "HOLD", "DEFER", "NO_PLAY", "SEEK_EVIDENCE", "COUNTERMOVE", "RETURN_TO_BETA"
}
HARD_CONTROL_ORDER = (
    "SECURITY_LEGAL_HUMAN",
    "VERIFIED_LEDGER_LIVE_EVIDENCE",
    "RATIFIED_CANON_MANIFEST",
    "RELEASE_TEST_EVIDENCE",
    "WORKER_ANALYSIS",
    "UNVERIFIED_INFERENCE",
)

REQUIRED = (
    "players", "objectives", "constraints", "information_by_player", "information_asymmetry",
    "strategies", "costs", "payoffs", "likely_response", "second_order_response",
    "repeated_game_effects", "reputation_cooperation_effects", "hard_controls",
    "no_play_option", "evidence_change_trigger"
)

@dataclass(frozen=True)
class AnalysisError(Exception):
    message: str


def _missing(payload: dict) -> list[str]:
    return [field for field in REQUIRED if field not in payload or payload[field] in (None, "", [], {})]


def analyze(payload: dict) -> dict:
    """Return an advisory strategic analysis. Never executes or writes Ledger truth."""
    missing = _missing(payload)
    if missing:
        return {
            "status": "HOLD",
            "recommendation": "SEEK_EVIDENCE",
            "reason": "missing_required_strategic_fields",
            "missing": missing,
            "authority": "ADVISORY_ONLY",
            "can_execute": False,
            "can_write_verified_ledger_truth": False,
        }

    hard_controls = [str(x).upper() for x in payload.get("hard_controls", [])]
    blocking = [x for x in hard_controls if x.startswith("BLOCK_") or x in {"SECURITY_HOLD", "LEGAL_HOLD", "HUMAN_HOLD"}]

    if blocking:
        recommendation = "HOLD"
        reason = "hard_control_precedence"
    elif payload.get("evidence_confidence", 1.0) < 0.5:
        recommendation = "SEEK_EVIDENCE"
        reason = "insufficient_evidence_confidence"
    else:
        requested = str(payload.get("proposed_recommendation", "ACT")).upper()
        recommendation = requested if requested in ALLOWED_RECOMMENDATIONS else "DEFER"
        reason = "advisory_strategy_evaluation"

    return {
        "analysis_id": payload.get("analysis_id") or f"gt-{uuid4()}",
        "players": payload["players"],
        "objectives": payload["objectives"],
        "constraints": payload["constraints"],
        "information_by_player": payload["information_by_player"],
        "information_asymmetry": payload["information_asymmetry"],
        "strategies": payload["strategies"],
        "costs": payload["costs"],
        "payoffs": payload["payoffs"],
        "likely_response": payload["likely_response"],
        "second_order_response": payload["second_order_response"],
        "repeated_game_effects": payload["repeated_game_effects"],
        "reputation_cooperation_effects": payload["reputation_cooperation_effects"],
        "hard_controls": payload["hard_controls"],
        "hard_control_precedence": list(HARD_CONTROL_ORDER),
        "no_play_option": payload["no_play_option"],
        "evidence_change_trigger": payload["evidence_change_trigger"],
        "recommendation": recommendation,
        "reason": reason,
        "will_this_work": payload.get("will_this_work") or "CONDITIONAL_ON_VERIFIED_ASSUMPTIONS_AND_CONTROLS",
        "what_happens_after_we_act": payload.get("what_happens_after_we_act") or payload["likely_response"],
        "confidence": max(0.0, min(1.0, float(payload.get("evidence_confidence", 0.5)))),
        "authority": "ADVISORY_ONLY",
        "can_execute": False,
        "can_write_verified_ledger_truth": False,
        "executed": False,
    }
