from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from state_store import repo_path, read_yaml

SCENARIO_REGISTRY = repo_path("config", "soc-detection-scenarios.yaml")
DEFAULT_BRIDGE = repo_path("runtime", "soc", "ccc-soc-bridge-payload.json")


def _bridge_path() -> Path:
    return Path(os.getenv("CCC_BRIDGE_PAYLOAD_PATH", str(DEFAULT_BRIDGE)))


def _load_bridge() -> dict | None:
    path = _bridge_path()
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else None
    except Exception:
        return None


def _age_seconds(timestamp: str | None) -> float | None:
    if not timestamp:
        return None
    try:
        ts = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).astimezone(timezone.utc)
        return max(0.0, (datetime.now(timezone.utc) - ts).total_seconds())
    except Exception:
        return None


def _run_has_real_evidence(row: dict) -> bool:
    if row.get("synthetic") is not False:
        return False
    refs = row.get("evidence_refs")
    return isinstance(refs, list) and any(str(ref).strip() for ref in refs)


def _scenario_state(runs: list[dict]) -> str:
    if not runs:
        return "UNKNOWN"
    if any(str(r.get("state", "")).startswith("HOLD") for r in runs):
        if not any(_run_has_real_evidence(r) for r in runs):
            return "HOLD"
    correlated = [r for r in runs if str(r.get("state", "")).upper() == "PASS" and _run_has_real_evidence(r)]
    if len(correlated) >= 3:
        return "PASS"
    if 1 <= len(correlated) <= 2:
        return "PARTIAL"
    if any(str(r.get("state", "")).upper() == "FAIL" for r in runs):
        return "FAIL"
    if any(str(r.get("state", "")).upper() == "VERIFY_CLOCK_SKEW" for r in runs):
        return "VERIFY_CLOCK_SKEW"
    if any(str(r.get("state", "")).startswith("HOLD") for r in runs):
        return "HOLD"
    return "UNKNOWN"


def scenario_summary() -> dict:
    registry = read_yaml(SCENARIO_REGISTRY)
    bridge = _load_bridge()
    all_runs = bridge.get("scenario_runs", []) if bridge else []
    rows = []
    for definition in registry.get("scenarios", []):
        sid = definition["id"]
        runs = [r for r in all_runs if isinstance(r, dict) and str(r.get("scenario_id")) == sid]
        runs = sorted(runs, key=lambda r: str(r.get("trigger_time") or ""), reverse=True)[:3]
        real_runs = sum(1 for r in runs if _run_has_real_evidence(r))
        latest = runs[0] if runs else {}
        latencies = [r.get("end_to_end_ms", r.get("latency_ms")) for r in runs]
        latencies = [float(x) for x in latencies if isinstance(x, (int, float)) and x >= 0]
        state = _scenario_state(runs)
        rows.append({
            **definition,
            "state": state,
            "runs_real": real_runs,
            "runs_required": 3,
            "sensor": latest.get("sensor") or (definition.get("expected_sensors") or [None])[0],
            "last_detection_age_seconds": _age_seconds(latest.get("detection_time") or latest.get("source_event_time")),
            "latency_ms": round(sum(latencies) / len(latencies), 2) if latencies else None,
            "evidence_count": sum(len(r.get("evidence_refs", [])) for r in runs if isinstance(r.get("evidence_refs"), list)),
            "next_action": latest.get("notes") or ("RUN_AUTHORIZED_GUEST_TRIGGER" if state in {"UNKNOWN", "PARTIAL"} else "REVIEW_EVIDENCE"),
            "run_records": runs,
            "validation": "REAL_RUN_EVIDENCE_REQUIRED",
        })
    real_scenarios = sum(1 for row in rows if row["runs_real"] > 0)
    passed = sum(1 for row in rows if row["state"] == "PASS")
    return {
        "state": "VERIFY" if bridge else "UNKNOWN",
        "bridge_present": bridge is not None,
        "scenario_count": len(rows),
        "real_scenario_count": real_scenarios,
        "pass_count": passed,
        "scenarios": rows,
        "truth_rule": "NO_REAL_SOURCE_EVIDENCE_NO_PASS",
        "acceptance_minimum_real_scenarios": 4,
    }


def scenario_trace(scenario_id: str | None = None) -> dict:
    summary = scenario_summary()
    selected = [s for s in summary["scenarios"] if scenario_id in (None, "", s["id"])]
    trace = []
    for scenario in selected:
        for run in scenario.get("run_records", []):
            trace.append({
                "scenario_id": scenario["id"],
                "run_id": run.get("run_id"),
                "trigger": run.get("trigger_time"),
                "source": run.get("source_host"),
                "target": run.get("target_host"),
                "sensor": run.get("sensor"),
                "detection": run.get("detection_time"),
                "ledger": run.get("ledger_time"),
                "dashboard": run.get("dashboard_time"),
                "latency_ms": run.get("end_to_end_ms", run.get("latency_ms")),
                "state": run.get("state", "UNKNOWN"),
                "evidence_refs": run.get("evidence_refs", []),
            })
    return {"state": summary["state"], "events": trace, "validation": "REAL_RUN_TRACE_ONLY"}


def bridge_status() -> dict:
    bridge = _load_bridge()
    if not bridge:
        return {"state": "UNKNOWN", "mode": os.getenv("CCC_BRIDGE_MODE", "FILE_FALLBACK"), "source": str(_bridge_path()), "last_real_event": None, "current_run": None}
    latest_times = []
    for row in bridge.get("scenario_runs", []):
        if isinstance(row, dict):
            latest_times.extend([row.get("detection_time"), row.get("source_event_time"), row.get("trigger_time")])
    latest_times = [x for x in latest_times if x]
    return {
        "state": "VERIFY",
        "mode": os.getenv("CCC_BRIDGE_MODE", "HTTP_LAN"),
        "source": str(_bridge_path()),
        "timestamp": bridge.get("timestamp"),
        "current_run": bridge.get("run_id"),
        "last_real_event": max(latest_times) if latest_times else None,
        "sensor_inventory_state": "AVAILABLE" if bridge.get("sensor_health") else "UNKNOWN",
        "next_action": bridge.get("next_action"),
    }


def sensor_inventory() -> dict:
    bridge = _load_bridge()
    sensors = bridge.get("sensor_health", []) if bridge else []
    return {
        "state": "AVAILABLE" if sensors else "UNKNOWN",
        "count": len(sensors),
        "sensors": sensors,
        "source": "SANITIZED_BRIDGE_PAYLOAD" if bridge else "NO_PHYSICAL_SOURCE",
    }
