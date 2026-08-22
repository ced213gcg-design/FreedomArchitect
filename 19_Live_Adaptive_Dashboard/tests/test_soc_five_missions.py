from pathlib import Path
import sys

BACKEND = Path(__file__).resolve().parents[1] / "backend"
sys.path.insert(0, str(BACKEND))

import soc_mission_adapter


class MissingSoc:
    def get_state(self):
        return {"state":"UNKNOWN","connected":False,"stale":True,"validation":"MISSING_SOURCE","last_valid_run_id":None}


class OneProvenSoc:
    def get_state(self):
        return {
            "state":"VERIFY","connected":True,"stale":False,"validation":"VALID_CONTRACT","last_valid_run_id":"run-1",
            "data":{"evidence":[{"mission_id":"SOC-03","result":"PASS","run_id":"run-1","timestamp":"2026-08-22T10:00:00+00:00","evidence_ref":"sha256:fixture","validation":"VERIFIED_TEST_EVIDENCE"}]}
        }


def test_missing_live_source_never_invents_pass(monkeypatch):
    monkeypatch.setattr(soc_mission_adapter, "SocAdapter", lambda: MissingSoc())
    payload = soc_mission_adapter.five_missions()
    assert payload["count"] == 5
    assert payload["proven_count"] == 0
    assert all(row["state"] == "UNKNOWN" for row in payload["missions"])


def test_only_bound_evidence_can_promote_one_mission(monkeypatch):
    monkeypatch.setattr(soc_mission_adapter, "SocAdapter", lambda: OneProvenSoc())
    payload = soc_mission_adapter.five_missions()
    assert payload["count"] == 5
    assert payload["proven_count"] == 1
    proven = [row for row in payload["missions"] if row["state"] == "PASS"]
    assert [row["id"] for row in proven] == ["SOC-03"]
    unknown = [row for row in payload["missions"] if row["state"] == "UNKNOWN"]
    assert len(unknown) == 4
