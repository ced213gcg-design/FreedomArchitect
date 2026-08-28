$ErrorActionPreference='Stop'
$StateDir = if ($env:FA_STATE_DIR) { $env:FA_STATE_DIR } else { Join-Path $HOME '.config\FreedomArchitect\state' }
New-Item -ItemType Directory -Force -Path $StateDir | Out-Null
$Fail=$false

if ($env:OPENAI_API_KEY) { Write-Host ('{0,-24} PRESENT' -f 'OPENAI_API_KEY') } else { Write-Host ('{0,-24} MISSING' -f 'OPENAI_API_KEY'); $Fail=$true }
if (Get-Command gh -ErrorAction SilentlyContinue) {
    & gh auth status *> $null
    if ($LASTEXITCODE -eq 0) { Write-Host ('{0,-24} PRESENT' -f 'GITHUB_AUTH') } else { Write-Host ('{0,-24} MISSING/REVIEW' -f 'GITHUB_AUTH'); $Fail=$true }
} else { Write-Host ('{0,-24} MISSING/REVIEW' -f 'GITHUB_AUTH'); $Fail=$true }
Write-Host ('{0,-24} CONNECTOR/REVIEW' -f 'GOOGLE_DRIVE_AUTH')
Write-Host ('{0,-24} CONNECTOR/REVIEW' -f 'GMAIL_AUTH')
Write-Host ('{0,-24} CONNECTOR/REVIEW' -f 'CALENDAR_AUTH')

$State = if ($Fail) { 'HOLD' } else { 'REVIEW' }
Set-Content -Path (Join-Path $StateDir 'KEYCHAIN_LOCK.state') -Value $State -Encoding ascii
Write-Host "KEYCHAIN_LOCK -> $State"
if (-not $Fail) { Write-Host 'Presence found; scope and harmless authentication checks are still required before PASS.' }
