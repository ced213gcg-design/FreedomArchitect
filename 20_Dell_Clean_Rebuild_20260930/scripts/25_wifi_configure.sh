#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "HOLD: run as root"
  exit 20
fi

command -v iw >/dev/null 2>&1 || { echo "HOLD: iw unavailable"; exit 21; }
command -v wpa_supplicant >/dev/null 2>&1 || { echo "HOLD: wpa_supplicant unavailable"; exit 22; }
command -v wpa_passphrase >/dev/null 2>&1 || { echo "HOLD: wpa_passphrase unavailable"; exit 23; }

WIRELESS_INTERFACE="$(iw dev | awk '$1=="Interface"{print $2; exit}')"
[[ -n "$WIRELESS_INTERFACE" ]] || { echo "HOLD: wireless interface not detected"; exit 24; }

echo "WIRELESS_INTERFACE=$WIRELESS_INTERFACE"
ip link set "$WIRELESS_INTERFACE" up

SCAN_FILE="/tmp/ccc-wifi-scan.txt"
if ! timeout 25s iw dev "$WIRELESS_INTERFACE" scan >"$SCAN_FILE" 2>&1; then
  echo "HOLD: SCAN_TIMEOUT_OR_FAILURE"
  exit 25
fi

echo "=== BOUNDED SSID LIST ==="
grep -E '^[[:space:]]*SSID:' "$SCAN_FILE" | sed 's/^[[:space:]]*//' | sort -u | head -50

read -r -p "SSID: " WIFI_SSID
read -r -s -p "Wi-Fi password: " WIFI_PASSWORD
echo

[[ -n "$WIFI_SSID" && -n "$WIFI_PASSWORD" ]] || { echo "HOLD: empty credential input"; exit 26; }

WPA_DIR="/etc/wpa_supplicant"
WPA_FILE="$WPA_DIR/wpa_supplicant-$WIRELESS_INTERFACE.conf"
mkdir -p "$WPA_DIR"
umask 077
wpa_passphrase "$WIFI_SSID" "$WIFI_PASSWORD" | sed '/^[[:space:]]*#psk=/d' >"$WPA_FILE"
unset WIFI_PASSWORD
chmod 0600 "$WPA_FILE"

NETWORK_DIR="/etc/network/interfaces.d"
NETWORK_FILE="$NETWORK_DIR/ccc-wifi"
mkdir -p "$NETWORK_DIR"

if ! grep -Eq '^[[:space:]]*source(-directory)?[[:space:]]+/etc/network/interfaces.d/' /etc/network/interfaces; then
  printf '\nsource /etc/network/interfaces.d/*\n' >>/etc/network/interfaces
fi

cat >"$NETWORK_FILE" <<EOF
auto $WIRELESS_INTERFACE
iface $WIRELESS_INTERFACE inet dhcp
    wpa-conf $WPA_FILE
EOF
chmod 0600 "$NETWORK_FILE"

if command -v ifdown >/dev/null 2>&1; then
  ifdown "$WIRELESS_INTERFACE" 2>/dev/null || true
fi
ifup "$WIRELESS_INTERFACE"

sleep 3
ip -4 addr show dev "$WIRELESS_INTERFACE"
ip route

if ! ip -4 addr show dev "$WIRELESS_INTERFACE" | grep -q 'inet '; then
  echo "HOLD: ASSOCIATED_OR_CONFIGURED_BUT_NO_IPV4"
  exit 27
fi
if ! ip route | grep -q '^default '; then
  echo "HOLD: IPV4_PRESENT_BUT_NO_DEFAULT_ROUTE"
  exit 28
fi

echo "WIFI_CONFIGURATION=PASS"
echo "SSID=$WIFI_SSID"
echo "PASSWORD_LOGGED=NO"
