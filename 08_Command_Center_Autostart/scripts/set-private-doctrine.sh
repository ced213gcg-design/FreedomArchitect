#!/usr/bin/env bash
set -euo pipefail

PRIVATE_DIR="${FA_PRIVATE_DIR:-$HOME/.config/FreedomArchitect/private}"
DOCTRINE_FILE="$PRIVATE_DIR/doctrine.txt"
mkdir -p "$PRIVATE_DIR"
chmod 700 "$PRIVATE_DIR" 2>/dev/null || true

if [ "$#" -ge 1 ]; then
  SOURCE="$1"
  [ -f "$SOURCE" ] || { echo "Source file not found: $SOURCE" >&2; exit 2; }
  cp "$SOURCE" "$DOCTRINE_FILE"
elif [ ! -t 0 ]; then
  cat > "$DOCTRINE_FILE"
else
  "${EDITOR:-nano}" "$DOCTRINE_FILE"
fi

chmod 600 "$DOCTRINE_FILE" 2>/dev/null || true
if [ ! -s "$DOCTRINE_FILE" ]; then
  echo "Doctrine file is empty: $DOCTRINE_FILE" >&2
  exit 3
fi
printf '%s\n' "Private doctrine installed locally: $DOCTRINE_FILE"
printf '%s\n' "No doctrine text was written to Git."
