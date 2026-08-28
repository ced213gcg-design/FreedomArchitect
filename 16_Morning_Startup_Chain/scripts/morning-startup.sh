#!/usr/bin/env bash
set -u
BASE="${FA_BASE:-$HOME/FreedomArchitect}"
LOGFILE="$BASE/16_Morning_Startup_Chain/logs/morning-startup.log"
NOW="$(date '+%Y-%m-%d %H:%M:%S')"
mkdir -p "$(dirname "$LOGFILE")"

clear 2>/dev/null || true
[ -x "$BASE/08_Command_Center_Autostart/scripts/show-preface.sh" ] && "$BASE/08_Command_Center_Autostart/scripts/show-preface.sh"

echo "[1/5] Gate Status"
[ -x "$BASE/15_Handshake_Operating_Map/scripts/gate-manager.sh" ] && "$BASE/15_Handshake_Operating_Map/scripts/gate-manager.sh" status || echo "Gate manager not found."
read -r -p "Press Enter for Mission State..." _

echo "[2/5] Mission State"
[ -x "$BASE/09_Mission_State_Dashboard/scripts/mission-state.sh" ] && "$BASE/09_Mission_State_Dashboard/scripts/mission-state.sh" || echo "Mission-state dashboard not found."
read -r -p "Press Enter for Revenue Work Box..." _

echo "[3/5] Revenue Work Box"
[ -f "$BASE/17_Revenue_Work_Box/WORK_BOX.md" ] && "${PAGER:-less}" "$BASE/17_Revenue_Work_Box/WORK_BOX.md" || echo "Revenue work box not found."
read -r -p "Press Enter for Today Command..." _

echo "[4/5] Today Command"
[ -f "$BASE/06_Daily_Command_Dashboard/today-command.md" ] && "${EDITOR:-nano}" "$BASE/06_Daily_Command_Dashboard/today-command.md" || echo "Today command not found."

echo "[5/5] Startup Audit Log"
printf '[%s] Unc\047s World startup chain executed; external release not implied.\n' "$NOW" >> "$LOGFILE"
echo "Startup complete. Execute the current gate only."
