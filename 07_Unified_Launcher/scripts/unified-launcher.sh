#!/bin/bash

BASE="$HOME/FreedomArchitect"

clear
echo "=================================================="
echo "         FREEDOM ARCHITECT UNIFIED LAUNCHER       "
echo "=================================================="
echo ""
echo "1. Open MASTER_CONTROL.md"
echo "2. Open Command Map"
echo "3. Open Agent Role Matrix"
echo "4. Open Release Gate"
echo "5. Open QA Checklist"
echo "6. Open Defect Log"
echo "7. Open Daily Log"
echo "8. Open Next Actions"
echo "9. Open Job Scorecards"
echo "10. Open Reverse Engineering Notes"
echo "11. Open GitHub Release"
echo "12. Open LinkedIn Release"
echo "13. Open Application Engine README"
echo "14. Open Daily Command Dashboard"
echo "15. Run Tracker Dashboard"
echo "16. Open LinkedIn Alignment (profile repo)"
echo "17. Open Recruiter Structure (profile repo)"
echo "18. Exit"
echo ""
read -p "Select option: " choice

case $choice in
  1) nano "$BASE/MASTER_CONTROL.md" ;;
  2) nano "$BASE/00_Orchestration/command-map.md" ;;
  3) nano "$BASE/00_Orchestration/agent-role-matrix.md" ;;
  4) nano "$BASE/00_Orchestration/release-gate.md" ;;
  5) nano "$BASE/01_Audit_Branch/qa-checklist.md" ;;
  6) nano "$BASE/01_Audit_Branch/defect-log.md" ;;
  7) nano "$BASE/02_Daily_Log_Branch/daily-log.md" ;;
  8) nano "$BASE/02_Daily_Log_Branch/next-actions.md" ;;
  9) nano "$BASE/03_Job_Intelligence_Branch/job-scorecards.md" ;;
  10) nano "$BASE/03_Job_Intelligence_Branch/reverse-engineering-notes.md" ;;
  11) nano "$BASE/04_Publication_Branch/github-release.md" ;;
  12) nano "$BASE/04_Publication_Branch/linkedin-release.md" ;;
  13) nano "$BASE/05_Application_Engine/README.md" ;;
  14) "$BASE/06_Daily_Command_Dashboard/scripts/dashboard.sh" ;;
  15) "$BASE/tracker/dashboard.sh" ;;
  16) nano "$HOME/ced213gcg-design/LINKEDIN_ALIGNMENT.md" ;;
  17) nano "$HOME/ced213gcg-design/RECRUITER_STRUCTURE.md" ;;
  18) exit ;;
  *) echo "Invalid option" ;;
esac
