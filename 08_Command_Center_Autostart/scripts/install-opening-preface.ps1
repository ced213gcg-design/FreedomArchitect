$ErrorActionPreference='Stop'
$Base=if ($env:FA_BASE) {$env:FA_BASE} else {Join-Path $HOME 'FreedomArchitect'}
$StateDir=Join-Path $HOME '.config\FreedomArchitect\state'
$PrivateDir=Join-Path $HOME '.config\FreedomArchitect\private'
$DoctrineFile=Join-Path $PrivateDir 'doctrine.txt'
New-Item -ItemType Directory -Force -Path $StateDir,$PrivateDir | Out-Null
if (-not (Test-Path $DoctrineFile)) { New-Item -ItemType File -Force -Path $DoctrineFile | Out-Null }

$ProfilePath=$PROFILE.CurrentUserCurrentHost
$ProfileDir=Split-Path -Parent $ProfilePath
if ($ProfileDir) { New-Item -ItemType Directory -Force -Path $ProfileDir | Out-Null }
if (-not (Test-Path $ProfilePath)) { New-Item -ItemType File -Force -Path $ProfilePath | Out-Null }

$Begin="# >>> FreedomArchitect Unc's World autostart >>>"
$End="# <<< FreedomArchitect Unc's World autostart <<<"
$Text=Get-Content $ProfilePath -Raw
$Pattern=[regex]::Escape($Begin)+'.*?'+[regex]::Escape($End)
$Text=[regex]::Replace($Text,$Pattern,'',[System.Text.RegularExpressions.RegexOptions]::Singleline).TrimEnd()
$Block=@"
$Begin
`$env:FA_BASE = Join-Path `$HOME 'FreedomArchitect'
function global:fa { & (Join-Path `$env:FA_BASE '07_Unified_Launcher\scripts\unified-launcher.ps1') }
if (`$env:FA_SKIP_AUTOSTART -ne '1') {
    `$Preface = Join-Path `$env:FA_BASE '08_Command_Center_Autostart\scripts\show-preface.ps1'
    if (Test-Path `$Preface) { & `$Preface }
}
$End
"@
Set-Content -Path $ProfilePath -Value ($Text+"`r`n`r`n"+$Block+"`r`n") -Encoding UTF8
Write-Host "Installed Unc's World opening surface into $ProfilePath"
Write-Host "Private doctrine file: $DoctrineFile"
Write-Host "Local gate state: $StateDir"
Write-Host "Open a new PowerShell window to verify startup."
