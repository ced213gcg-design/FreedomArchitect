#!/usr/bin/env bash
set -euo pipefail

BASE="${FA_BASE:-$HOME/FreedomArchitect}"
BASHRC="$HOME/.bashrc"
STATE_DIR="$HOME/.config/FreedomArchitect/state"
PRIVATE_DIR="$HOME/.config/FreedomArchitect/private"
DOCTRINE_FILE="$PRIVATE_DIR/doctrine.txt"
MARKER_BEGIN="# >>> FreedomArchitect Unc's World autostart >>>"
MARKER_END="# <<< FreedomArchitect Unc's World autostart <<<"

mkdir -p "$STATE_DIR" "$PRIVATE_DIR"
chmod 700 "$HOME/.config/FreedomArchitect" "$STATE_DIR" "$PRIVATE_DIR" 2>/dev/null || true
if [ ! -e "$DOCTRINE_FILE" ]; then : > "$DOCTRINE_FILE"; fi
chmod 600 "$DOCTRINE_FILE" 2>/dev/null || true

for script in \
  "$BASE/08_Command_Center_Autostart/scripts/autostart.sh" \
  "$BASE/08_Command_Center_Autostart/scripts/show-preface.sh" \
  "$BASE/08_Command_Center_Autostart/scripts/set-private-doctrine.sh" \
  "$BASE/07_Unified_Launcher/scripts/unified-launcher.sh" \
  "$BASE/15_Handshake_Operating_Map/scripts/gate-manager.sh" \
  "$BASE/15_Handshake_Operating_Map/scripts/keychain-presence.sh" \
  "$BASE/19_Interface_Reference_Lock/interface-gate-check.sh"; do
  [ -f "$script" ] && chmod +x "$script"
done

touch "$BASHRC"
python3 - "$BASHRC" "$MARKER_BEGIN" "$MARKER_END" <<'PY'
from pathlib import Path
import sys
p=Path(sys.argv[1]); begin=sys.argv[2]; end=sys.argv[3]
text=p.read_text() if p.exists() else ''
if begin in text and end in text:
    before=text.split(begin,1)[0]
    after=text.split(end,1)[1]
    text=before+after.lstrip('\n')
block=f'''{begin}
export FA_BASE="$HOME/FreedomArchitect"
alias fa='"$HOME/FreedomArchitect/07_Unified_Launcher/scripts/unified-launcher.sh"'
if [ -f "$HOME/FreedomArchitect/08_Command_Center_Autostart/scripts/autostart.sh" ]; then
  . "$HOME/FreedomArchitect/08_Command_Center_Autostart/scripts/autostart.sh"
fi
{end}
'''
p.write_text(text.rstrip()+"\n\n"+block)
PY

printf '%s\n' "Installed Unc's World opening surface into $BASHRC"
printf '%s\n' "Private doctrine file: $DOCTRINE_FILE"
printf '%s\n' "Local gate state: $STATE_DIR"
printf '%s\n' "Use set-private-doctrine.sh to place private doctrine locally without committing it to Git."
printf '%s\n' "Run interface-gate-check.sh to import canonical runtime evidence into INTERFACE_MATCH."
printf '%s\n' "Open a new terminal to verify startup."
