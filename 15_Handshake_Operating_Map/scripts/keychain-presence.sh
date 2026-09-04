#!/usr/bin/env bash
set -euo pipefail

STATE_DIR="${FA_STATE_DIR:-$HOME/.config/FreedomArchitect/state}"
mkdir -p "$STATE_DIR"
chmod 700 "$STATE_DIR" 2>/dev/null || true

fail=0
if [ -n "${OPENAI_API_KEY:-}" ]; then printf '%-24s PRESENT\n' OPENAI_API_KEY; else printf '%-24s MISSING\n' OPENAI_API_KEY; fail=1; fi
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then printf '%-24s PRESENT\n' GITHUB_AUTH; else printf '%-24s MISSING/REVIEW\n' GITHUB_AUTH; fail=1; fi
printf '%-24s %s\n' GOOGLE_DRIVE_AUTH CONNECTOR/REVIEW
printf '%-24s %s\n' GMAIL_AUTH CONNECTOR/REVIEW
printf '%-24s %s\n' CALENDAR_AUTH CONNECTOR/REVIEW

if [ "$fail" -eq 0 ]; then
  printf '%s\n' REVIEW > "$STATE_DIR/KEYCHAIN_LOCK.state"
  echo "KEYCHAIN_LOCK -> REVIEW (presence found; scope/auth checks still required before PASS)."
else
  printf '%s\n' HOLD > "$STATE_DIR/KEYCHAIN_LOCK.state"
  echo "KEYCHAIN_LOCK -> HOLD"
fi
chmod 600 "$STATE_DIR/KEYCHAIN_LOCK.state" 2>/dev/null || true
