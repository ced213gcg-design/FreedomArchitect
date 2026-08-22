from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from state_store import repo_path, read_yaml
from soc_adapter import SocAdapter

REGISTRY_PATH = repo_path("config", "soc-five-test-registry.yaml")


def _records_from(value: Any) -> list[dict]:
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        for key in ("tests", "missions", "records", "events"):
            if isinstance(value.get(key), list):
                return [row for row in value[key] if isinstance(row, dict)]
        return [value]
    return []


def _live_records(soc_state: dict) -> list[dict]:
    data = soc_state.get("data") if isinstance(soc_state, dict) else None
    if not isinstance(data, dict):
        return []
    rows: list[dict] = []
    for key in ("tests", "missions", "evidence", "soc_tests"):
        rows.extend(_records_from(data.get(key)))
    return rows


def _record_keys(row: dict) -> set[str]:
    values = []
    for key in ("id", "mission_id", "test_id", "key", "mission_key", "test_key", "type"):
        if row.get(key) is not None:
            values.append(str(row[key]).strip().upper())
    return set(values)


def _explicit_state(row: dict, stale: bool) -> str:
    raw = str(row.get("state") or row.get("status") or row.get("result") or "VERIFY").upper()
    if stale and raw in {"PASS", "READY", "VERIFIED"}:
        return "VERIFY"
    if raw in {"PASS", "READY", "VERIFIED", "VERIFY", "HOLD", "FAIL", "UNKNOWN", "STALE"}:
        return raw
    return "VERIFY"


def five_missions() -> dict:
    registry = read_yaml(REGISTRY_PATH)
    soc = SocAdapter().get_state()
    records = _live_records(soc)
    missions = []

    for definition in registry.get("missions", []):
        wanted = {str(definition.get("id", "")).upper(), str(definition.get("key", "")).upper()}
        evidence = next((row for row in records if wanted & _record_keys(row)), None)
        if evidence is None:
            missions.append({
                **definition,
                "state": "UNKNOWN",
                "result": None,
                "run_id": soc.get("last_valid_run_id"),
                "last_verified": None,
                "validation": "LIVE_EVIDENCE_NOT_REGISTERED",
                "evidence_ref": None,
                "source_state": soc.get("validation"),
                "next_action": "COLLECT_AND_BIND_LIVE_EVIDENCE",
            })
            continue

        missions.append({
            **definition,
            "state": _explicit_state(evidence, bool(soc.get("stale", True))),
            "result": evidence.get("result") or evidence.get("status"),
            "run_id": evidence.get("run_id") or soc.get("last_valid_run_id"),
            "last_verified": evidence.get("timestamp") or evidence.get("last_verified"),
            "validation": evidence.get("validation") or "LIVE_EVIDENCE_PRESENT_UNCLASSIFIED",
            "evidence_ref": evidence.get("evidence_ref") or evidence.get("artifact") or evidence.get("artifact_hash"),
            "source_state": soc.get("validation"),
            "latency_ms": evidence.get("latency_ms"),
            "owner": evidence.get("owner") or "soc",
            "next_action": evidence.get("next_action") or "REVIEW_EVIDENCE",
        })

    proven = sum(1 for row in missions if row["state"] in {"PASS", "READY", "VERIFIED"})
    return {
        "state": "VERIFY" if soc.get("connected") else "UNKNOWN",
        "source_state": soc.get("validation"),
        "run_id": soc.get("last_valid_run_id"),
        "count": len(missions),
        "proven_count": proven,
        "missions": missions,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "truth_rule": "NO_LIVE_EVIDENCE_NO_PASS",
    }


def mission_trace() -> dict:
    payload = five_missions()
    events = []
    for mission in payload["missions"]:
        if not mission.get("last_verified") and not mission.get("evidence_ref"):
            continue
        events.append({
            "timestamp": mission.get("last_verified"),
            "source": "dell-soc-live-state",
            "target": mission.get("id"),
            "type": "SOC_MISSION_EVIDENCE",
            "state": mission.get("state"),
            "validation": mission.get("validation"),
            "evidence_ref": mission.get("evidence_ref"),
            "run_id": mission.get("run_id"),
        })
    return {
        "state": payload["state"],
        "run_id": payload["run_id"],
        "events": events,
        "validation": "TRACE_FROM_BOUND_LIVE_EVIDENCE_ONLY",
    }
