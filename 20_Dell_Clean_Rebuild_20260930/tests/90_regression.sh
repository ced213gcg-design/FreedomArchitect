#!/usr/bin/env bash
set -Eeuo pipefail

PACKAGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAIL_COUNT=0

pass() { printf 'PASS %s\n' "$1"; }
fail() { printf 'FAIL %s\n' "$1"; FAIL_COUNT=$((FAIL_COUNT+1)); }

grep -q 'UNKNOWN != PASS' "$PACKAGE_ROOT/README.md" && pass "truth firewall" || fail "truth firewall"
grep -q 'No second reboot' "$PACKAGE_ROOT/README.md" && pass "reboot loop doctrine" || fail "reboot loop doctrine"

if grep -RniE 'enable[[:space:]]+ccc-dell-bootstrap|enable[[:space:]]+ccc-network-restore' "$PACKAGE_ROOT"   --exclude='90_regression.sh' >/tmp/ccc-regression-stale-enable.txt 2>/dev/null; then
  fail "stale services are never enabled"
  cat /tmp/ccc-regression-stale-enable.txt
else
  pass "stale services are never enabled"
fi

grep -q 'systemctl mask ccc-dell-bootstrap.service' "$PACKAGE_ROOT/scripts/20_postinstall_baseline.sh"   && pass "stale bootstrap masked" || fail "stale bootstrap masked"

grep -q 'systemctl mask ccc-network-restore.service' "$PACKAGE_ROOT/scripts/20_postinstall_baseline.sh"   && pass "stale network restore masked" || fail "stale network restore masked"

grep -q 'timeout 25s iw dev' "$PACKAGE_ROOT/scripts/30_run_dispatcher.sh"   && pass "bounded Wi-Fi scan" || fail "bounded Wi-Fi scan"

grep -q 'PENDING_POST_REBOOT' "$PACKAGE_ROOT/scripts/30_run_dispatcher.sh"   && pass "pending reboot checkpoint" || fail "pending reboot checkpoint"

grep -q 'POST_REBOOT_ACCEPTED' "$PACKAGE_ROOT/scripts/40_post_reboot_acceptance.sh"   && pass "post reboot accepted checkpoint" || fail "post reboot accepted checkpoint"

if grep -q 'systemctl reboot' "$PACKAGE_ROOT/scripts/40_post_reboot_acceptance.sh"; then
  fail "post reboot script issues no reboot"
else
  pass "post reboot script issues no reboot"
fi

grep -q 'SOURCE_SHA256.*IMAGE_SHA256' "$PACKAGE_ROOT/scripts/10_save_all.sh"   && pass "SAVE-ALL source/image hash comparison" || fail "SAVE-ALL source/image hash comparison"

grep -q 'PASSWORD_LOGGED=NO' "$PACKAGE_ROOT/scripts/25_wifi_configure.sh"   && pass "Wi-Fi secret not logged" || fail "Wi-Fi secret not logged"

if (( FAIL_COUNT == 0 )); then
  echo "REGRESSION_PASS=10"
  echo "REGRESSION_FAIL=0"
  exit 0
fi

echo "REGRESSION_FAIL=$FAIL_COUNT"
exit 1
