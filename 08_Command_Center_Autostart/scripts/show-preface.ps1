$Base = if ($env:FA_BASE) { $env:FA_BASE } else { Join-Path $HOME 'FreedomArchitect' }
$StateDir = if ($env:FA_STATE_DIR) { $env:FA_STATE_DIR } else { Join-Path $HOME '.config\FreedomArchitect\state' }
$PrivateDir = if ($env:FA_PRIVATE_DIR) { $env:FA_PRIVATE_DIR } else { Join-Path $HOME '.config\FreedomArchitect\private' }
$DoctrineFile = Join-Path $PrivateDir 'doctrine.txt'

function Get-GateState([string]$Gate, [string]$Fallback = 'HOLD') {
    $Path = Join-Path $StateDir "$Gate.state"
    $Value = $Fallback
    if (Test-Path $Path) { $Value = (Get-Content $Path -Raw).Trim().ToUpperInvariant() }
    if ($Value -notin @('PASS','REVIEW','HOLD','UNKNOWN')) { return 'REVIEW' }
    return $Value
}

$Branch='UNKNOWN'; $Dirty='UNKNOWN'
if (Get-Command git -ErrorAction SilentlyContinue) {
    try { $Branch=(git -C $Base branch --show-current 2>$null).Trim(); $Dirty=if (git -C $Base status --porcelain 2>$null) {'CHANGES'} else {'CLEAN'} } catch {}
}

Clear-Host
Write-Host '=================================================================='
Write-Host "                    UNC'S WORLD - OPENING PREFACE"
Write-Host '=================================================================='
if ((Test-Path $DoctrineFile) -and (Get-Item $DoctrineFile).Length -gt 0) { Get-Content $DoctrineFile } else { Write-Host '[PRIVATE DOCTRINE: LOCAL SOURCE NOT INSTALLED]' }
Write-Host '------------------------------------------------------------------'
Write-Host ("Repository : {0} / {1}" -f $Branch,$Dirty)
foreach ($Gate in @('INTERFACE_MATCH','MAP_LOCK','KEYCHAIN_LOCK','DEVICE_VERIFY','REVENUE_READY','HUMAN_RELEASE')) { Write-Host ("{0,-18} {1}" -f $Gate,(Get-GateState $Gate)) }
Write-Host '------------------------------------------------------------------'
Write-Host 'INTERFACE -> MAP -> KEYCHAIN -> DEVICE -> REVENUE -> HUMAN RELEASE'
Write-Host 'LINK-01 HP_RECEIVER_VERIFICATION remains unresolved until proven.'
Write-Host 'Private doctrine and credential values are never read from Git.'
Write-Host '=================================================================='
