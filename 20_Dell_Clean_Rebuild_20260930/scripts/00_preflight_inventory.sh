#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "HOLD: run as root"
  exit 20
fi

ROOT_LV="/dev/pve/root"
ROOT_MOUNT="/mnt/pve-root"
TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUTPUT_DIR="${1:-/tmp/ccc-dell-preflight-${TIMESTAMP}}"
mkdir -p "$OUTPUT_DIR"

echo "=== CCC DELL PREWIPE READ-ONLY INVENTORY ==="
echo "TIMESTAMP=$TIMESTAMP"
echo "OUTPUT_DIR=$OUTPUT_DIR"

[[ -b "$ROOT_LV" ]] || { echo "HOLD: $ROOT_LV not present"; exit 21; }

PV_DEVICE="$(pvs --noheadings -o pv_name,vg_name 2>/dev/null | awk '$2=="pve"{print $1; exit}' | xargs)"
[[ -n "$PV_DEVICE" ]] || { echo "HOLD: pve PV not resolved"; exit 22; }

PARENT_NAME="$(lsblk -no PKNAME "$PV_DEVICE" | head -n1 | xargs)"
[[ -n "$PARENT_NAME" ]] || { echo "HOLD: internal disk parent unresolved"; exit 23; }
INTERNAL_DISK="/dev/$PARENT_NAME"

ROOT_OPTIONS="$(findmnt -no OPTIONS "$ROOT_MOUNT" 2>/dev/null || true)"
if [[ -z "$ROOT_OPTIONS" ]]; then
  mkdir -p "$ROOT_MOUNT"
  mount -o ro "$ROOT_LV" "$ROOT_MOUNT"
  ROOT_OPTIONS="$(findmnt -no OPTIONS "$ROOT_MOUNT")"
fi
grep -qw "ro" <<<"${ROOT_OPTIONS//,/ }" || { echo "HOLD: installed root is not read-only"; exit 24; }

{
  echo "INTERNAL_DISK=$INTERNAL_DISK"
  echo "PV_DEVICE=$PV_DEVICE"
  echo "ROOT_LV=$ROOT_LV"
  echo "ROOT_MOUNT=$ROOT_MOUNT"
  echo "ROOT_OPTIONS=$ROOT_OPTIONS"
  lsblk -o NAME,PATH,TYPE,TRAN,RM,SIZE,FSTYPE,LABEL,UUID,MOUNTPOINTS,MODEL
} | tee "$OUTPUT_DIR/lsblk.txt"

blkid >"$OUTPUT_DIR/blkid.txt" 2>&1 || true
pvs -a -o+devices >"$OUTPUT_DIR/pvs.txt"
vgs -a >"$OUTPUT_DIR/vgs.txt"
lvs -a -o lv_name,vg_name,lv_size,data_percent,metadata_percent,devices >"$OUTPUT_DIR/lvs.txt"
findmnt >"$OUTPUT_DIR/findmnt.txt"

if command -v sfdisk >/dev/null 2>&1; then
  sfdisk -d "$INTERNAL_DISK" >"$OUTPUT_DIR/partition-table.sfdisk"
fi

echo "PREWIPE_INVENTORY=PASS"
echo "DESTRUCTIVE_ACTION=NONE"
