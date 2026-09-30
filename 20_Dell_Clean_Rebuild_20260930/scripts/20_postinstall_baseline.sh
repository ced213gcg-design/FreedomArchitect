#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "HOLD: run as root"
  exit 20
fi

command -v pveversion >/dev/null 2>&1 || { echo "HOLD: not running installed Proxmox VE"; exit 21; }

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
INSTALL_ROOT="/opt/ccc/dell-clean-rebuild"
STATE_ROOT="/var/lib/ccc-run-dell"
RECEIPT_ROOT="$STATE_ROOT/receipts"

mkdir -p "$INSTALL_ROOT" "$STATE_ROOT/state" "$RECEIPT_ROOT"
if [[ "$(readlink -f "$PACKAGE_ROOT")" != "$(readlink -f "$INSTALL_ROOT")" ]]; then
  cp -a "$PACKAGE_ROOT/." "$INSTALL_ROOT/"
fi
chmod 0755 "$INSTALL_ROOT/scripts/"*.sh

systemctl mask ccc-dell-bootstrap.service >/dev/null 2>&1 || true
systemctl mask ccc-network-restore.service >/dev/null 2>&1 || true

install -m 0644 "$INSTALL_ROOT/systemd/ccc-post-reboot-acceptance.service"   /etc/systemd/system/ccc-post-reboot-acceptance.service

cat >/usr/local/sbin/RUN <<'EOF'
#!/usr/bin/env bash
set -Eeuo pipefail
if [[ "$#" -ne 1 || "$1" != "DELL" ]]; then
  echo "Usage: RUN DELL"
  exit 64
fi
exec /opt/ccc/dell-clean-rebuild/scripts/30_run_dispatcher.sh
EOF
chmod 0755 /usr/local/sbin/RUN

systemctl daemon-reload
systemctl disable ccc-post-reboot-acceptance.service >/dev/null 2>&1 || true

TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
{
  echo "POSTINSTALL_BASELINE=PASS"
  echo "TIMESTAMP=$TIMESTAMP"
  echo "PVEVERSION=$(pveversion)"
  echo "STALE_BOOTSTRAP_MASKED=$(systemctl is-enabled ccc-dell-bootstrap.service 2>/dev/null || true)"
  echo "STALE_NETWORK_RESTORE_MASKED=$(systemctl is-enabled ccc-network-restore.service 2>/dev/null || true)"
  echo "RUN_COMMAND=/usr/local/sbin/RUN"
  echo "POST_REBOOT_SERVICE_DEFAULT=DISABLED"
} | tee "$RECEIPT_ROOT/postinstall-baseline-$TIMESTAMP.txt"

echo "NEXT_TRUE_MOVE=configure Wi-Fi if needed, then type: RUN DELL"
