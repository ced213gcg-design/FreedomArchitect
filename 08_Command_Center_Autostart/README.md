# Command Center Autostart — Unc's World Opening Surface

## Purpose
Make the command surface appear when the working terminal/shell opens so operating boundary, gate state, mapping, keychain process, private-doctrine access, and revenue work are immediately accessible.

## Linux / Chromebook Crostini
From the repository root:

```bash
chmod +x 08_Command_Center_Autostart/scripts/*.sh 07_Unified_Launcher/scripts/*.sh 15_Handshake_Operating_Map/scripts/*.sh
./08_Command_Center_Autostart/scripts/install-opening-preface.sh
```

The installer creates these local protected locations:
- `~/.config/FreedomArchitect/private/doctrine.txt`
- `~/.config/FreedomArchitect/state/`

The doctrine file is intentionally blank until Human Command places the private doctrine there. It is not sourced from Git.

Open a new terminal. The opening preface appears first, followed by the unified launcher. Use `fa` to reopen the launcher manually.

To bypass autostart for one session: `FA_SKIP_AUTOSTART=1 bash`

## Windows PowerShell
From the repository root:

```powershell
& .\08_Command_Center_Autostart\scripts\install-opening-preface.ps1
```

The installer creates local private/state folders under `$HOME\.config\FreedomArchitect\` and wires the PowerShell profile. Use `fa` to open the Windows unified launcher.

To bypass autostart for one session: `$env:FA_SKIP_AUTOSTART='1'`

## Security Rule
Public Git may store structure, credential names, and state-machine logic. It must never store private doctrine text or credential values.
