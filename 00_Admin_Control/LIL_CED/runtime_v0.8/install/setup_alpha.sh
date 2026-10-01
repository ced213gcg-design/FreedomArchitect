#!/usr/bin/env bash
set -Eeuo pipefail

HOME_DIR="/home/ced213gcg"
APP="$HOME_DIR/LilCed/app"
CAB="$HOME_DIR/LIL_CED_CABINET"
CCC="$HOME_DIR/CCC_FILING_CABINET/14_LIL_CED"
VENV="$APP/.venv"
BOOT="$APP/virtualenv.pyz"

echo "=== LIL CED v0.8 ALPHA SETUP ==="
date -Is

python3 -m py_compile "$APP/lilced_core.py" "$APP/lilced_terminal.py" "$APP/lilced_graph.py" "$APP/lilced_model.py"
echo "PY_COMPILE=PASS"

desktop-file-validate "$HOME_DIR/.local/share/applications/lilced-terminal.desktop"
desktop-file-validate "$HOME_DIR/.local/share/applications/lilced-cabinet.desktop"
desktop-file-validate "$HOME_DIR/.local/share/applications/ccc-filing-cabinet.desktop"
echo "DESKTOP_VALIDATE=PASS"

if [ ! -x "$VENV/bin/python" ] || [ ! -x "$VENV/bin/pip" ]; then
  rm -rf "$VENV"
  if [ ! -f "$BOOT" ]; then
    curl -fsSL "https://bootstrap.pypa.io/virtualenv.pyz" -o "$BOOT.part"
    mv "$BOOT.part" "$BOOT"
  fi
  echo "VIRTUALENV_BOOTSTRAP_SHA256=$(sha256sum "$BOOT" | awk '{print $1}')"
  python3 "$BOOT" "$VENV"
fi

"$VENV/bin/python" -m pip install --disable-pip-version-check -q --upgrade pip
"$VENV/bin/python" -m pip install --disable-pip-version-check -q langgraph anthropic
echo "PY_DEPS_INSTALL=PASS"

"$VENV/bin/python" - <<'PY'
import anthropic, langgraph
print("ANTHROPIC_IMPORT=PASS")
print("LANGGRAPH_IMPORT=PASS")
PY

"$VENV/bin/python" -m pip freeze > "$CAB/04_SOURCE_AND_DEPENDENCIES/requirements.lock.txt"
cp "$CAB/04_SOURCE_AND_DEPENDENCIES/requirements.lock.txt" "$CCC/04_SOURCE_AND_DEPENDENCIES/requirements.lock.txt"

chmod 700 "$APP/lilced_core.py" "$APP/lilced_terminal.py"
chmod 600 "$HOME_DIR/.config/lilced/secrets.env"
chmod 644 "$HOME_DIR/.config/systemd/user/lilced-core.service"
chmod 644 "$HOME_DIR/.local/share/applications/"{lilced-terminal.desktop,lilced-cabinet.desktop,ccc-filing-cabinet.desktop}

systemctl --user daemon-reload
systemctl --user enable --now lilced-core.service

for _ in $(seq 1 40); do
  [ -S "$HOME_DIR/.local/state/lilced/lilced.sock" ] && break
  sleep 0.1
done
[ -S "$HOME_DIR/.local/state/lilced/lilced.sock" ]

echo "SERVICE_START=PASS"
systemctl --user --no-pager --full status lilced-core.service | sed -n '1,20p'
echo "SETUP=PASS"