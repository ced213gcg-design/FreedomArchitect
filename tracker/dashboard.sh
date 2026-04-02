#!/bin/bash

STATUS_FILE="$HOME/FreedomArchitect/tracker/status.env"
LOG_FILE="$HOME/FreedomArchitect/tracker/daily-log.txt"

# COLORS
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# LOAD STATUS
if [ -f "$STATUS_FILE" ]; then
  source "$STATUS_FILE"
else
  echo "Status file not found."
  exit 1
fi

# PROGRESS CALCULATION
LAB_PERCENT=$((COMPLETED_LABS * 100 / TOTAL_LABS))
SYS_PERCENT=$((COMPLETED_SYSTEMS * 100 / TOTAL_SYSTEMS))

# PROGRESS BAR FUNCTION
progress_bar() {
  local percent=$1
  local filled=$((percent / 5))
  local empty=$((20 - filled))

  printf "["
  for ((i=0;i<filled;i++)); do printf "#"; done
  for ((i=0;i<empty;i++)); do printf "-"; done
  printf "] %d%%" "$percent"
}

clear

echo -e "${CYAN}==================================================${NC}"
echo -e "${WHITE}        FREEDOM ARCHITECT COMMAND DASHBOARD       ${NC}"
echo -e "${CYAN}==================================================${NC}"
echo ""

echo -e "${WHITE}IDENTITY${NC}"
echo "----------------------------------------------"
echo -e "Profile Status     : ${GREEN}$PROFILE_STATUS${NC}"
echo -e "Active Project     : ${YELLOW}$ACTIVE_PROJECT${NC}"
echo -e "Next Action        : ${CYAN}$NEXT_ACTION${NC}"
echo ""

echo -e "${WHITE}LAB PROGRESSION${NC}"
echo "----------------------------------------------"
echo -e "Labs Completed     : $COMPLETED_LABS / $TOTAL_LABS"
progress_bar $LAB_PERCENT
echo ""
echo -e "SOC Lab            : ${GREEN}$SOC_LAB_STATUS${NC}"
echo -e "Network Lab        : ${GREEN}$NETWORK_LAB_STATUS${NC}"
echo -e "Due Diligence      : ${YELLOW}$DUE_DILIGENCE_STATUS${NC}"
echo ""

echo -e "${WHITE}SYSTEM BUILD${NC}"
echo "----------------------------------------------"
echo -e "Systems Built      : $COMPLETED_SYSTEMS / $TOTAL_SYSTEMS"
progress_bar $SYS_PERCENT
echo ""

echo -e "${WHITE}CONTRIBUTION${NC}"
echo "----------------------------------------------"
echo -e "PR Status          : ${CYAN}$PR_STATUS${NC}"
echo ""

echo -e "${WHITE}DAILY STRIKE${NC}"
echo "----------------------------------------------"
echo -e "Applications       : $DAILY_APPLICATIONS"
echo -e "Follow-Ups         : $DAILY_FOLLOWUPS"
echo ""

echo -e "${WHITE}MISSION READINESS${NC}"
echo "----------------------------------------------"

if [ "$LAB_PERCENT" -ge 70 ] && [ "$SYS_PERCENT" -ge 60 ]; then
  echo -e "${GREEN}STATUS: OPERATIONAL${NC}"
else
  echo -e "${YELLOW}STATUS: BUILDING${NC}"
fi

echo ""

echo -e "${WHITE}RECENT LOG${NC}"
echo "----------------------------------------------"
tail -n 5 "$LOG_FILE" 2>/dev/null || echo "No logs yet."

echo ""
echo -e "${CYAN}==================================================${NC}"
echo -e "${WHITE}Run: ~/FreedomArchitect/tracker/dashboard.sh${NC}"
echo -e "${CYAN}==================================================${NC}"
