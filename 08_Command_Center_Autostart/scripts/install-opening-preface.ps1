$ErrorActionPreference='Stop'

$UserRoot = if ($env:USERPROFILE) { $env:USERPROFILE } else { $HOME }
$Base = if ($env:FA_BASE) { $env:FA_BASE } else { "$UserRoot\FreedomArchitect" }
$StateDir = "$UserRoot\.config\FreedomArchitect\state"
$PrivateDir = "$UserRoot\.config\FreedomArchitect\private"
$DoctrineFile = "$PrivateDir\doctrine.txt"

New-Item -ItemType Directory -Force -Path $StateDir,$PrivateDir | Out-Null
if (-not (Test-Path $DoctrineFile)) { New-Item -ItemType File -Force -Path $DoctrineFile | Out-Null }

$ProfilePath = $PROFILE.CurrentUserCurrentHost
$ProfileDir = Split-Path -Parent $ProfilePath
if ($ProfileDir) { New-Item -ItemType Directory -Force -Path $ProfileDir | Out-Null }
if (-not (Test-Path $ProfilePath)) { New-Item -ItemType File -Force -Path $ProfilePath | Out-Null }

$Begin="# >>> FreedomArchitect Unc's World autostart >>>"
$End="# <<< FreedomArchitect Unc's World autostart <<<"
$Text=if (Test-Path $ProfilePath) { Get-Content $ProfilePath -Raw } else { '' }
$Pattern=[regex]::Escape($Begin)+'.*?'+[regex]::Escape($End)
$Text=[regex]::Replace($Text,$Pattern,'',[System.Text.RegularExpressions.RegexOptions]::Singleline).TrimEnd()

$BlockLines = @(
    $Begin,
    '$env:FA_BASE = "$env:USERPROFILE\FreedomArchitect"',
    'function global:fa {',
    '    $Launcher = "$env:FA_BASE\07_Unified_Launcher\scripts\unified-launcher.ps1"',
    '    if (-not (Test-Path $Launcher)) { Write-Host "FreedomArchitect launcher missing: $Launcher" -ForegroundColor Red; return }',
    '    & $Launcher',
    '}',
    '$Preface = "$env:FA_BASE\08_Command_Center_Autostart\scripts\show-preface.ps1"',
    'if ($env:FA_SKIP_AUTOSTART -ne ''1'' -and (Test-Path $Preface)) { & $Preface }',
    $End
)
$Block = $BlockLines -join "`r`n"
Set-Content -Path $ProfilePath -Value ($Text+"`r`n`r`n"+$Block+"`r`n") -Encoding UTF8

Write-Host "Installed Unc's World opening surface into $ProfilePath"
Write-Host "FreedomArchitect base: $Base"
Write-Host "Private doctrine file: $DoctrineFile"
Write-Host "Local gate state: $StateDir"
Write-Host "Open a new PowerShell window to verify startup."
