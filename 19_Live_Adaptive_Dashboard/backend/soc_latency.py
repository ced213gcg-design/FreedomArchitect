from __future__ import annotations
from datetime import datetime, timezone

ORDER=("trigger_time","source_event_time","detection_time","ledger_time","dashboard_time")


def _dt(value):
    if not value: return None
    return datetime.fromisoformat(str(value).replace("Z","+00:00")).astimezone(timezone.utc)


def reconcile_latency(run: dict, skew_tolerance_ms: int = 2000) -> dict:
    points={k:_dt(run.get(k)) for k in ORDER}
    present=[(k,v) for k,v in points.items() if v is not None]
    clock_skew=False
    for (_,a),(_,b) in zip(present,present[1:]):
        if (b-a).total_seconds()*1000 < -skew_tolerance_ms:
            clock_skew=True
    def diff(a,b):
        if points[a] is None or points[b] is None: return None
        value=(points[b]-points[a]).total_seconds()*1000
        return round(value,2) if value >= 0 else None
    metrics={
        "trigger_to_sensor_ms":diff("trigger_time","source_event_time"),
        "sensor_to_detection_ms":diff("source_event_time","detection_time"),
        "detection_to_ledger_ms":diff("detection_time","ledger_time"),
        "ledger_to_dashboard_ms":diff("ledger_time","dashboard_time"),
        "end_to_end_ms":diff("trigger_time","dashboard_time"),
    }
    state=str(run.get("state") or "UNKNOWN").upper()
    if clock_skew: state="VERIFY_CLOCK_SKEW"
    return {**run,**metrics,"latency_ms":metrics["end_to_end_ms"],"clock_skew":clock_skew,"state":state}
