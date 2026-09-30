# CCC Dell Clean Rebuild Package v1.0.0

**Date:** 2026-09-30  
**Authority:** Human Command  
**Repository authority:** `ced213gcg-design/FreedomArchitect`  
**Source lock:** `main@cc2565379b28c5a04a8078d176dbb9285f9ce52c`  
**Package state:** BUILT_NOT_DEPLOYED  
**Destructive state:** WIPE_HOLD_UNTIL_SAVE_ALL_PASS

## Mission

Preserve the entire current Dell before destruction, perform a clean direct Proxmox installation, then install a bounded `RUN DELL` control layer that proves boot, Wi-Fi/network state, and Proxmox service health without restoring the known stale autostart loop.

## Human Command supersession

The 2026-09-17 fault record stated that the r7.2 reboot-loop defect by itself was not a reason to rebuild Proxmox. Human Command has now explicitly selected SAVE-ALL -> CLEAN REBUILD. The historical non-action remains preserved; the current rebuild direction supersedes it for this mission.

## Hard controls

- FACT BEFORE CLAIM.
- UNKNOWN != PASS.
- No wipe until full-disk SAVE-ALL hash/readback passes.
- No remembered topology is baked into this package.
- No secrets are stored in GitHub.
- No old `ccc-dell-bootstrap.service` autostart.
- No old `ccc-network-restore.service` autostart.
- No RDC logic on the Dell bootstrap path.
- No infinite Wi-Fi scan.
- No DHCP success inferred from command text alone.
- No second reboot for the same checkpoint.
- Post-reboot acceptance must close before OPERATIONAL is claimed.

## Package phases

1. `scripts/00_preflight_inventory.sh` — read-only Dell/storage inventory.
2. `scripts/10_save_all.sh <backup-mount>` — full raw NVMe image + metadata + configuration archive + source/image SHA-256 match.
3. Human verifies `SAVE_ALL_PASS.txt`.
4. Boot official verified Proxmox VE installer USB and install directly to the verified internal NVMe.
5. Copy this package to the clean Proxmox host.
6. Run `scripts/20_postinstall_baseline.sh`.
7. Run `scripts/25_wifi_configure.sh` if Wi-Fi host management is required.
8. Type exactly `RUN DELL`.
9. Dispatcher proves network/PVE boundaries, arms one-shot post-reboot acceptance, and reboots once.
10. Post-reboot service verifies acceptance and disables itself. No second reboot.
11. Apply `scripts/50_apply_topology_overlay.sh` only after the topology overlay is evidence-verified.

## Topology hold

GitHub currently proves that bridge setup and CCC-KALI-RED/qemu-guest-agent migration are preserved migration planning, but the searched build lineage did not expose exact `vmbr10`/`vmbr69` addressing. Therefore lab bridge restoration is intentionally excluded from the base rebuild.

Use `config/TOPOLOGY_OVERLAY.env.example` only after a verified GitHub or archived topology source is reconciled.

## Wipe method

The package does not contain a custom wipe script. After SAVE-ALL PASS, use the official Proxmox installer and deliberately select the exact verified internal NVMe. This removes an unnecessary destructive tool from the package and keeps the wipe tied to the installer target-selection screen.

## Acceptance

A clean rebuild is not DONE until:
- SAVE-ALL source/image hashes match;
- clean Proxmox boots;
- stale units are absent/masked;
- `RUN DELL` pre-reboot sequence passes;
- exactly one reboot occurs;
- post-reboot acceptance passes;
- Proxmox services are active;
- receipts and package hashes are preserved.
