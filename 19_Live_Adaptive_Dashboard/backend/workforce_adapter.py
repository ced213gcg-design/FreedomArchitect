from pathlib import Path
import yaml

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
WORKFORCE_ROOT = ROOT / "26_CCC_Workforce"

class WorkforceAdapter:
    def __init__(self, root=WORKFORCE_ROOT):
        self.root = Path(root)

    def _yaml(self, name):
        return yaml.safe_load((self.root / name).read_text(encoding="utf-8")) or {}

    def _workers(self):
        return self._yaml("workforce.yaml").get("workers", [])

    def list_workers(self):
        rows = []
        for worker in self._workers():
            rows.append({
                **worker,
                "current_objective": "UNASSIGNED",
                "progress": None,
                "evidence": "DECLARED_CONFIG_ONLY",
                "pressure_loss": None,
                "cost_today": None,
                "last_report": None,
                "blocker": "RUNTIME_EVIDENCE_PENDING",
                "next_action": "P0_IMPLEMENT_AND_VALIDATE",
                "next_owner": worker["id"],
                "runtime_validation": "UNKNOWN",
            })
        return rows

    def get_worker(self, worker_id):
        return next((w for w in self.list_workers() if w["id"] == worker_id), None)

    def shift(self, worker_id):
        worker = self.get_worker(worker_id)
        if not worker:
            return None
        policy = self._yaml("shift-policy.yaml")
        return {"worker": worker_id, "shift": worker["shift"], "formal_reports_per_shift": policy["formal_reports_per_shift"], "formal_report_types": policy["formal_report_types"], "runtime_reports": [], "validation": "POLICY_DECLARED_RUNTIME_REPORTS_NOT_YET_INGESTED"}

    def health(self, worker_id):
        worker = self.get_worker(worker_id)
        if not worker:
            return None
        return {"worker": worker_id, "configured_state": worker["state"], "runtime_health": "UNKNOWN", "fallback_required_if_offline": True, "validation": "DECLARED_CONFIG_NOT_LIVE_TELEMETRY"}

    def pressure(self):
        return {"state": "INCUBATE", "workers": [{"worker": w["id"], "pressure_loss": None, "validation": "RUNTIME_EVIDENCE_REQUIRED"} for w in self._workers()], "system_weakest": None, "validation": "NO_RUNTIME_WORKFORCE_PRESSURE_EVIDENCE"}

    def cost(self):
        return {"state": "INCUBATE", "total_today": None, "workers": [{"worker": w["id"], "cost_today": None} for w in self._workers()], "validation": "NO_RUNTIME_COST_EVIDENCE"}

    def handoffs(self):
        return {"handoffs": [], "validation": "NO_RUNTIME_HANDOFF_EVENTS_INGESTED"}

    def task_request(self, worker_id, payload):
        worker = self.get_worker(worker_id)
        if not worker:
            return None
        approval_required = bool(payload.get("approval_required", False))
        return {"status": "PENDING_HUMAN_APPROVAL" if approval_required else "ROUTED_INTERNAL_REQUEST", "worker": worker_id, "task": payload, "executed": False, "authority": "REQUEST_ONLY", "validation": "TASK_REQUEST_DOES_NOT_BYPASS_POLICY"}
