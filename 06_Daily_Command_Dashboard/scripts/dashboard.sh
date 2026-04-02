#!/bin/bash

BASE="$HOME/FreedomArchitect/06_Daily_Command_Dashboard"

clear
echo "=================================================="
echo "          DAILY COMMAND DASHBOARD"
echo "=================================================="
echo ""
echo "1. Open Today Command"
echo "2. Open Mission Status"
echo "3. Open KPI Tracker"
echo "4. Open Daily Briefing Template"
echo "5. Open End of Day Review"
echo "6. Exit"
echo ""
read -p "Select option: " choice

case $choice in
  1) nano "$BASE/today-command.md" ;;
  2) nano "$BASE/status/mission-status.md" ;;
  3) nano "$BASE/status/kpi-tracker.md" ;;
  4) nano "$BASE/briefings/daily-briefing-template.md" ;;
  5) nano "$BASE/reviews/end-of-day-review.md" ;;
  6) exit ;;
  *) echo "Invalid option" ;;
esac
