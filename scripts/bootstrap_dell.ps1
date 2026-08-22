param([switch]$PreflightOnly)
$ErrorActionPreference = "Stop"
if ($PSVersionTable.PSVersion.Major -lt 5) { throw "PowerShell 5.1+ required" }
$principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) { throw "Administrator shell required" }
$Launcher = "C:\CCC\START_CCC_SOC_LAB_UPGRADED.ps1"
if (-not (Test-Path $Launcher)) { throw "Existing upgraded SOC launcher not found at $Launcher" }
& $Launcher -PreflightOnly
if (-not $PreflightOnly) { & $Launcher }
