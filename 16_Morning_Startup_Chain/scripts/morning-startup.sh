#!/bin/bash

BASE="$HOME/FreedomArchitect"
LOGFILE="$BASE/16_Morning_Startup_Chain/logs/morning-startup.log"
NOW="$(date '+%Y-%m-%d %H:%M:%S')"

clear
echo "=================================================="
echo "        FREEDOM ARCHITECT MORNING STARTUP         "
echo "=================================================="
echo " Time: $NOW"
echo "=================================================="
echo ""

echo "[1/6] Mission State Dashboard"
if [ -x "$BASE/09_Mission_State_Dashboard/scripts/mission-state.sh" ]; then
  "$BASE/09_Mission_State_Dashboard/scripts/mission-state.sh"
else
  echo "Mission-state dashboard not found."
fi

echo ""
read -p "Press Enter to continue to Executive Summary..."

echo "[2/6] Executive Summary Board"
if [ -x "$BASE/10_Executive_Summary_Board/scripts/executive-board.sh" ]; then
  "$BASE/10_Executive_Summary_Board/scripts/executive-board.sh"
else
  echo "Executive board not found."
fi

echo ""
read -p "Press Enter to continue to Job Finder..."

echo "[3/6] Auto Job Finder"
if [ -x "$BASE/11_Auto_Job_Finder/scripts/run-job-finder.sh" ]; then
  "$BASE/11_Auto_Job_Finder/scripts/run-job-finder.sh"
else
  echo "Job finder not found."
fi

echo ""
read -p "Press Enter to open Today Command..."

echo "[4/6] Opening Today Command"
nano "$BASE/06_Daily_Command_Dashboard/today-command.md"

echo ""
read -p "Press Enter to open KPI Tracker..."

echo "[5/6] Opening KPI Tracker"
nano "$BASE/06_Daily_Command_Dashboard/status/kpi-tracker.md"

echo ""
echo "[6/6] Writing startup log entry"
echo "[$NOW] Morning startup chain executed." >> "$LOGFILE"

echo ""
echo "=================================================="
echo " Morning startup complete."
echo " Next move: execute applications, outreach, and follow-ups."
echo "=================================================="
