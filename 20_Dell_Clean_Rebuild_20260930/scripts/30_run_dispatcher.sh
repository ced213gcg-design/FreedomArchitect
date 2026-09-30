#!/usr/bin/env bash
set -Eeuo pipefail

STATE_ROOT="/var/lib/ccc-run-dell"
STATE_DIR="$STATE_ROOT/state"
RECEIPT_DIR="$STATE_ROOT/receipts"
LOCK_FILE="/run/ccc-run-dell.lock"
PACKAGE_ROOT="/opt/ccc/dell-clean-rebuild"
mkdir -p "$STATE_DIR" "$RECEIPT_DIR"

exec 9>"$LOCK_FILE"
flock -n 9 || { echo "HOLD: RUN DELL already active"; exit 30; }

if [[ -f "$STATE_DIR/POST_REBOOT_ACCEPTED" ]]; then
  echo "RUN_DELL=DONE"
  echo "POST_REBOOT_ACCEPTANCE=PASS"
  exit 0
fi
if [[ -f "$STATE_DIR/PENDING_POST_REBOOT" ]]; then
  echo "HOLD: reboot acceptance is pending; dispatcher will not replay"
  exit 31
fi

TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
RECEIPT="$RECEIPT_DIR/pre-reboot-$TIMESTAMP.txt"
exec > >(tee -a "$RECEIPT") 2>&1

echo "=== RUN DELL ==="
echo "TIMESTAMP=$TIMESTAMP"

echo "STATE=PRECHECK"
command -v pveversion >/dev/null 2>&1 || { echo "HOLD: pveversion missing"; exit 32; }
systemctl is-enabled ccc-dell-bootstrap.service 2>/dev/null | grep -qx masked || { echo "HOLD: stale bootstrap not masked"; exit 33; }
systemctl is-enabled ccc-network-restore.service 2>/dev/null | grep -qx masked || { echo "HOLD: stale network restore not masked"; exit 34; }

echo "STATE=DEVICE_IDENTITY"
ROOT_SOURCE="$(findmnt -no SOURCE /)"
echo "ROOT_SOURCE=$ROOT_SOURCE"
lsblk -o NAME,PATH,TYPE,TRAN,RM,SIZE,FSTYPE,MOUNTPOINTS,MODEL

echo "STATE=PAYLOAD_INTEGRITY"
if [[ -f "$PACKAGE_ROOT/checksums.sha256" ]]; then
  (cd "$PACKAGE_ROOT" && sha256sum -c checksums.sha256)
else
  echo "HOLD: package checksums missing"
  exit 35
fi

echo "STATE=INTERNAL_STAGE"
[[ -x /usr/local/sbin/RUN && -x "$PACKAGE_ROOT/scripts/40_post_reboot_acceptance.sh" ]] || {
  echo "HOLD: internal package stage incomplete"
  exit 36
}

echo "STATE=WIFI_STACK"
WIRELESS_INTERFACE="$(iw dev 2>/dev/null | awk '$1=="Interface"{print $2; exit}' || true)"
if [[ -n "$WIRELESS_INTERFACE" ]]; then
  echo "WIRELESS_INTERFACE=$WIRELESS_INTERFACE"
  command -v wpa_supplicant >/dev/null 2>&1 || { echo "HOLD: wpa_supplicant missing"; exit 37; }

  echo "STATE=BOUNDED_SCAN"
  timeout 25s iw dev "$WIRELESS_INTERFACE" scan >/tmp/ccc-run-dell-scan.txt 2>&1 || {
    echo "HOLD: SCAN_TIMEOUT_OR_FAILURE"
    exit 38
  }

  echo "STATE=NETWORK_SELECTION"
  iw dev "$WIRELESS_INTERFACE" link || true

  echo "STATE=ASSOCIATION"
  iw dev "$WIRELESS_INTERFACE" link | grep -q '^Connected to ' || {
    echo "HOLD: Wi-Fi not associated; run 25_wifi_configure.sh"
    exit 39
  }
else
  echo "WIRELESS_INTERFACE=NONE"
  echo "NETWORK_SELECTION=NON_WIFI"
fi

echo "STATE=IPV4"
ip -4 -o addr show scope global
ip -4 -o addr show scope global | grep -q 'inet ' || { echo "HOLD: no global IPv4"; exit 40; }

echo "STATE=DEFAULT_ROUTE"
ip route | tee /tmp/ccc-run-dell-routes.txt
grep -q '^default ' /tmp/ccc-run-dell-routes.txt || { echo "HOLD: no default route"; exit 41; }

echo "STATE=DNS"
getent ahostsv4 pve.proxmox.com | head -n5
getent ahostsv4 pve.proxmox.com >/dev/null || { echo "HOLD: DNS resolution failed"; exit 42; }

echo "STATE=TCP_EGRESS"
timeout 8s bash -c '</dev/tcp/1.1.1.1/443' || { echo "HOLD: TCP_443 direct-IP failed"; exit 43; }

echo "STATE=CAPTIVE_PORTAL_CLASSIFICATION"
if command -v curl >/dev/null 2>&1; then
  HTTP_CODE="$(curl -L -sS -o /dev/null -w '%{http_code}' --max-time 10 http://neverssl.com/ || true)"
  echo "CAPTIVE_CHECK_HTTP_CODE=$HTTP_CODE"
else
  echo "CAPTIVE_CHECK=UNKNOWN_CURL_UNAVAILABLE"
fi

echo "STATE=NETWORK_PERSISTENCE"
if [[ -n "$WIRELESS_INTERFACE" ]]; then
  [[ -s "/etc/network/interfaces.d/ccc-wifi" ]] || { echo "HOLD: Wi-Fi persistence file missing"; exit 44; }
fi

echo "STATE=PROXMOX_SERVICE_HEALTH"
for SERVICE_NAME in pveproxy pvedaemon pvestatd; do
  systemctl is-active --quiet "$SERVICE_NAME" || { echo "HOLD: $SERVICE_NAME inactive"; exit 45; }
  echo "$SERVICE_NAME=ACTIVE"
done

echo "STATE=RECEIPT"
echo "PRE_REBOOT_ACCEPTANCE=PASS"
touch "$STATE_DIR/PRE_REBOOT_COMPLETE"
touch "$STATE_DIR/PENDING_POST_REBOOT"

echo "STATE=REBOOT"
systemctl enable ccc-post-reboot-acceptance.service
sync

if [[ "${CCC_NO_REBOOT:-0}" == "1" ]]; then
  echo "REBOOT=ARMED_NOT_EXECUTED_CCC_NO_REBOOT"
  exit 0
fi

echo "REBOOT=ISSUED_ONCE"
systemctl reboot
