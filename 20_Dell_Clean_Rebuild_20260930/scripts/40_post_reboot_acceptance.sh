#!/usr/bin/env bash
set -Eeuo pipefail

STATE_ROOT="/var/lib/ccc-run-dell"
STATE_DIR="$STATE_ROOT/state"
RECEIPT_DIR="$STATE_ROOT/receipts"
mkdir -p "$STATE_DIR" "$RECEIPT_DIR"

[[ -f "$STATE_DIR/PENDING_POST_REBOOT" ]] || {
  echo "POST_REBOOT_ACCEPTANCE=SKIP_NO_PENDING_STATE"
  exit 0
}
[[ ! -f "$STATE_DIR/POST_REBOOT_ACCEPTED" ]] || {
  rm -f "$STATE_DIR/PENDING_POST_REBOOT"
  systemctl disable ccc-post-reboot-acceptance.service >/dev/null 2>&1 || true
  echo "POST_REBOOT_ACCEPTANCE=ALREADY_PASS"
  exit 0
}

TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
RECEIPT="$RECEIPT_DIR/post-reboot-$TIMESTAMP.txt"
exec > >(tee -a "$RECEIPT") 2>&1

echo "=== CCC POST-REBOOT ACCEPTANCE ==="
echo "TIMESTAMP=$TIMESTAMP"
echo "BOOT_ID=$(cat /proc/sys/kernel/random/boot_id)"

systemctl is-enabled ccc-dell-bootstrap.service 2>/dev/null | grep -qx masked || {
  echo "POST_REBOOT_ACCEPTANCE=FAIL_STALE_BOOTSTRAP"
  exit 50
}
systemctl is-enabled ccc-network-restore.service 2>/dev/null | grep -qx masked || {
  echo "POST_REBOOT_ACCEPTANCE=FAIL_STALE_NETWORK_RESTORE"
  exit 51
}

ip -4 addr | grep -q 'inet ' || { echo "POST_REBOOT_ACCEPTANCE=FAIL_NO_IPV4"; exit 52; }
ip route | grep -q '^default ' || { echo "POST_REBOOT_ACCEPTANCE=FAIL_NO_DEFAULT_ROUTE"; exit 53; }
getent ahostsv4 pve.proxmox.com >/dev/null || { echo "POST_REBOOT_ACCEPTANCE=FAIL_DNS"; exit 54; }
timeout 8s bash -c '</dev/tcp/1.1.1.1/443' || { echo "POST_REBOOT_ACCEPTANCE=FAIL_TCP443"; exit 55; }

for SERVICE_NAME in pveproxy pvedaemon pvestatd; do
  systemctl is-active --quiet "$SERVICE_NAME" || {
    echo "POST_REBOOT_ACCEPTANCE=FAIL_SERVICE_$SERVICE_NAME"
    exit 56
  }
done

touch "$STATE_DIR/POST_REBOOT_ACCEPTED"
rm -f "$STATE_DIR/PENDING_POST_REBOOT"
systemctl disable ccc-post-reboot-acceptance.service >/dev/null 2>&1 || true
sync

echo "POST_REBOOT_ACCEPTANCE=PASS"
echo "SECOND_REBOOT=PROHIBITED"
echo "RUN_DELL=OPERATIONAL_FOR_DEFINED_BOOT_NETWORK_PVE_SCOPE"
