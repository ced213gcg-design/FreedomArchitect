#!/usr/bin/env bash
set -Eeuo pipefail

if [[ "${EUID}" -ne 0 ]]; then
  echo "HOLD: run as root"
  exit 20
fi
if [[ "$#" -ne 1 ]]; then
  echo "Usage: $0 /mounted/backup/destination"
  exit 21
fi

DESTINATION="$(readlink -f "$1")"
[[ -d "$DESTINATION" ]] || { echo "HOLD: destination missing"; exit 22; }
findmnt -T "$DESTINATION" >/dev/null || { echo "HOLD: destination is not on a mounted filesystem"; exit 23; }

ROOT_LV="/dev/pve/root"
ROOT_MOUNT="/mnt/pve-root"
PV_DEVICE="$(pvs --noheadings -o pv_name,vg_name | awk '$2=="pve"{print $1; exit}' | xargs)"
[[ -n "$PV_DEVICE" ]] || { echo "HOLD: pve PV unresolved"; exit 24; }

PARENT_NAME="$(lsblk -no PKNAME "$PV_DEVICE" | head -n1 | xargs)"
INTERNAL_DISK="/dev/$PARENT_NAME"
[[ -b "$INTERNAL_DISK" ]] || { echo "HOLD: internal disk unresolved"; exit 25; }

if ! findmnt -no OPTIONS "$ROOT_MOUNT" 2>/dev/null | tr ',' '\n' | grep -qx ro; then
  echo "HOLD: installed root must be mounted read-only before SAVE-ALL"
  exit 26
fi

DISK_BYTES="$(lsblk -b -dn -o SIZE "$INTERNAL_DISK" | xargs)"
AVAILABLE_BYTES="$(df -B1 --output=avail "$DESTINATION" | tail -n1 | xargs)"
REQUIRED_BYTES=$((DISK_BYTES + 5368709120))
if (( AVAILABLE_BYTES < REQUIRED_BYTES )); then
  echo "HOLD: backup destination lacks capacity"
  echo "DISK_BYTES=$DISK_BYTES AVAILABLE_BYTES=$AVAILABLE_BYTES REQUIRED_BYTES=$REQUIRED_BYTES"
  exit 27
fi

TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
SAVE_DIR="$DESTINATION/CCC_DELL_SAVE_ALL_$TIMESTAMP"
mkdir -p "$SAVE_DIR/metadata" "$SAVE_DIR/config"

echo "=== CCC SAVE-ALL START ===" | tee "$SAVE_DIR/SAVE_ALL.log"
echo "INTERNAL_DISK=$INTERNAL_DISK" | tee -a "$SAVE_DIR/SAVE_ALL.log"
echo "DISK_BYTES=$DISK_BYTES" | tee -a "$SAVE_DIR/SAVE_ALL.log"

lsblk -o NAME,PATH,TYPE,TRAN,RM,SIZE,FSTYPE,LABEL,UUID,MOUNTPOINTS,MODEL >"$SAVE_DIR/metadata/lsblk.txt"
blkid >"$SAVE_DIR/metadata/blkid.txt" 2>&1 || true
pvs -a -o+devices >"$SAVE_DIR/metadata/pvs.txt"
vgs -a >"$SAVE_DIR/metadata/vgs.txt"
lvs -a -o lv_name,vg_name,lv_size,data_percent,metadata_percent,devices >"$SAVE_DIR/metadata/lvs.txt"
findmnt >"$SAVE_DIR/metadata/findmnt.txt"

if command -v sfdisk >/dev/null 2>&1; then
  sfdisk -d "$INTERNAL_DISK" >"$SAVE_DIR/metadata/partition-table.sfdisk"
fi
if command -v sgdisk >/dev/null 2>&1; then
  sgdisk --backup="$SAVE_DIR/metadata/gpt-backup.bin" "$INTERNAL_DISK"
fi
vgcfgbackup -f "$SAVE_DIR/metadata/pve-vgcfgbackup.conf" pve

tar --xattrs --acls --numeric-owner -C "$ROOT_MOUNT" -cpf "$SAVE_DIR/config/critical-config.tar"   etc root home opt usr/local var/lib/pve-cluster var/lib/vz/dump 2>"$SAVE_DIR/config/tar-warnings.log" || {
    echo "HOLD: critical configuration archive failed" | tee -a "$SAVE_DIR/SAVE_ALL.log"
    exit 28
  }

IMAGE_PATH="$SAVE_DIR/dell-internal-disk.raw"
echo "FULL_DISK_IMAGE_BEGIN=$(date -Is)" | tee -a "$SAVE_DIR/SAVE_ALL.log"
dd if="$INTERNAL_DISK" of="$IMAGE_PATH" bs=16M iflag=fullblock conv=noerror,sync status=progress
sync
echo "FULL_DISK_IMAGE_END=$(date -Is)" | tee -a "$SAVE_DIR/SAVE_ALL.log"

IMAGE_BYTES="$(stat -c %s "$IMAGE_PATH")"
[[ "$IMAGE_BYTES" -eq "$DISK_BYTES" ]] || { echo "HOLD: image size mismatch"; exit 29; }

echo "SOURCE_SHA256_BEGIN=$(date -Is)" | tee -a "$SAVE_DIR/SAVE_ALL.log"
SOURCE_SHA256="$(sha256sum "$INTERNAL_DISK" | awk '{print $1}')"
IMAGE_SHA256="$(sha256sum "$IMAGE_PATH" | awk '{print $1}')"
echo "SOURCE_SHA256=$SOURCE_SHA256" | tee -a "$SAVE_DIR/SAVE_ALL.log"
echo "IMAGE_SHA256=$IMAGE_SHA256" | tee -a "$SAVE_DIR/SAVE_ALL.log"

[[ "$SOURCE_SHA256" == "$IMAGE_SHA256" ]] || { echo "SAVE_ALL=FAIL_HASH_MISMATCH"; exit 30; }

(
  cd "$SAVE_DIR"
  find metadata config -type f -print0 | sort -z | xargs -0 sha256sum >ARTIFACTS.sha256
)

cat >"$SAVE_DIR/SAVE_ALL_PASS.txt" <<EOF
SAVE_ALL=PASS
TIMESTAMP=$TIMESTAMP
INTERNAL_DISK=$INTERNAL_DISK
DISK_BYTES=$DISK_BYTES
IMAGE_BYTES=$IMAGE_BYTES
SOURCE_SHA256=$SOURCE_SHA256
IMAGE_SHA256=$IMAGE_SHA256
CONFIG_ARCHIVE=critical-config.tar
METADATA=CAPTURED
WIPE_GATE=ELIGIBLE_FOR_HUMAN_TARGET_REVALIDATION
EOF

sync
echo "SAVE_ALL=PASS"
echo "WIPE_NOT_AUTOMATICALLY_AUTHORIZED=TRUE"
echo "RECEIPT=$SAVE_DIR/SAVE_ALL_PASS.txt"
