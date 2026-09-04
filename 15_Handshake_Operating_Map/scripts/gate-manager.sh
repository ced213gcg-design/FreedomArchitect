#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="${FA_STATE_DIR:-$HOME/.config/FreedomArchitect/state}"
mkdir -p "$STATE_DIR"
chmod 700 "$STATE_DIR" 2>/dev/null || true
GATES=(INTERFACE_MATCH MAP_LOCK KEYCHAIN_LOCK DEVICE_VERIFY REVENUE_READY HUMAN_RELEASE)

index_of() { local target="$1" i; for i in "${!GATES[@]}"; do [ "${GATES[$i]}" = "$target" ] && { echo "$i"; return 0; }; done; return 1; }
get_state() { local gate="$1" file="$STATE_DIR/$gate.state" value="HOLD"; [ -f "$file" ] && value="$(tr -d '[:space:]' < "$file" | tr '[:lower:]' '[:upper:]')"; case "$value" in PASS|REVIEW|HOLD|UNKNOWN) echo "$value" ;; *) echo REVIEW ;; esac; }
show_status() { local gate; for gate in "${GATES[@]}"; do printf '%-18s %s\n' "$gate" "$(get_state "$gate")"; done; }

set_state() {
  local gate="${1:-}" state="${2:-}" idx prior i
  gate="$(printf '%s' "$gate" | tr '[:lower:]' '[:upper:]')"
  state="$(printf '%s' "$state" | tr '[:lower:]' '[:upper:]')"
  idx="$(index_of "$gate")" || { echo "Unknown gate: $gate" >&2; exit 2; }
  case "$state" in PASS|REVIEW|HOLD|UNKNOWN) ;; *) echo "Invalid state: $state" >&2; exit 2 ;; esac
  if [ "$state" = "PASS" ] && [ "$idx" -gt 0 ]; then
    for ((i=0; i<idx; i++)); do
      prior="${GATES[$i]}"
      if [ "$(get_state "$prior")" != "PASS" ]; then
        echo "BLOCKED: $gate cannot PASS while $prior is $(get_state "$prior")." >&2
        exit 3
      fi
    done
  fi
  printf '%s\n' "$state" > "$STATE_DIR/$gate.state"
  chmod 600 "$STATE_DIR/$gate.state" 2>/dev/null || true
  printf '%s -> %s\n' "$gate" "$state"
}

case "${1:-status}" in
  status) show_status ;;
  set) set_state "${2:-}" "${3:-}" ;;
  reset) rm -f "$STATE_DIR"/*.state; echo "Gate state reset to default HOLD." ;;
  *) echo "Usage: $0 [status | set GATE STATE | reset]"; exit 2 ;;
esac
