#!/bin/bash

STATE_FILE="$HOME/FreedomArchitect/10_Executive_Summary_Board/board/executive-state.env"

if [ ! -f "$STATE_FILE" ]; then
  echo "Executive state file not found."
  exit 1
fi

source "$STATE_FILE"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
RED='\033[0;31m'
NC='\033[0m'

clear
echo -e "${CYAN}==================================================${NC}"
echo -e "${WHITE}          FREEDOM ARCHITECT EXECUTIVE BOARD       ${NC}"
echo -e "${CYAN}==================================================${NC}"
echo ""
echo -e "${WHITE}MISSION${NC}"
echo "----------------------------------------------"
echo -e "${YELLOW}$MISSION_SUMMARY${NC}"
echo ""
echo -e "${WHITE}PUBLIC PLATFORM STATE${NC}"
echo "----------------------------------------------"
echo -e "GitHub Status        : ${GREEN}$GITHUB_STATUS${NC}"
echo -e "LinkedIn Status      : ${GREEN}$LINKEDIN_STATUS${NC}"
echo -e "Profile Status       : ${CYAN}$PROFILE_STATUS${NC}"
echo -e "Portfolio Signal     : ${GREEN}$PORTFOLIO_SIGNAL${NC}"
echo ""
echo -e "${WHITE}PORTFOLIO ASSETS${NC}"
echo "----------------------------------------------"
echo -e "SOC Lab              : ${GREEN}$SOC_LAB_STATUS${NC}"
echo -e "Network Defense      : ${GREEN}$NETWORK_DEFENSE_STATUS${NC}"
echo -e "Packet Analysis      : ${GREEN}$PACKET_ANALYSIS_STATUS${NC}"
echo -e "Nmap Lab             : ${GREEN}$NMAP_STATUS${NC}"
echo -e "Due Diligence        : ${YELLOW}$DUE_DILIGENCE_STATUS${NC}"
echo ""
echo -e "${WHITE}HIRING PIPELINE${NC}"
echo "----------------------------------------------"
echo -e "Pipeline State       : ${CYAN}$APPLICATION_PIPELINE${NC}"
echo -e "Applications Sent    : $APPLICATION_COUNT"
echo -e "Recruiter Outreach   : $RECRUITER_OUTREACH"
echo -e "Follow-Ups           : $FOLLOWUP_COUNT"
echo -e "Interviews Secured   : $INTERVIEWS"
echo ""
echo -e "${WHITE}CURRENT RISK${NC}"
echo "----------------------------------------------"
echo -e "${RED}$PRIMARY_RISK${NC}"
echo ""
echo -e "${WHITE}NEXT EXECUTIVE MOVE${NC}"
echo "----------------------------------------------"
echo -e "${CYAN}$NEXT_EXECUTIVE_MOVE${NC}"
echo ""
echo -e "${CYAN}==================================================${NC}"
echo -e "${WHITE}Commands:${NC}"
echo "  1. Edit executive state -> nano ~/FreedomArchitect/10_Executive_Summary_Board/board/executive-state.env"
echo "  2. Open summary board   -> nano ~/FreedomArchitect/10_Executive_Summary_Board/board/executive-summary.md"
echo "  3. Run board            -> ~/FreedomArchitect/10_Executive_Summary_Board/scripts/executive-board.sh"
echo -e "${CYAN}==================================================${NC}"
