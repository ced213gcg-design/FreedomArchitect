#!/usr/bin/env python3
import asyncio, json, os, hashlib, stat
from datetime import datetime, timezone
from pathlib import Path

APP = Path.home() / "LilCed/app"
WORKSPACE = Path.home() / "LilCed/workspace"
CABINET = Path.home() / "LIL_CED_CABINET"
CCC = Path.home() / "CCC_FILING_CABINET/14_LIL_CED"
STATE_DIR = Path.home() / ".local/state/lilced"
SOCKET = STATE_DIR / "lilced.sock"
STATE_FILE = STATE_DIR / "state.json"
RECEIPTS = CABINET / "11_RECEIPTS_AND_HASHES"
BRAIN = Path.home() / "CCC_FILING_CABINET/09_GITHUB_AUTHORITATIVE_LINEAGE/FreedomArchitect/00_Admin_Control/MY_OG_CCC_BRAIN.md"
EXPECTED_BRAIN_BLOB = "9f0aadc36abb871f3ca1a70aaeca29833477529a"
TOOLS = ["read", "workspace-write", "hash", "status"]
READ_ROOTS = [WORKSPACE, CABINET, Path.home()/"CCC_FILING_CABINET", Path.home()/".config/lilced"]
SECRET = Path.home()/".config/lilced/secrets.env"

from lilced_graph import analyze
from lilced_model import ask, configured, provider_statuses, MODEL_ID

STATE_DIR.mkdir(parents=True, exist_ok=True)
RECEIPTS.mkdir(parents=True, exist_ok=True)

def utc():
    return datetime.now(timezone.utc).isoformat()

def git_blob(path: Path):
    data = path.read_bytes()
    hdr = f"blob {len(data)}\0".encode()
    return hashlib.sha1(hdr + data).hexdigest()

def load_state():
    if not STATE_FILE.exists():
        return {"frozen": False, "hold": None, "provider": "all", "started": utc()}
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {"frozen": True, "hold": "STATE_FILE_INVALID", "provider": "all", "started": utc()}

def save_state(s):
    STATE_FILE.write_text(json.dumps(s, indent=2) + "\n")

STATE = load_state()

def receipt(kind, objective, final_state, details=None):
    rid = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    body = {
        "schema": "lilced.receipt.v1",
        "task_id": f"{kind}-{rid}",
        "utc": utc(),
        "human_objective": objective,
        "final_state": final_state,
        "model_id": MODEL_ID,
        "tools": TOOLS,
        "details": details or {},
    }
    path = RECEIPTS / f"{body['task_id']}.json"
    path.write_text(json.dumps(body, indent=2) + "\n")
    return path

def is_under(path: Path, roots):
    p = path.expanduser().resolve()
    return any(p == r.resolve() or r.resolve() in p.parents for r in roots)

def status():
    brain_state = "MISSING"
    if BRAIN.exists():
        try:
            brain_state = "PASS" if git_blob(BRAIN) == EXPECTED_BRAIN_BLOB else "HOLD_MISMATCH"
        except Exception:
            brain_state = "HOLD_READ_ERROR"
    return {
        "name": "Lil Ced",
        "version": "0.9-provider-all",
        "mode": "FROZEN" if STATE.get("frozen") else ("HOLD" if STATE.get("hold") else ("READY" if configured() else "SAFE_NO_MODEL")),
        "model": MODEL_ID,
        "model_configured": configured(),
        "provider_mode": STATE.get("provider", "all"),
        "providers": provider_statuses(),
        "socket": str(SOCKET),
        "brain_integrity": brain_state,
        "tools": TOOLS,
        "shell": "DISABLED",
        "closed_lanes": ["Letta","Open Interpreter","Goose","OpenHands","CrewAI","Microsoft Agent Framework","n8n","Hermes","OpenClaw","voice","HUD","local LLM"],
    }

def deny(objective, reason):
    p = receipt("DENIED", objective, "DENIED", {"reason": reason})
    return f"DENIED: {reason}\nRECEIPT={p}"

def handle(line: str):
    line = line.strip()
    if not line:
        return ""
    if line == "/status":
        return json.dumps(status(), indent=2)
    if line == "/providers":
        return json.dumps(provider_statuses(), indent=2)
    if line.startswith("/provider "):
        name = line.split(None, 1)[1].strip().lower()
        allowed = set(provider_statuses()) | {"all", "auto"}
        if name not in allowed:
            return deny(line, f"Unknown provider: {name}")
        STATE["provider"] = "all" if name == "auto" else name
        save_state(STATE)
        p = receipt("PROVIDER", line, "PASS", {"provider_mode": STATE["provider"]})
        return f"PROVIDER_MODE={STATE['provider']}\nRECEIPT={p}"
    if line == "/brain":
        return f"BRAIN={BRAIN}\nEXPECTED_BLOB={EXPECTED_BRAIN_BLOB}\nSTATE={status()['brain_integrity']}"
    if line == "/tools":
        return "ALPHA_TOOLS=" + ", ".join(TOOLS) + "\nSHELL=DISABLED"
    if line == "/memory":
        files = sorted((APP/"memory").rglob("*"))
        return "\n".join(str(p) for p in files if p.is_file()) or "MEMORY_EMPTY"
    if line == "/receipts":
        files = sorted(RECEIPTS.glob("*.json"))[-10:]
        return "\n".join(str(p) for p in files) or "NO_RECEIPTS"
    if line in {"/mcp", "/workers"}:
        return "CLOSED: registered lane not active in alpha."
    if line == "/shell" or line.startswith("/shell "):
        return deny(line, "Raw shell is disabled in alpha.")
    if line == "/freeze":
        STATE["frozen"] = True; STATE["hold"] = "HUMAN_FREEZE"; save_state(STATE)
        p = receipt("FREEZE", line, "HOLD")
        return f"FROZEN\nRECEIPT={p}"
    if line == "/resume":
        STATE["frozen"] = False; STATE["hold"] = None; save_state(STATE)
        p = receipt("RESUME", line, "PASS")
        return f"RESUMED\nRECEIPT={p}"
    if line.startswith("/mit "):
        result = analyze(line[5:])
        gate = "ON" if result.get("mit_gate") else "OFF"
        return f"MIT_GATE={gate}\nFINAL_STATE={result.get('final_state')}\nWORKSHEET={CABINET/'03_MIT_GATE/worksheet.md'}"
    if line.startswith("/hash "):
        p = Path(line[6:]).expanduser()
        if not p.is_file() or not is_under(p, READ_ROOTS):
            return deny(line, "Path is outside approved read roots or is not a file.")
        return hashlib.sha256(p.read_bytes()).hexdigest() + "  " + str(p)
    if line.startswith("/read "):
        p = Path(line[6:]).expanduser()
        if p == SECRET or not p.is_file() or not is_under(p, READ_ROOTS):
            return deny(line, "Read denied by root/secret policy.")
        data = p.read_text(errors="replace")
        return data[:12000]
    if line.startswith("/write "):
        if "|" not in line:
            return "USAGE: /write relative/path | text"
        left, data = line[7:].split("|", 1)
        target = (WORKSPACE / left.strip()).resolve()
        if not is_under(target, [WORKSPACE]):
            return deny(line, "Workspace boundary.")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(data.lstrip())
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        p = receipt("WRITE", line[:200], "PASS", {"path": str(target), "sha256": digest})
        return f"WROTE={target}\nSHA256={digest}\nRECEIPT={p}"
    if STATE.get("frozen"):
        return "HOLD: Lil Ced is frozen. /status /brain /receipts remain available."
    flow = analyze(line)
    if flow.get("mit_gate"):
        p = receipt("MIT_HOLD", line[:300], "HOLD", {"worksheet": str(CABINET/"03_MIT_GATE/worksheet.md")})
        return f"{flow.get('response')}\nRECEIPT={p}"
    answer, used = ask(line, provider=STATE.get("provider", "all"))
    if used:
        return f"PROVIDER={used}\n{answer}"
    return answer

async def client(reader, writer):
    try:
        data = await reader.readline()
        response = handle(data.decode(errors="replace"))
        writer.write((response + "\n").encode())
        await writer.drain()
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    if SOCKET.exists():
        SOCKET.unlink()
    server = await asyncio.start_unix_server(client, path=str(SOCKET))
    os.chmod(SOCKET, stat.S_IRUSR | stat.S_IWUSR)
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    asyncio.run(main())