$ErrorActionPreference = 'Stop'

$Branch = 'unc-world-control-surface-2026-08-28'
$Remote = 'https://github.com/ced213gcg-design/FreedomArchitect.git'
$Repo = "$env:USERPROFILE\FreedomArchitect"
$Stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$Stage = "$env:TEMP\FreedomArchitect-stage-$Stamp"
$Backup = "$env:USERPROFILE\FreedomArchitect-preserved-$Stamp"

Write-Host ''
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host " UNC'S WORLD - DELL CLEAN BOOTSTRAP" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan

# Find Git without depending on PATH refresh.
$GitExe = $null
$Candidates = @(
    "$env:ProgramFiles\Git\cmd\git.exe",
    "$env:ProgramFiles\Git\bin\git.exe"
)
foreach ($Candidate in $Candidates) {
    if (Test-Path $Candidate) { $GitExe = $Candidate; break }
}
if (-not $GitExe) {
    $GitCmd = Get-Command git -ErrorAction SilentlyContinue
    if ($GitCmd) { $GitExe = $GitCmd.Source }
}
if (-not $GitExe) {
    throw 'STOP: Git is not installed or could not be located.'
}

Write-Host "Git:" (& $GitExe --version) -ForegroundColor Green

# Clone a known-clean copy first. Do not touch the existing folder until verification passes.
if (Test-Path $Stage) { Remove-Item -Recurse -Force $Stage }
Write-Host "Cloning verified branch into staging..." -ForegroundColor Cyan
& $GitExe clone --branch $Branch --single-branch $Remote $Stage
if ($LASTEXITCODE -ne 0) { throw 'STOP: Git clone failed.' }

$Required = @(
    '07_Unified_Launcher\scripts\unified-launcher.ps1',
    '08_Command_Center_Autostart\scripts\install-opening-preface.ps1',
    '08_Command_Center_Autostart\scripts\show-preface.ps1',
    '15_Handshake_Operating_Map\scripts\gate-manager.ps1',
    '15_Handshake_Operating_Map\scripts\keychain-presence.ps1',
    '17_Revenue_Work_Box\WORK_BOX.md'
)

foreach ($Rel in $Required) {
    $Full = "$Stage\$Rel"
    if (-not (Test-Path $Full)) { throw "STOP: Verified branch is missing required file: $Rel" }
}

Write-Host 'Staging verification: PASS' -ForegroundColor Green

# Preserve whatever is currently at the canonical path.
if (Test-Path $Repo) {
    Write-Host "Preserving existing folder as: $Backup" -ForegroundColor Yellow
    Move-Item -Path $Repo -Destination $Backup
}

Move-Item -Path $Stage -Destination $Repo

# Verify the canonical installation physically exists.
foreach ($Rel in $Required) {
    $Full = "$Repo\$Rel"
    if (-not (Test-Path $Full)) { throw "STOP: Canonical install missing required file: $Rel" }
}

# Build a minimal profile with literal Windows paths. No Join-Path dependency.
$ProfilePath = $PROFILE.CurrentUserCurrentHost
$ProfileDir = Split-Path -Parent $ProfilePath
New-Item -ItemType Directory -Force -Path $ProfileDir | Out-Null

$ProfileLines = @(
    '$env:FA_BASE = "$env:USERPROFILE\FreedomArchitect"',
    '',
    'function global:fa {',
    '    $Launcher = "$env:USERPROFILE\FreedomArchitect\07_Unified_Launcher\scripts\unified-launcher.ps1"',
    '    if (-not (Test-Path $Launcher)) { throw "FreedomArchitect launcher missing: $Launcher" }',
    '    & $Launcher',
    '}',
    '',
    '$Preface = "$env:USERPROFILE\FreedomArchitect\08_Command_Center_Autostart\scripts\show-preface.ps1"',
    'if ($env:FA_SKIP_AUTOSTART -ne ''1'' -and (Test-Path $Preface)) { & $Preface }'
)
Set-Content -Path $ProfilePath -Value $ProfileLines -Encoding UTF8

# Persist a safe user-level policy. Process Bypass used by the caller remains temporary.
try { Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force -ErrorAction Stop } catch { Write-Host "CurrentUser policy note: $($_.Exception.Message)" -ForegroundColor Yellow }

# Load profile in this process and verify the function.
. $ProfilePath

$Launcher = "$Repo\07_Unified_Launcher\scripts\unified-launcher.ps1"
$Gate = "$Repo\15_Handshake_Operating_Map\scripts\gate-manager.ps1"
$Keychain = "$Repo\15_Handshake_Operating_Map\scripts\keychain-presence.ps1"
$Preface = "$Repo\08_Command_Center_Autostart\scripts\show-preface.ps1"

Write-Host ''
Write-Host '================ VERIFIED DELL STATE ================' -ForegroundColor Cyan
Write-Host 'Repository :' (Test-Path "$Repo\.git")
Write-Host 'Launcher   :' (Test-Path $Launcher)
Write-Host 'Preface    :' (Test-Path $Preface)
Write-Host 'Gate       :' (Test-Path $Gate)
Write-Host 'Keychain   :' (Test-Path $Keychain)
Write-Host 'Branch     :' (& $GitExe -C $Repo branch --show-current)
Write-Host 'Profile    :' (Test-Path $ProfilePath)
Get-Command fa -ErrorAction Stop | Format-Table CommandType,Name -AutoSize
Write-Host '======================================================' -ForegroundColor Cyan
Write-Host 'DELL CLEAN BOOTSTRAP: VERIFIED' -ForegroundColor Green
Write-Host ''
Write-Host 'Run: fa' -ForegroundColor Yellow
