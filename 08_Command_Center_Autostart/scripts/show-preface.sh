#!/usr/bin/env bash
set -u

BASE="${FA_BASE:-$HOME/FreedomArchitect}"
STATE_DIR="${FA_STATE_DIR:-$HOME/.config/FreedomArchitect/state}"
PRIVATE_DIR="${FA_PRIVATE_DIR:-$HOME/.config/FreedomArchitect/private}"
DOCTRINE_FILE="$PRIVATE_DIR/doctrine.txt"

read_gate() {
  local gate="$1" fallback="${2:-HOLD}" file="$STATE_DIR/${gate}.state" value="$fallback"
  if [ -f "$file" ]; then value="$(tr -d '[:space:]' < "$file" | tr '[:lower:]' '[:upper:]')"; fi
  case "$value" in PASS|REVIEW|HOLD|UNKNOWN) printf '%s' "$value" ;; *) printf 'REVIEW' ;; esac
}

BRANCH="UNKNOWN"; DIRTY="UNKNOWN"
if command -v git >/dev/null 2>&1 && git -C "$BASE" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  BRANCH="$(git -C "$BASE" branch --show-current 2>/dev/null || printf 'UNKNOWN')"
  if [ -n "$(git -C "$BASE" status --porcelain 2>/dev/null)" ]; then DIRTY="CHANGES"; else DIRTY="CLEAN"; fi
fi

clear 2>/dev/null || true
printf '%s\n' '=================================================================='
printf '%s\n' "                    UNC'S WORLD — OPENING PREFACE"
printf '%s\n' '=================================================================='
if [ -r "$DOCTRINE_FILE" ] && [ -s "$DOCTRINE_FILE" ]; then
  cat "$DOCTRINE_FILE"
else
  printf '%s\n' '[PRIVATE DOCTRINE: LOCAL SOURCE NOT INSTALLED]'
fi
printf '%s\n' '------------------------------------------------------------------'
printf '%s\n' "Repository : $BRANCH / $DIRTY"
for gate in INTERFACE_MATCH MAP_LOCK KEYCHAIN_LOCK DEVICE_VERIFY REVENUE_READY HUMAN_RELEASE; do
  printf '%-18s %s\n' "$gate" "$(read_gate "$gate" HOLD)"
done
printf '%s\n' '------------------------------------------------------------------'
printf '%s\n' 'Critical path:'
printf '%s\n' 'INTERFACE -> MAP -> KEYCHAIN -> DEVICE -> REVENUE -> HUMAN RELEASE'
printf '%s\n' 'LINK-01 HP_RECEIVER_VERIFICATION remains unresolved until proven.'
printf '%s\n' '------------------------------------------------------------------'
printf '%s\n' 'Launcher: Boundary | Map | Keychain | Work Box | Today'
printf '%s\n' 'Private doctrine and credential values are never read from Git.'
printf '%s\n' '=================================================================='
printf '\n'
