from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SCHEMA_PATH = ROOT / "20_CCC_Living_Organism" / "schemas" / "soc-evidence-bridge.schema.json"
MAX_PAYLOAD = 1024 * 1024
FORBIDDEN_KEYS = {
    "password", "secret", "token", "api_key", "credential", "private_key",
    "shell", "command_to_execute", "script_body"
}
DEFAULT_SOURCE = "ccc-dell-compute-01"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _contains_forbidden_key(value: Any) -> str | None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).strip().lower()
            if normalized in FORBIDDEN_KEYS:
                return normalized
            found = _contains_forbidden_key(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _contains_forbidden_key(child)
            if found:
                return found
    return None


def _parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_payload(payload: dict, raw: bytes, token: str, signature: str, allowed_source: str = DEFAULT_SOURCE, max_age_seconds: int = 300) -> list[str]:
    errors: list[str] = []
    if len(raw) > MAX_PAYLOAD:
        return ["PAYLOAD_TOO_LARGE"]
    expected = hmac.new(token.encode("utf-8"), raw, hashlib.sha256).hexdigest()
    supplied = signature.removeprefix("sha256=").strip().lower()
    if not supplied or not hmac.compare_digest(expected, supplied):
        errors.append("INVALID_HMAC")
    forbidden = _contains_forbidden_key(payload)
    if forbidden:
        errors.append(f"FORBIDDEN_FIELD:{forbidden}")
    validator = Draft202012Validator(load_schema(), format_checker=FormatChecker())
    errors.extend(f"SCHEMA:{e.json_path}:{e.message}" for e in validator.iter_errors(payload))
    if payload.get("source_host") != allowed_source:
        errors.append("SOURCE_HOST_NOT_ALLOWED")
    try:
        age = abs((_utc_now() - _parse_timestamp(str(payload.get("timestamp", "")))).total_seconds())
        if age > max_age_seconds:
            errors.append("STALE_BRIDGE_PAYLOAD")
    except Exception:
        errors.append("INVALID_TIMESTAMP")
    return errors


def normalize_live_state(payload: dict) -> dict:
    evidence: list[dict] = []
    for row in payload.get("control_gates", []):
        if isinstance(row, dict):
            evidence.append({**row, "record_class": "CONTROL_GATE"})
    for row in payload.get("scenario_runs", []):
        if isinstance(row, dict):
            evidence.append({**row, "record_class": "DETECTION_SCENARIO"})
    return {
        "timestamp": payload["timestamp"],
        "run_id": payload["run_id"],
        "phase": "PHYSICAL_SOC_EVIDENCE",
        "status": "VERIFY",
        "host_health": [{"host": payload["source_host"], "state": "OBSERVED"}],
        "vm_health": payload.get("vm_health", []),
        "sensor_health": payload.get("sensor_health", []),
        "evidence": evidence,
        "evidence_refs": payload.get("evidence_refs", []),
        "next_action": payload.get("next_action", "REVIEW_PHYSICAL_EVIDENCE"),
        "bridge_mode": "HTTP_LAN",
        "bridge_schema": payload.get("schema"),
    }


def persist_payload(payload: dict, bridge_path: Path, state_path: Path) -> None:
    bridge_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    bridge_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    state_path.write_text(json.dumps(normalize_live_state(payload), indent=2) + "\n", encoding="utf-8")


class BridgeHandler(BaseHTTPRequestHandler):
    server_version = "CCC-Evidence-Bridge/1"

    def _json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path != "/health":
            self._json(404, {"status": "NOT_FOUND"})
            return
        self._json(200, {"status": "PASS", "service": "ccc-soc-evidence-bridge", "mode": "RECEIVE_ONLY", "max_payload_bytes": MAX_PAYLOAD})

    def do_POST(self) -> None:
        if self.path != "/bridge/v1/evidence":
            self._json(404, {"status": "NOT_FOUND"})
            return
        length = int(self.headers.get("Content-Length", "0") or 0)
        if length <= 0 or length > MAX_PAYLOAD:
            self._json(413, {"status": "REJECTED", "reason": "PAYLOAD_SIZE"})
            return
        token = self.server.session_token  # type: ignore[attr-defined]
        auth = self.headers.get("Authorization", "")
        if not auth.startswith("Bearer ") or not hmac.compare_digest(auth[7:], token):
            self._json(401, {"status": "REJECTED", "reason": "INVALID_BEARER"})
            return
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw)
        except Exception:
            self._json(400, {"status": "REJECTED", "reason": "INVALID_JSON"})
            return
        if not isinstance(payload, dict):
            self._json(400, {"status": "REJECTED", "reason": "OBJECT_REQUIRED"})
            return
        errors = validate_payload(
            payload,
            raw,
            token,
            self.headers.get("X-CCC-Signature", ""),
            self.server.allowed_source,  # type: ignore[attr-defined]
        )
        if errors:
            self._json(400, {"status": "REJECTED", "errors": errors})
            return
        persist_payload(payload, self.server.bridge_path, self.server.state_path)  # type: ignore[attr-defined]
        self._json(202, {"status": "ACCEPTED", "run_id": payload["run_id"], "executed": False, "authority": "EVIDENCE_ONLY"})

    def log_message(self, fmt: str, *args: object) -> None:
        return


def main() -> int:
    parser = argparse.ArgumentParser(description="CCC one-way SOC evidence receiver")
    parser.add_argument("--host", default=os.getenv("CCC_BRIDGE_BIND", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("CCC_BRIDGE_PORT", "8790")))
    parser.add_argument("--bridge-path", default=os.getenv("CCC_BRIDGE_PAYLOAD_PATH", str(ROOT / "runtime" / "soc" / "ccc-soc-bridge-payload.json")))
    parser.add_argument("--state-path", default=os.getenv("CCC_SOC_STATE_PATH", str(ROOT / "runtime" / "soc" / "ccc-soc-live-state.json")))
    args = parser.parse_args()
    token = os.getenv("CCC_BRIDGE_TOKEN", "")
    if len(token) < 32:
        print("HARD_FAIL: CCC_BRIDGE_TOKEN must be a random session value of at least 32 characters.", file=sys.stderr)
        return 2
    server = ThreadingHTTPServer((args.host, args.port), BridgeHandler)
    server.session_token = token  # type: ignore[attr-defined]
    server.allowed_source = os.getenv("CCC_BRIDGE_ALLOWED_SOURCE", DEFAULT_SOURCE)  # type: ignore[attr-defined]
    server.bridge_path = Path(args.bridge_path)  # type: ignore[attr-defined]
    server.state_path = Path(args.state_path)  # type: ignore[attr-defined]
    print(f"CCC Evidence Bridge receive-only: http://{args.host}:{args.port}/bridge/v1/evidence")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
