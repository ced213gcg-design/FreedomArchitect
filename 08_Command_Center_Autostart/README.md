# Command Center Autostart

## Purpose
This module turns the Freedom Architect environment into an auto-start command center.

## What It Does
- Displays a command-center banner
- Auto-launches the unified launcher when a terminal opens
- Preserves manual control through aliases
- Avoids duplicate startup inserts

## Control Notes
If you want to bypass the launcher for one session, run:
FA_SKIP_AUTOSTART=1 bash

If you want to open the launcher manually, run:
fa
