from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

from soc_adapter import SocAdapter
from state_store import hosts


def _vm_rows(value: Any) -> list[dict]:
    if isinstance(value, list):
        return [row for row in value if isinstance(row, dict)]
    if isinstance(value, dict):
        if isinstance(value.get("vms"), list):
            return [row for row in value["vms"] if isinstance(row, dict)]
        rows = []
        for name, item in value.items():
            if isinstance(item, dict):
                rows.append({"name": name, **item})
        return rows
    return []


def vm_portals() -> dict:
    soc = SocAdapter().get_state()
    data = soc.get("data") if isinstance(soc.get("data"), dict) else {}
    rows = _vm_rows(data.get("vm_health"))
    portals = []

    for row in rows:
        state = str(row.get("state") or row.get("power_state") or row.get("status") or "UNKNOWN").upper()
        portals.append({
            "id": row.get("id") or row.get("name") or "unidentified-vm",
            "name": row.get("name") or row.get("id") or "UNIDENTIFIED VM",
            "role": row.get("role") or "SOC lab virtual machine",
            "host": row.get("host") or "ccc-dell-compute-01",
            "power_state": state,
            "health": row.get("health") or row.get("validation") or "UNKNOWN",
            "ip": row.get("ip") or row.get("mgmt_ip") or row.get("management_ip"),
            "cpu": row.get("cpu") or row.get("vcpu"),
            "ram": row.get("ram") or row.get("ram_gb"),
            "last_checkpoint": row.get("last_checkpoint"),
            "last_verified": row.get("timestamp") or row.get("last_verified"),
            "active_test": row.get("active_test"),
            "sensor_state": row.get("sensor_state"),
            "evidence_freshness": "STALE" if soc.get("stale") else "CURRENT",
            "validation": row.get("validation") or soc.get("validation"),
            "read_only": True,
        })

    return {
        "state": "VERIFY" if portals and soc.get("connected") else "UNKNOWN",
        "source_state": soc.get("validation"),
        "host": "ccc-dell-compute-01",
        "host_definition": hosts().get("hosts", {}).get("ccc-dell-compute-01", {}),
        "count": len(portals),
        "vms": portals,
        "read_only": True,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "reason": None if portals else "NO_VERIFIED_VM_HEALTH_IN_LIVE_STATE",
        "next_action": "VERIFY_DELL_VM_HEALTH_EVIDENCE" if not portals else "REVIEW_VM_STATE",
    }
