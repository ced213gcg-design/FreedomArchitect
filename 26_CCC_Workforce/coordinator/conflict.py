PRECEDENCE = [
    "HARD_SECURITY_LEGAL_HUMAN_AUTHORITY",
    "VERIFIED_LEDGER_LIVE_EVIDENCE",
    "CURRENT_RATIFIED_CANON_MANIFEST",
    "RELEASE_TEST_EVIDENCE",
    "WORKER_ANALYSIS",
    "UNVERIFIED_INFERENCE",
]

def resolve_claims(claims: list[dict]):
    if not claims:
        return {"status": "NO_CLAIMS", "winner": None, "deadlock": False}
    ranked = sorted(claims, key=lambda c: PRECEDENCE.index(c.get("authority_level", "UNVERIFIED_INFERENCE")))
    best_rank = PRECEDENCE.index(ranked[0].get("authority_level", "UNVERIFIED_INFERENCE"))
    top = [c for c in ranked if PRECEDENCE.index(c.get("authority_level", "UNVERIFIED_INFERENCE")) == best_rank]
    facts = {str(c.get("fact")) for c in top}
    if len(facts) > 1:
        return {"status": "VISIBLE_DEADLOCK", "winner": None, "deadlock": True, "claims": top, "next_owner": "command", "human_decision_required": True}
    return {"status": "RESOLVED", "winner": top[0], "deadlock": False, "competing_claims": ranked[1:]}
