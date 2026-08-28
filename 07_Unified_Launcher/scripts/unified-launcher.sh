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
  echo "4. Interface Reference Lock"
  echo "5. Run Interface Gate Check"
  echo "6. Ratify Interface (Human Command only)"
  echo "7. Command / Mapping Map"
  echo "8. Keychain Gate Authority"
  echo "9. Revenue Work Box"
  echo "10. Today's Command"
  echo "11. Gate Status"
  echo "12. Keychain Presence Check"
  echo "13. Mission State Dashboard"
  echo "14. Executive Summary Board"
  echo "15. Daily Command Dashboard"
  echo "16. Job Scorecards"
  echo "17. Application Engine README"
  echo "18. Master Control"
  echo "19. Exit"
  read -r -p "Select option: " choice
  case "$choice" in
    1) open_doc "$BASE/06_Daily_Command_Dashboard/OPENING_PREFACE.md" ;;
    2) open_doc "$BASE/00_Admin_Control/UNC_WORLD_OPERATING_BOUNDARY_2026-08-28.md" ;;
    3) open_doc "$BASE/00_Admin_Control/RESTART_AUTHORITY_2026-08-28.md" ;;
    4) open_doc "$BASE/19_Interface_Reference_Lock/README.md" ;;
    5) "$BASE/19_Interface_Reference_Lock/interface-gate-check.sh"; read -r -p "Press Enter..." _ ;;
    6)
      read -r -p "After visually confirming the exact approved interface, type RATIFY: " approval
      if [ "$approval" = "RATIFY" ]; then "$BASE/19_Interface_Reference_Lock/ratify-interface.sh" RATIFY; else echo "Ratification cancelled."; fi
      read -r -p "Press Enter..." _
      ;;
    7) open_doc "$BASE/15_Handshake_Operating_Map/maps/unc-world-command-map.md" ;;
    8) open_doc "$BASE/15_Handshake_Operating_Map/rules/keychain-gate-authority.md" ;;
    9) open_doc "$BASE/17_Revenue_Work_Box/WORK_BOX.md" ;;
    10) open_doc "$BASE/06_Daily_Command_Dashboard/today-command.md" ;;
    11) "$BASE/15_Handshake_Operating_Map/scripts/gate-manager.sh" status; read -r -p "Press Enter..." _ ;;
    12) "$BASE/15_Handshake_Operating_Map/scripts/keychain-presence.sh"; read -r -p "Press Enter..." _ ;;
    13) [ -x "$BASE/09_Mission_State_Dashboard/scripts/mission-state.sh" ] && "$BASE/09_Mission_State_Dashboard/scripts/mission-state.sh" || { echo "Mission-state dashboard not found."; read -r -p "Press Enter..." _; } ;;
    14) [ -x "$BASE/10_Executive_Summary_Board/scripts/executive-board.sh" ] && "$BASE/10_Executive_Summary_Board/scripts/executive-board.sh" || { echo "Executive board not found."; read -r -p "Press Enter..." _; } ;;
    15) [ -x "$BASE/06_Daily_Command_Dashboard/scripts/dashboard.sh" ] && "$BASE/06_Daily_Command_Dashboard/scripts/dashboard.sh" || { echo "Daily dashboard not found."; read -r -p "Press Enter..." _; } ;;
    16) open_doc "$BASE/03_Job_Intelligence_Branch/job-scorecards.md" ;;
    17) open_doc "$BASE/05_Application_Engine/README.md" ;;
    18) open_doc "$BASE/MASTER_CONTROL.md" ;;
    19) exit 0 ;;
    *) echo "Invalid option"; sleep 1 ;;
  esac
done
