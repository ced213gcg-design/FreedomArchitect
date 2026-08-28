$Base = if ($env:FA_BASE) { $env:FA_BASE } else { Join-Path $HOME 'FreedomArchitect' }
function Open-Text([string]$RelativePath) { $Path=Join-Path $Base $RelativePath; if (Test-Path $Path) { Start-Process notepad.exe -ArgumentList @($Path) } else { Write-Host "Missing: $RelativePath" } }
while ($true) {
    Clear-Host
    Write-Host "=============================================================="
    Write-Host "                 UNC'S WORLD - UNIFIED LAUNCHER"
    Write-Host "=============================================================="
    Write-Host "1. Opening Preface"
    Write-Host "2. Operating Boundary"
    Write-Host "3. Restart Authority"
    Write-Host "4. Command / Mapping Map"
    Write-Host "5. Keychain Gate Authority"
    Write-Host "6. Revenue Work Box"
    Write-Host "7. Today's Command"
    Write-Host "8. Mission State folder"
    Write-Host "9. Repository folder"
    Write-Host "Q. Exit"
    $Choice=(Read-Host 'Select').Trim().ToUpperInvariant()
    switch ($Choice) {
        '1' { Open-Text '06_Daily_Command_Dashboard\OPENING_PREFACE.md' }
        '2' { Open-Text '00_Admin_Control\UNC_WORLD_OPERATING_BOUNDARY_2026-08-28.md' }
        '3' { Open-Text '00_Admin_Control\RESTART_AUTHORITY_2026-08-28.md' }
        '4' { Open-Text '15_Handshake_Operating_Map\maps\unc-world-command-map.md' }
        '5' { Open-Text '15_Handshake_Operating_Map\rules\keychain-gate-authority.md' }
        '6' { Open-Text '17_Revenue_Work_Box\WORK_BOX.md' }
        '7' { Open-Text '06_Daily_Command_Dashboard\today-command.md' }
        '8' { Start-Process explorer.exe (Join-Path $Base '09_Mission_State_Dashboard') }
        '9' { Start-Process explorer.exe $Base }
        'Q' { break }
        default { Write-Host 'Invalid selection.'; Start-Sleep -Seconds 1 }
    }
}
