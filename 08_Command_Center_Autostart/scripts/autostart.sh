#!/usr/bin/env bash

if [ "${FA_SKIP_AUTOSTART:-0}" = "1" ]; then return 0 2>/dev/null || exit 0; fi
case $- in *i*) ;; *) return 0 2>/dev/null || exit 0 ;; esac
if [ -n "${FA_AUTOSTART_RAN:-}" ]; then return 0 2>/dev/null || exit 0; fi
export FA_AUTOSTART_RAN=1
BASE="${FA_BASE:-$HOME/FreedomArchitect}"

if [ -x "$BASE/08_Command_Center_Autostart/scripts/show-preface.sh" ]; then
  "$BASE/08_Command_Center_Autostart/scripts/show-preface.sh"
elif [ -x "$BASE/08_Command_Center_Autostart/scripts/show-banner.sh" ]; then
  "$BASE/08_Command_Center_Autostart/scripts/show-banner.sh"
fi

if [ -x "$BASE/07_Unified_Launcher/scripts/unified-launcher.sh" ]; then
  "$BASE/07_Unified_Launcher/scripts/unified-launcher.sh"
fi
