from __future__ import annotations
import hashlib, json, os
from pathlib import Path

REQUIRED = [
    "event_id","timestamp","source","owner","organ","run_id","event_type",
    "previous_state","new_state","change","validation","provenance",
    "artifact_hashes","synthetic","financial_classification","notes"
]

def canonical_bytes(record: dict) -> bytes:
    return json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def compute_hash(record: dict) -> str:
    payload = {k:v for k,v in record.items() if k != "event_hash"}
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()

def _read_records(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records=[]
    for idx,line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL at line {idx}: {exc}") from exc
    return records

def append_event(path: str|Path, event: dict) -> dict:
    missing=[k for k in REQUIRED if k not in event]
    if missing:
        raise ValueError("missing required ledger fields: " + ", ".join(missing))
    if not isinstance(event.get("synthetic"), bool):
        raise ValueError("synthetic must be boolean")
    path=Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    existing=_read_records(path)
    previous_hash=existing[-1].get("event_hash") if existing else None
    record=dict(event)
    record["previous_event_hash"]=previous_hash
    record["event_hash"]=compute_hash(record)
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False)+"\n")
        fh.flush()
        os.fsync(fh.fileno())
    return record

def verify_chain(path: str|Path) -> dict:
    path=Path(path)
    records=_read_records(path)
    previous=None
    defects=[]
    for index, record in enumerate(records):
        if record.get("previous_event_hash") != previous:
            defects.append({"index":index,"defect":"previous_event_hash_mismatch"})
        expected=compute_hash(record)
        if record.get("event_hash") != expected:
            defects.append({"index":index,"defect":"event_hash_mismatch"})
        previous=record.get("event_hash")
    return {"ok": not defects, "events": len(records), "defects": defects, "head_hash": previous}

def recent(path: str|Path, limit: int=25) -> list[dict]:
    return _read_records(Path(path))[-max(0,limit):]
