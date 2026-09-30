#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "HOLD: run as root"
  exit 20
fi

OVERLAY_FILE="${1:-/opt/ccc/dell-clean-rebuild/config/TOPOLOGY_OVERLAY.env}"
[[ -f "$OVERLAY_FILE" ]] || { echo "HOLD: topology overlay not present"; exit 21; }

# shellcheck disable=SC1090
source "$OVERLAY_FILE"

[[ "${TOPOLOGY_VERIFIED:-NO}" == "YES" ]] || { echo "HOLD: TOPOLOGY_VERIFIED != YES"; exit 22; }
[[ -n "${TOPOLOGY_SOURCE_COMMIT:-}" ]] || { echo "HOLD: topology source commit missing"; exit 23; }
[[ -n "${TOPOLOGY_SOURCE_PATH:-}" ]] || { echo "HOLD: topology source path missing"; exit 24; }
[[ -n "${MGMT_BRIDGE_NAME:-}" ]] || { echo "HOLD: management bridge name missing"; exit 25; }
[[ -n "${RANGE_BRIDGE_NAME:-}" ]] || { echo "HOLD: range bridge name missing"; exit 26; }

NETWORK_DIR="/etc/network/interfaces.d"
NETWORK_FILE="$NETWORK_DIR/ccc-lab-bridges"
BACKUP_DIR="/var/lib/ccc-run-dell/network-backups"
mkdir -p "$NETWORK_DIR" "$BACKUP_DIR"

TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
cp -a /etc/network/interfaces "$BACKUP_DIR/interfaces-$TIMESTAMP" 2>/dev/null || true
cp -a "$NETWORK_FILE" "$BACKUP_DIR/ccc-lab-bridges-$TIMESTAMP" 2>/dev/null || true

{
  echo "# CCC verified topology overlay"
  echo "# source_commit=$TOPOLOGY_SOURCE_COMMIT"
  echo "# source_path=$TOPOLOGY_SOURCE_PATH"
  echo
  echo "auto $MGMT_BRIDGE_NAME"
  if [[ -n "${MGMT_BRIDGE_ADDRESS:-}" ]]; then
    echo "iface $MGMT_BRIDGE_NAME inet static"
    echo "    address $MGMT_BRIDGE_ADDRESS"
  else
    echo "iface $MGMT_BRIDGE_NAME inet manual"
  fi
  echo "    bridge-ports none"
  echo "    bridge-stp off"
  echo "    bridge-fd 0"
  echo
  echo "auto $RANGE_BRIDGE_NAME"
  if [[ -n "${RANGE_BRIDGE_ADDRESS:-}" ]]; then
    echo "iface $RANGE_BRIDGE_NAME inet static"
    echo "    address $RANGE_BRIDGE_ADDRESS"
  else
    echo "iface $RANGE_BRIDGE_NAME inet manual"
  fi
  echo "    bridge-ports none"
  echo "    bridge-stp off"
  echo "    bridge-fd 0"
} >"$NETWORK_FILE"

if command -v ifreload >/dev/null 2>&1; then
  ifreload -a
else
  echo "HOLD: topology file written but ifreload unavailable"
  exit 27
fi

echo "TOPOLOGY_APPLY=PASS"
echo "SOURCE_COMMIT=$TOPOLOGY_SOURCE_COMMIT"
echo "SOURCE_PATH=$TOPOLOGY_SOURCE_PATH"
