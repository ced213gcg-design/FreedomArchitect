# CCC v10.1 HP / Dell Deployment and Acceptance

## HP: `ccc-hp-dev-01`

From Crostini Linux:

```bash
cd ~/FreedomArchitect
git fetch origin
git switch upgrade/ccc-living-dashboard-v10-1
git pull --ff-only origin upgrade/ccc-living-dashboard-v10-1
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/validate_ccc_repo.py
pytest -q --import-mode=importlib
node scripts/test_sphere.js
node scripts/test_exception_constellation.js
python 19_Live_Adaptive_Dashboard/backend/app.py
```

Expected local URL: `http://127.0.0.1:8787`.

Verify the dashboard renders and these endpoints return HTTP 200: `/api/health`, `/api/manifest`, `/api/hosts`, `/api/organs`, `/api/mission`, `/api/pressure-loss`, `/api/soc/state`, `/api/ledger/recent`, `/api/agents`, `/api/exceptions`, `/api/exceptions/high-priority`, `/api/sphere`, `/api/economics/technology-choice`, `/api/economics/revenue-flywheel`.

If Python, Node, venv support or another dependency is missing, stop and report the missing dependency precisely. Do not turn dependency absence into PASS.

## Dell: `ccc-dell-compute-01`

Use elevated Windows PowerShell 5.1. Do not replace the existing upgraded SOC launcher.

```powershell
$Launcher = 'C:\CCC\START_CCC_SOC_LAB_UPGRADED.ps1'
$PSVersionTable.PSVersion
([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
& $Launcher -PreflightOnly
```

Proceed to the existing authorized full launcher only if preflight PASS is evidenced. Then verify:

```powershell
Test-Path 'C:\CCC\State\ccc-soc-live-state.json'
Get-Content 'C:\CCC\State\ccc-soc-live-state.json'
```

The state file must not contain credentials. Preserve transcript/JSONL/hash evidence. The approved SOC range is `10.69.69.0/24`; `10.77.0.0/24` is superseded historical context.

If Dell state is unavailable, dashboard state remains `SOC = UNKNOWN / DISCONNECTED`. Never fabricate green.
