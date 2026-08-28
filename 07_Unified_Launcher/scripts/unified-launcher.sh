#!/usr/bin/env bash
set -u
BASE="${FA_BASE:-$HOME/FreedomArchitect}"
open_doc() { local path="$1"; if [ -f "$path" ]; then "${EDITOR:-nano}" "$path"; else echo "Missing: $path"; read -r -p "Press Enter..." _; fi; }

while true; do
  clear 2>/dev/null || true
  echo "=============================================================="
  echo "                 UNC'S WORLD — UNIFIED LAUNCHER"
  echo "=============================================================="
  echo "1. Opening Preface"
  echo "2. Operating Boundary"
  echo "3. Restart Authority"
  echo "4. Command / Mapping Map"
  echo "5. Keychain Gate Authority"
  echo "6. Revenue Work Box"
  echo "7. Today's Command"
  echo "8. Gate Status"
  echo "9. Keychain Presence Check"
  echo "10. Mission State Dashboard"
  echo "11. Executive Summary Board"
  echo "12. Daily Command Dashboard"
  echo "13. Job Scorecards"
  echo "14. Application Engine README"
  echo "15. Master Control"
  echo "16. Exit"
  read -r -p "Select option: " choice
  case "$choice" in
    1) open_doc "$BASE/06_Daily_Command_Dashboard/OPENING_PREFACE.md" ;;
    2) open_doc "$BASE/00_Admin_Control/UNC_WORLD_OPERATING_BOUNDARY_2026-08-28.md" ;;
    3) open_doc "$BASE/00_Admin_Control/RESTART_AUTHORITY_2026-08-28.md" ;;
    4) open_doc "$BASE/15_Handshake_Operating_Map/maps/unc-world-command-map.md" ;;
    5) open_doc "$BASE/15_Handshake_Operating_Map/rules/keychain-gate-authority.md" ;;
    6) open_doc "$BASE/17_Revenue_Work_Box/WORK_BOX.md" ;;
    7) open_doc "$BASE/06_Daily_Command_Dashboard/today-command.md" ;;
    8) "$BASE/15_Handshake_Operating_Map/scripts/gate-manager.sh" status; read -r -p "Press Enter..." _ ;;
    9) "$BASE/15_Handshake_Operating_Map/scripts/keychain-presence.sh"; read -r -p "Press Enter..." _ ;;
    10) [ -x "$BASE/09_Mission_State_Dashboard/scripts/mission-state.sh" ] && "$BASE/09_Mission_State_Dashboard/scripts/mission-state.sh" || { echo "Mission-state dashboard not found."; read -r -p "Press Enter..." _; } ;;
    11) [ -x "$BASE/10_Executive_Summary_Board/scripts/executive-board.sh" ] && "$BASE/10_Executive_Summary_Board/scripts/executive-board.sh" || { echo "Executive board not found."; read -r -p "Press Enter..." _; } ;;
    12) [ -x "$BASE/06_Daily_Command_Dashboard/scripts/dashboard.sh" ] && "$BASE/06_Daily_Command_Dashboard/scripts/dashboard.sh" || { echo "Daily dashboard not found."; read -r -p "Press Enter..." _; } ;;
    13) open_doc "$BASE/03_Job_Intelligence_Branch/job-scorecards.md" ;;
    14) open_doc "$BASE/05_Application_Engine/README.md" ;;
    15) open_doc "$BASE/MASTER_CONTROL.md" ;;
    16) exit 0 ;;
    *) echo "Invalid option"; sleep 1 ;;
  esac
done
