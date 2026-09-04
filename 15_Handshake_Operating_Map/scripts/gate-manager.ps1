$ErrorActionPreference = 'Stop'
$StateDir = if ($env:FA_STATE_DIR) { $env:FA_STATE_DIR } else { Join-Path $HOME '.config\FreedomArchitect\state' }
New-Item -ItemType Directory -Force -Path $StateDir | Out-Null
$Gates = @('INTERFACE_MATCH','MAP_LOCK','KEYCHAIN_LOCK','DEVICE_VERIFY','REVENUE_READY','HUMAN_RELEASE')
$Allowed = @('PASS','REVIEW','HOLD','UNKNOWN')

function Get-GateState([string]$Gate) {
    $Path = Join-Path $StateDir "$Gate.state"
    $Value = 'HOLD'
    if (Test-Path $Path) { $Value = (Get-Content $Path -Raw).Trim().ToUpperInvariant() }
    if ($Value -notin $Allowed) { return 'REVIEW' }
    return $Value
}

function Show-Gates {
    foreach ($Gate in $Gates) { Write-Host ("{0,-18} {1}" -f $Gate,(Get-GateState $Gate)) }
}

function Set-Gate([string]$Gate,[string]$State) {
    $Gate = $Gate.ToUpperInvariant(); $State = $State.ToUpperInvariant()
    $Index = [Array]::IndexOf($Gates,$Gate)
    if ($Index -lt 0) { throw "Unknown gate: $Gate" }
    if ($State -notin $Allowed) { throw "Invalid state: $State" }
    if ($State -eq 'PASS' -and $Index -gt 0) {
        for ($i=0; $i -lt $Index; $i++) {
            $Prior=$Gates[$i]; $PriorState=Get-GateState $Prior
            if ($PriorState -ne 'PASS') { throw "BLOCKED: $Gate cannot PASS while $Prior is $PriorState." }
        }
    }
    Set-Content -Path (Join-Path $StateDir "$Gate.state") -Value $State -Encoding ascii
    Write-Host "$Gate -> $State"
}

$Command = if ($args.Count -gt 0) { $args[0].ToLowerInvariant() } else { 'status' }
switch ($Command) {
    'status' { Show-Gates }
    'set' { if ($args.Count -lt 3) { throw 'Usage: gate-manager.ps1 set GATE STATE' }; Set-Gate $args[1] $args[2] }
    'reset' { Get-ChildItem $StateDir -Filter '*.state' -ErrorAction SilentlyContinue | Remove-Item -Force; Write-Host 'Gate state reset to default HOLD.' }
    default { throw 'Usage: gate-manager.ps1 [status | set GATE STATE | reset]' }
}
