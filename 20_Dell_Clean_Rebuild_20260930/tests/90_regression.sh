#!/usr/bin/env bash
set -Eeuo pipefail

PACKAGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PASS_COUNT=0
FAIL_COUNT=0

pass() {
  PASS_COUNT=$((PASS_COUNT+1))
  printf 'PASS %03d %s\n' "$PASS_COUNT" "$1"
}
fail() {
  FAIL_COUNT=$((FAIL_COUNT+1))
  printf 'FAIL %03d %s\n' "$FAIL_COUNT" "$1"
}

grep -q 'UNKNOWN != PASS' "$PACKAGE_ROOT/README.md" && pass "truth firewall" || fail "truth firewall"
grep -q 'No second reboot' "$PACKAGE_ROOT/README.md" && pass "reboot loop doctrine" || fail "reboot loop doctrine"

if grep -RniE 'enable[[:space:]]+ccc-dell-bootstrap|enable[[:space:]]+ccc-network-restore' "$PACKAGE_ROOT" \
  --exclude='90_regression.sh' >/tmp/ccc-regression-stale-enable.txt 2>/dev/null; then
  fail "stale services are never enabled"
  cat /tmp/ccc-regression-stale-enable.txt
else
  pass "stale services are never enabled"
fi

grep -q 'systemctl mask ccc-dell-bootstrap.service' "$PACKAGE_ROOT/scripts/20_postinstall_baseline.sh" \
  && pass "stale bootstrap masked" || fail "stale bootstrap masked"

grep -q 'systemctl mask ccc-network-restore.service' "$PACKAGE_ROOT/scripts/20_postinstall_baseline.sh" \
  && pass "stale network restore masked" || fail "stale network restore masked"

grep -q 'timeout 25s iw dev' "$PACKAGE_ROOT/scripts/30_run_dispatcher.sh" \
  && pass "bounded Wi-Fi scan" || fail "bounded Wi-Fi scan"

grep -q 'scope global' "$PACKAGE_ROOT/scripts/30_run_dispatcher.sh" \
  && pass "global IPv4 required" || fail "global IPv4 required"

grep -q 'PENDING_POST_REBOOT' "$PACKAGE_ROOT/scripts/30_run_dispatcher.sh" \
  && pass "pending reboot checkpoint" || fail "pending reboot checkpoint"

grep -q 'POST_REBOOT_ACCEPTED' "$PACKAGE_ROOT/scripts/40_post_reboot_acceptance.sh" \
  && pass "post reboot accepted checkpoint" || fail "post reboot accepted checkpoint"

if grep -q 'systemctl reboot' "$PACKAGE_ROOT/scripts/40_post_reboot_acceptance.sh"; then
  fail "post reboot script issues no reboot"
else
  pass "post reboot script issues no reboot"
fi

grep -q 'SOURCE_SHA256=' "$PACKAGE_ROOT/scripts/10_save_all.sh" \
  && grep -q 'IMAGE_SHA256=' "$PACKAGE_ROOT/scripts/10_save_all.sh" \
  && grep -q 'SOURCE_SHA256.*IMAGE_SHA256' "$PACKAGE_ROOT/scripts/10_save_all.sh" \
  && pass "SAVE-ALL source/image hash comparison" || fail "SAVE-ALL source/image hash comparison"

grep -q 'unsuitable SAVE-ALL destination filesystem' "$PACKAGE_ROOT/scripts/10_save_all.sh" \
  && pass "SAVE-ALL destination guard" || fail "SAVE-ALL destination guard"

grep -q 'PASSWORD_LOGGED=NO' "$PACKAGE_ROOT/scripts/25_wifi_configure.sh" \
  && pass "Wi-Fi secret not logged" || fail "Wi-Fi secret not logged"

RUN_COUNT=$((PASS_COUNT+FAIL_COUNT))
echo "REGRESSION_RUN_COUNT=$RUN_COUNT"
echo "REGRESSION_PASS_COUNT=$PASS_COUNT"
echo "REGRESSION_FAIL_COUNT=$FAIL_COUNT"

if (( FAIL_COUNT == 0 )); then
  echo "REGRESSION_STATUS=PASS"
  exit 0
fi

echo "REGRESSION_STATUS=FAIL"
exit 1
