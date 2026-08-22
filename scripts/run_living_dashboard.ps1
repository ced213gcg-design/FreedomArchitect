$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
python 19_Live_Adaptive_Dashboard/backend/app.py
