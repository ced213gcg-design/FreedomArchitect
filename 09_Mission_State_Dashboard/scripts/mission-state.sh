#!/bin/bash

STATE_FILE="$HOME/FreedomArchitect/09_Mission_State_Dashboard/status/mission-state.env"

if [ ! -f "$STATE_FILE" ]; then
  echo "Mission state file not found."
  exit 1
fi

source "$STATE_FILE"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

clear
echo -e "${CYAN}==================================================${NC}"
echo -e "${WHITE}            FREEDOM ARCHITECT MISSION STATE       ${NC}"
echo -e "${CYAN}==================================================${NC}"
echo ""
echo -e "${WHITE}CORE STATUS${NC}"
echo "----------------------------------------------"
echo -e "Mission State        : ${GREEN}$MISSION_STATE${NC}"
echo -e "Active Objective     : ${YELLOW}$ACTIVE_OBJECTIVE${NC}"
echo -e "Active Branch        : ${CYAN}$ACTIVE_BRANCH${NC}"
echo ""
echo -e "${WHITE}PUBLIC PRESENCE${NC}"
echo "----------------------------------------------"
echo -e "GitHub               : ${GREEN}$PUBLIC_GITHUB${NC}"
echo -e "LinkedIn             : ${GREEN}$PUBLIC_LINKEDIN${NC}"
echo -e "Resume Status        : ${CYAN}$RESUME_STATUS${NC}"
echo -e "Cover Letter Status  : ${CYAN}$COVER_LETTER_STATUS${NC}"
echo ""
echo -e "${WHITE}PORTFOLIO ASSETS${NC}"
echo "----------------------------------------------"
echo -e "SOC Lab              : ${GREEN}$SOC_LAB${NC}"
echo -e "Network Defense Lab  : ${GREEN}$NETWORK_DEFENSE_LAB${NC}"
echo -e "Packet Analysis Lab  : ${GREEN}$PACKET_ANALYSIS_LAB${NC}"
echo -e "Nmap Lab             : ${GREEN}$NMAP_LAB${NC}"
echo -e "Due Diligence        : ${YELLOW}$DUE_DILIGENCE_FRAMEWORK${NC}"
echo ""
echo -e "${WHITE}OPPORTUNITY METRICS${NC}"
echo "----------------------------------------------"
echo -e "Applications Sent    : $APPLICATIONS_SENT"
echo -e "Follow-Ups Sent      : $FOLLOWUPS_SENT"
echo -e "Recruiter Messages   : $RECRUITER_MESSAGES"
echo -e "Interviews Secured   : $INTERVIEWS_SECURED"
echo ""
echo -e "${WHITE}NEXT ACTION${NC}"
echo "----------------------------------------------"
echo -e "${CYAN}$NEXT_ACTION${NC}"
echo ""
echo -e "${CYAN}==================================================${NC}"
echo -e "${WHITE}Commands:${NC}"
echo "  1. Edit state      -> nano ~/FreedomArchitect/09_Mission_State_Dashboard/status/mission-state.env"
echo "  2. Run dashboard   -> ~/FreedomArchitect/09_Mission_State_Dashboard/scripts/mission-state.sh"
echo -e "${CYAN}==================================================${NC}"
