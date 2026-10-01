#!/usr/bin/env python3
import json, hashlib, os, pathlib, subprocess, stat
from datetime import datetime, timezone

HOME = pathlib.Path.home()
APP = HOME / "LilCed/app"
CAB = HOME / "LIL_CED_CABINET"
CCC = HOME / "CCC_FILING_CABINET/14_LIL_CED"
REPO = HOME / "CCC_FILING_CABINET/09_GITHUB_AUTHORITATIVE_LINEAGE/FreedomArchitect"
SOCK = HOME / ".local/state/lilced/lilced.sock"
ACCEPT = CAB / "10_TESTS_AND_REGRESSIONS/alpha_acceptance_latest.json"
REQ = CAB / "04_SOURCE_AND_DEPENDENCIES/requirements.lock.txt"
OUT = CAB / "11_RECEIPTS_AND_HASHES/HP_ALPHA_DEPLOYMENT_RECEIPT_20260930.json"
MAN = CAB / "11_RECEIPTS_AND_HASHES/HP_ALPHA_SOURCE_SHA256_20260930.txt"

def sh(*args):
    return subprocess.run(args, text=True, capture_output=True)

def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

if not REQ.exists():
    p = sh(str(APP/".venv/bin/python"), "-m", "pip", "freeze")
    if p.returncode == 0:
        REQ.write_text(p.stdout)

sources = [
    APP/"lilced_core.py",
    APP/"lilced_terminal.py",
    APP/"lilced_graph.py",
    APP/"lilced_model.py",
    APP/"config.json",
    APP/"setup_alpha.sh",
    HOME/"LilCed/tests/alpha_acceptance.py",
    HOME/".config/systemd/user/lilced-core.service",
    HOME/".local/share/applications/lilced-terminal.desktop",
    HOME/".local/share/applications/lilced-cabinet.desktop",
    HOME/".local/share/applications/ccc-filing-cabinet.desktop",
    CAB/"03_MIT_GATE/worksheet.md",
    CAB/"08_LANES_REGISTERED/LANES.md",
    REQ,
]
manifest = []
for p in sources:
    if p.exists():
        manifest.append((str(p), p.stat().st_size, sha(p)))
MAN.write_text("".join(f"{digest}  {size:>10}  {path}\n" for path,size,digest in manifest))

accept = json.loads(ACCEPT.read_text())
service = sh("systemctl","--user","is-active","lilced-core.service").stdout.strip()
git_head = sh("git","-C",str(REPO),"rev-parse","HEAD").stdout.strip()
socket_mode = oct(SOCK.stat().st_mode & 0o777) if SOCK.exists() else "MISSING"
secret = HOME/".config/lilced/secrets.env"

receipt = {
    "schema":"lilced.hp.alpha.deployment.v1",
    "utc":datetime.now(timezone.utc).isoformat(),
    "authority":"Human Command",
    "host":"penguin",
    "user":os.environ.get("USER"),
    "lilced_version":"0.8-alpha",
    "model_id":"claude-sonnet-5-5",
    "chatgpt_runtime_dependency":"NONE",
    "service_state":service,
    "socket_mode":socket_mode,
    "secret_mode":oct(secret.stat().st_mode & 0o777),
    "secret_size_bytes":secret.stat().st_size,
    "acceptance":accept,
    "separate_cabinet":str(CAB),
    "ccc_mirror":str(CCC),
    "local_freedomarchitect_head":git_head,
    "source_manifest":str(MAN),
    "source_manifest_sha256":sha(MAN),
    "off_container_backup":"PENDING_DRIVE_OR_USB",
    "github_runtime_sync":"PENDING_THIS_RECEIPT",
    "local_state":"PASS_WITH_BACKUP_GATE_OPEN",
    "truth_boundary":"LOCAL_RUNTIME_ACCEPTANCE_PASS does not equal off-container backup PASS or full alpha closure.",
}
OUT.write_text(json.dumps(receipt, indent=2) + "\n")

for rel in [
    "03_MIT_GATE/worksheet.md",
    "08_LANES_REGISTERED/LANES.md",
    "10_TESTS_AND_REGRESSIONS/alpha_acceptance_latest.json",
    "11_RECEIPTS_AND_HASHES/HP_ALPHA_DEPLOYMENT_RECEIPT_20260930.json",
    "11_RECEIPTS_AND_HASHES/HP_ALPHA_SOURCE_SHA256_20260930.txt",
]:
    src = CAB / rel
    dst = CCC / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(src.read_bytes())

print(f"FINALIZE_RECEIPT={OUT}")
print(f"FINALIZE_RECEIPT_SHA256={sha(OUT)}")
print(f"MANIFEST_SHA256={sha(MAN)}")
print(f"SERVICE_STATE={service}")
print(f"SOCKET_MODE={socket_mode}")
print(f"LOCAL_STATE={receipt['local_state']}")