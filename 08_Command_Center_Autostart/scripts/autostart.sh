#!/bin/bash

# Skip autostart if explicitly disabled
if [ "$FA_SKIP_AUTOSTART" = "1" ]; then
  return 0 2>/dev/null || exit 0
fi

# Only run in interactive shells
case $- in
  *i*) ;;
  *) return 0 2>/dev/null || exit 0 ;;
esac

# Prevent repeated launcher nesting
if [ -n "$FA_AUTOSTART_RAN" ]; then
  return 0 2>/dev/null || exit 0
fi
export FA_AUTOSTART_RAN=1

# Show banner
if [ -x "$HOME/FreedomArchitect/08_Command_Center_Autostart/scripts/show-banner.sh" ]; then
  "$HOME/FreedomArchitect/08_Command_Center_Autostart/scripts/show-banner.sh"
fi

# Launch unified launcher if available
if [ -x "$HOME/FreedomArchitect/07_Unified_Launcher/scripts/unified-launcher.sh" ]; then
  "$HOME/FreedomArchitect/07_Unified_Launcher/scripts/unified-launcher.sh"
fi
