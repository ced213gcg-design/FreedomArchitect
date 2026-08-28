param([string]$SourcePath)
$ErrorActionPreference='Stop'
$PrivateDir = if ($env:FA_PRIVATE_DIR) { $env:FA_PRIVATE_DIR } else { Join-Path $HOME '.config\FreedomArchitect\private' }
$DoctrineFile = Join-Path $PrivateDir 'doctrine.txt'
New-Item -ItemType Directory -Force -Path $PrivateDir | Out-Null

if ($SourcePath) {
    if (-not (Test-Path $SourcePath)) { throw "Source file not found: $SourcePath" }
    Copy-Item -Force $SourcePath $DoctrineFile
} else {
    if (-not (Test-Path $DoctrineFile)) { New-Item -ItemType File -Force -Path $DoctrineFile | Out-Null }
    Start-Process notepad.exe -ArgumentList @($DoctrineFile) -Wait
}

if (-not (Test-Path $DoctrineFile) -or (Get-Item $DoctrineFile).Length -eq 0) { throw "Doctrine file is empty: $DoctrineFile" }
Write-Host "Private doctrine installed locally: $DoctrineFile"
Write-Host 'No doctrine text was written to Git.'
