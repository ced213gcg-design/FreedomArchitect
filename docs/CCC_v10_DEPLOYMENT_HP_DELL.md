# CCC v10 Deployment — HP + Dell

## HP / ChromeOS Crostini
```bash
git pull
git switch upgrade/ccc-living-dashboard-v10
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/validate_ccc_repo.py
python -m compileall -q 19_Live_Adaptive_Dashboard 21_CCC_Orchestra 22_CCC_Ledger 23_CCC_Agent_Mesh scripts
pytest -q --import-mode=importlib
node scripts/test_sphere.js
python 19_Live_Adaptive_Dashboard/backend/app.py
```
Expected local URL: `http://127.0.0.1:8787` unless environment overrides it.

If a dependency is missing, report the exact dependency. Do not silently change package managers.

## Dell / Windows 11 Pro / Hyper-V
Use an **elevated PowerShell 5.1+** shell.

Do not replace the existing upgraded SOC launcher.

```powershell
# Verify launcher location for your actual installation first.
$Launcher = 'C:\CCC\START_CCC_SOC_LAB_UPGRADED.ps1'
& $Launcher -PreflightOnly
# Only after PASS:
& $Launcher
Test-Path 'C:\CCC\State\ccc-soc-live-state.json'
Get-Content 'C:\CCC\State\ccc-soc-live-state.json'
```

The state file must not contain credentials. Preserve launcher transcript/JSONL/hash evidence.

## Approved adapter exposure
The HP dashboard does not assume direct Windows filesystem access. Configure `CCC_SOC_STATE_PATH` only to a locally mounted/copied/approved read-only integration path. Until such an approved path exists, `/api/soc/state` must report `UNKNOWN / DISCONNECTED`.
