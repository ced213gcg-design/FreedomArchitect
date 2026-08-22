FALLBACK = {
    "command": "ORCHESTRA_LAST_VERIFIED_QUEUE_AND_HUMAN_PRIORITIZATION",
    "intelligence": "NO_NEW_EXTERNAL_SIGNAL_PROMOTION_EXISTING_VERIFIED_WORK_CONTINUES",
    "security": "CONSEQUENTIAL_RELEASE_AND_SECURITY_ACTIONS_DEFAULT_HOLD",
    "revenue": "NO_NEW_CAPITAL_OR_REVENUE_PROMOTION_WORK_WITHIN_APPROVED_BUDGET",
    "communications": "EXTERNAL_SENDS_QUEUE_DASHBOARD_REMAINS_PRIMARY_VISIBILITY",
}

def fallback_for(worker_id: str, online: bool):
    if online:
        return {"worker": worker_id, "state": "ONLINE", "fallback_active": False}
    return {"worker": worker_id, "state": "OFFLINE", "fallback_active": True, "behavior": FALLBACK[worker_id]}
