#!/bin/bash



# ==========================================

# FREEDOM ARCHITECT OPERATIONS CONSOLE

# Audited Integrated Build

# ==========================================



# ---------- Colors ----------

RED="\033[31m"

GREEN="\033[32m"

CYAN="\033[36m"

YELLOW="\033[33m"

BOLD="\033[1m"

RESET="\033[0m"



# ---------- Paths ----------

FA_HOME="$HOME/FreedomArchitect"

SYNC_HOME="$HOME/FreedomArchitect_Sync"

CONTROL_DIR="$SYNC_HOME/control"

ASSIST_DIR="$FA_HOME/00_Admin_Control/assistant"

ARCHIVE_DIR="$FA_HOME/99_Encrypted_Archive"

CYBER_DIR="$FA_HOME/01_Cybersecurity"

GITHUB_DIR="$CYBER_DIR/GitHub"

MANUSCRIPT_DIR="$FA_HOME/02_Manuscripts"

LOCKKEY_DIR="$FA_HOME/03_Lock_and_Key"

SINTRA_DIR="$FA_HOME/10_Sintra_Operations"

DASHBOARD_TXT="$SYNC_HOME/dashboard.txt"

DASHBOARD_HTML="$SYNC_HOME/Freedom_Architect_Dashboard.html"



# ---------- Helpers ----------

pause() {

  echo

  read -r -p "Press ENTER to continue..." _

}



safe_open_url() {

  local url="$1"

  xdg-open "$url" >/dev/null 2>&1 &

}



require_tool() {

  command -v "$1" >/dev/null 2>&1

}



ensure_layout() {

  mkdir -p "$FA_HOME"/{00_Admin_Control,01_Cybersecurity,02_Manuscripts,03_Lock_and_Key,04_Pipeline_Funding,05_Capital_Engine,06_Trust_and_Ownership,07_Protocols,08_System_Setup,09_Phone_Sync,10_Sintra_Operations,99_Encrypted_Archive}

  mkdir -p "$CYBER_DIR"/{GitHub,Labs,PCAP_Analysis,Tools,Portfolio,Cyber_Lab}

  mkdir -p "$SINTRA_DIR"/{workflows,trend_reports,outreach,accountability}

  mkdir -p "$SYNC_HOME" "$CONTROL_DIR" "$ASSIST_DIR" "$ARCHIVE_DIR"



  touch "$CONTROL_DIR"/today.txt

  touch "$CONTROL_DIR"/progress.log

  touch "$CONTROL_DIR"/project_status.txt

  touch "$CONTROL_DIR"/questions.txt

  touch "$CONTROL_DIR"/daily_review.txt

  touch "$CONTROL_DIR"/career_log.txt



  touch "$ASSIST_DIR"/inbox.txt

  touch "$ASSIST_DIR"/heartbeat.log

  touch "$ASSIST_DIR"/questions.txt

  touch "$ASSIST_DIR"/daily_review.txt



  if [ ! -s "$CONTROL_DIR/project_status.txt" ]; then

    cat > "$CONTROL_DIR/project_status.txt" <<'TXT'

Freedom Architect Project Status



Cyber Command:

- Console integrated

- Nmap available

- GitHub workspace ready



Operations:

- Manuscripts workspace ready

- Lock & Key workspace ready

- Sintra operations workspace ready



Next Priorities:

- Strengthen Cyber Lab

- Build portfolio evidence

- Maintain workflow logs

TXT

  fi



  if [ ! -s "$CONTROL_DIR/today.txt" ]; then

    cat > "$CONTROL_DIR/today.txt" <<'TXT'

Today's Goals

1. Run one authorized cyber lab task

2. Update one project or repo

3. Record one progress note

4. Review diagnostics and backup posture

TXT

  fi



  if [ ! -s "$CONTROL_DIR/daily_review.txt" ]; then

    cat > "$CONTROL_DIR/daily_review.txt" <<'TXT'

Daily Review

- What was the main cyber task?

- What project moved forward?

- What was completed?

- What needs review or backup?

TXT

  fi



  if [ ! -s "$DASHBOARD_TXT" ]; then

    cat > "$DASHBOARD_TXT" <<'TXT'

Freedom Architect Dashboard



CYBER COMMAND

- Lab ready

- GitHub workspace ready



PROJECT STATUS

- Use project_status.txt for current state



TODAY'S GOALS

- Use today.txt



NEXT STEP

- Execute one strong task, log it, review it

TXT

  fi

}



banner() {

  clear

  echo -e "${CYAN}${BOLD}========================================================${RESET}"

  echo -e "${CYAN}${BOLD}          FREEDOM ARCHITECT OPERATIONS CONSOLE${RESET}"

  echo -e "${CYAN}${BOLD}========================================================${RESET}"

  echo "User:    $(whoami)"

  echo "Host:    $(hostname)"

  echo "Kernel:  $(uname -r)"

  echo "IP:      $(hostname -I | awk '{print $1}')"

  echo "Time:    $(date)"

  echo

}



# ---------- Core Views ----------

show_today() {

  clear

  echo -e "${GREEN}${BOLD}TODAY'S GOALS${RESET}"

  echo "----------------------------------------"

  cat "$CONTROL_DIR/today.txt"

  pause

}



show_project_status() {

  clear

  echo -e "${GREEN}${BOLD}PROJECT STATUS${RESET}"

  echo "----------------------------------------"

  cat "$CONTROL_DIR/project_status.txt"

  pause

}



show_daily_review() {

  clear

  echo -e "${GREEN}${BOLD}DAILY REVIEW${RESET}"

  echo "----------------------------------------"

  cat "$CONTROL_DIR/daily_review.txt"

  pause

}



record_progress() {

  clear

  echo -e "${GREEN}${BOLD}PROGRESS LOG${RESET}"

  echo "----------------------------------------"

  read -r -p "Enter progress update: " note

  if [ -n "$note" ]; then

    echo "$(date '+%Y-%m-%d %H:%M:%S') | $note" >> "$CONTROL_DIR/progress.log"

    echo "Saved."

  else

    echo "Nothing entered."

  fi

  pause

}



open_progress_log() {

  nano "$CONTROL_DIR/progress.log"

}



open_questions_queue() {

  nano "$CONTROL_DIR/questions.txt"

}



add_assistant_question() {

  clear

  echo -e "${CYAN}${BOLD}ASSISTANT QUESTION / TASK${RESET}"

  echo "----------------------------------------"

  read -r -p "Enter question or task: " q

  if [ -n "$q" ]; then

    echo "$(date '+%Y-%m-%d %H:%M:%S') | $q" >> "$CONTROL_DIR/questions.txt"

    echo "$(date '+%Y-%m-%d %H:%M:%S') | $q" >> "$ASSIST_DIR/questions.txt"

    echo "Saved."

  else

    echo "Nothing entered."

  fi

  pause

}



view_assistant_inbox() {

  clear

  echo -e "${CYAN}${BOLD}ASSISTANT INBOX${RESET}"

  echo "----------------------------------------"

  cat "$ASSIST_DIR/inbox.txt"

  pause

}



log_heartbeat() {

  echo "$(date '+%Y-%m-%d %H:%M:%S') | Freedom Architect heartbeat active." >> "$ASSIST_DIR/heartbeat.log"

  echo "$(date '+%Y-%m-%d %H:%M:%S') | Review cyber tasks, backups, and progress." >> "$ASSIST_DIR/heartbeat.log"

  echo "Heartbeat logged."

  pause

}



view_heartbeat() {

  clear

  echo -e "${CYAN}${BOLD}HEARTBEAT LOG${RESET}"

  echo "----------------------------------------"

  cat "$ASSIST_DIR/heartbeat.log"

  pause

}



# ---------- Diagnostics ----------

diagnostics() {

  clear

  echo -e "${YELLOW}${BOLD}SYSTEM DIAGNOSTICS${RESET}"

  echo "----------------------------------------"

  echo "Uptime / Load:"

  uptime

  echo

  echo "Memory:"

  free -h

  echo

  echo "Disk:"

  df -h

  echo

  echo "Network Interfaces:"

  if require_tool ip; then

    ip -brief addr 2>/dev/null || ip addr

  else

    ifconfig 2>/dev/null || echo "No network tool found."

  fi

  echo

  echo "Listening Ports:"

  ss -tuln 2>/dev/null | head -n 25 || echo "ss not available."

  echo

  echo "Tool Versions:"

  python3 --version 2>/dev/null || true

  git --version 2>/dev/null || true

  nmap --version 2>/dev/null | head -n 1 || true

  echo

  pause

}



# ---------- Backups ----------

backup_standard() {

  clear

  local out="$ARCHIVE_DIR/freedom_backup_$(date +%Y%m%d_%H%M%S).tar.gz"

  tar -czf "$out" "$FA_HOME" "$SYNC_HOME" 2>/dev/null

  echo "Standard backup created:"

  echo "$out"

  pause

}



backup_encrypted() {

  clear

  local out="$ARCHIVE_DIR/freedom_secure_$(date +%Y%m%d_%H%M%S).zip"

  if require_tool zip; then

    zip -r -e "$out" "$FA_HOME" "$SYNC_HOME" >/dev/null 2>&1

    echo "Encrypted backup created:"

    echo "$out"

  else

    echo "zip is not installed."

    echo "Install with: sudo apt install zip"

  fi

  pause

}



snapshot() {

  clear

  local snap="$CONTROL_DIR/system_snapshot_$(date +%Y%m%d_%H%M%S).txt"

  {

    echo "Freedom Architect System Snapshot"

    echo "Timestamp: $(date)"

    echo

    echo "=== TODAY ==="

    cat "$CONTROL_DIR/today.txt"

    echo

    echo "=== PROJECT STATUS ==="

    cat "$CONTROL_DIR/project_status.txt"

    echo

    echo "=== MEMORY ==="

    free -h

    echo

    echo "=== DISK ==="

    df -h

    echo

    echo "=== IP ==="

    hostname -I

  } > "$snap"

  echo "Snapshot created:"

  echo "$snap"

  pause

}



# ---------- Workflows ----------

guided_workflow() {

  clear

  echo -e "${CYAN}${BOLD}GUIDED WORKFLOW${RESET}"

  echo "----------------------------------------"

  read -r -p "Today's main cyber task: " cybertask

  read -r -p "Main project movement: " projectmove

  read -r -p "Completed today: " completed

  read -r -p "Needs backup / review: " backupneed



  {

    echo "Daily Review - $(date)"

    echo

    echo "Cyber Task: $cybertask"

    echo "Project Move: $projectmove"

    echo "Completed: $completed"

    echo "Needs Review: $backupneed"

  } > "$CONTROL_DIR/daily_review.txt"



  {

    echo "$(date '+%Y-%m-%d %H:%M:%S') | Cyber Task | $cybertask"

    echo "$(date '+%Y-%m-%d %H:%M:%S') | Project Move | $projectmove"

    echo "$(date '+%Y-%m-%d %H:%M:%S') | Completed | $completed"

    echo "$(date '+%Y-%m-%d %H:%M:%S') | Review | $backupneed"

  } >> "$CONTROL_DIR/progress.log"



  {

    echo "Today's Goals - $(date)"

    echo "1. $cybertask"

    echo "2. $projectmove"

    echo "3. Review completion: $completed"

    echo "4. Backup / review: $backupneed"

  } > "$CONTROL_DIR/today.txt"



  echo "Workflow saved."

  pause

}



career_mode() {

  clear

  echo -e "${CYAN}${BOLD}CYBER CAREER MODE${RESET}"

  echo "----------------------------------------"

  read -r -p "Skill studied today: " skill

  read -r -p "Lab or tool practiced: " lab

  read -r -p "Repo or project touched: " repo

  read -r -p "Career action taken: " action



  {

    echo "$(date '+%Y-%m-%d %H:%M:%S') | Skill | $skill"

    echo "$(date '+%Y-%m-%d %H:%M:%S') | Lab | $lab"

    echo "$(date '+%Y-%m-%d %H:%M:%S') | Repo | $repo"

    echo "$(date '+%Y-%m-%d %H:%M:%S') | Action | $action"

  } >> "$CONTROL_DIR/career_log.txt"



  echo "Career progress saved."

  pause

}



# ---------- Workspace Navigation ----------

open_workspace() {

  local dir="$1"

  clear

  cd "$dir" 2>/dev/null || { echo "Directory not found: $dir"; pause; return; }

  pwd

  echo

  ls

  pause

}



operations_menu() {

  while true; do

    clear

    echo -e "${GREEN}${BOLD}OPERATIONS WORKSPACES${RESET}"

    echo "----------------------------------------"

    echo "1) 01_Cybersecurity"

    echo "2) 02_Manuscripts"

    echo "3) 03_Lock_and_Key"

    echo "4) 10_Sintra_Operations"

    echo "5) Control files"

    echo "6) Back"

    echo

    read -r -p "Select option: " ochoice



    case "$ochoice" in

      1) open_workspace "$CYBER_DIR" ;;

      2) open_workspace "$MANUSCRIPT_DIR" ;;

      3) open_workspace "$LOCKKEY_DIR" ;;

      4) open_workspace "$SINTRA_DIR" ;;

      5) open_workspace "$CONTROL_DIR" ;;

      6) return ;;

      *) echo "Invalid selection."; sleep 1 ;;

    esac

  done

}



# ---------- GitHub ----------

github_menu() {

  while true; do

    clear

    echo -e "${CYAN}${BOLD}GITHUB WORKSPACE${RESET}"

    echo "----------------------------------------"

    echo "1) Open GitHub folder"

    echo "2) Git status"

    echo "3) Git pull"

    echo "4) Git add + commit + push"

    echo "5) Back"

    echo

    read -r -p "Select option: " gchoice



    case "$gchoice" in

      1)

        open_workspace "$GITHUB_DIR"

        ;;

      2)

        clear

        cd "$GITHUB_DIR" 2>/dev/null || { echo "GitHub folder not found."; pause; continue; }

        git status

        pause

        ;;

      3)

        clear

        cd "$GITHUB_DIR" 2>/dev/null || { echo "GitHub folder not found."; pause; continue; }

        git pull

        pause

        ;;

      4)

        clear

        cd "$GITHUB_DIR" 2>/dev/null || { echo "GitHub folder not found."; pause; continue; }

        git add .

        read -r -p "Commit message: " msg

        if [ -n "$msg" ]; then

          git commit -m "$msg" && git push

        else

          echo "Commit message cannot be empty."

        fi

        pause

        ;;

      5)

        return

        ;;

      *)

        echo "Invalid selection."

        sleep 1

        ;;

    esac

  done

}



# ---------- Cyber Lab ----------

cyber_lab_menu() {

  while true; do

    clear

    echo -e "${YELLOW}${BOLD}CYBERSECURITY LAB${RESET}"

    echo "Authorized systems only."

    echo "----------------------------------------"

    echo "1) Fast scan"

    echo "2) Service scan"

    echo "3) Local network discovery"

    echo "4) Launch Wireshark"

    echo "5) Back"

    echo

    read -r -p "Select option: " cchoice



    case "$cchoice" in

      1)

        clear

        read -r -p "Enter target IP or hostname: " target

        echo

        nmap -Pn -F "$target"

        pause

        ;;

      2)

        clear

        read -r -p "Enter target IP or hostname: " target

        echo

        nmap -Pn -sV --top-ports 100 "$target"

        pause

        ;;

      3)

        clear

        local_cidr="$(ip route 2>/dev/null | awk '/proto kernel/ && $1 ~ /\// {print $1; exit}')"

        echo "Detected local network: ${local_cidr:-not found}"

        read -r -p "Enter network CIDR to scan [Enter = detected]: " netinput

        target_net="${netinput:-$local_cidr}"

        if [ -n "$target_net" ]; then

          echo

          nmap -sn "$target_net"

        else

          echo "No network CIDR available."

        fi

        pause

        ;;

      4)

        clear

        if require_tool wireshark; then

          wireshark >/dev/null 2>&1 &

          echo "Wireshark launched."

        else

          echo "Wireshark not installed."

          echo "Install with: sudo apt install wireshark"

        fi

        pause

        ;;

      5)

        return

        ;;

      *)

        echo "Invalid selection."

        sleep 1

        ;;

    esac

  done

}



# ---------- Research ----------

research_menu() {

  while true; do

    clear

    echo -e "${CYAN}${BOLD}AI / RESEARCH${RESET}"

    echo "----------------------------------------"

    echo "1) ChatGPT"

    echo "2) Perplexity"

    echo "3) Search engine"

    echo "4) Back"

    echo

    read -r -p "Select option: " rchoice



    case "$rchoice" in

      1) safe_open_url "https://chat.openai.com"; echo "Opening ChatGPT..."; pause ;;

      2) safe_open_url "https://www.perplexity.ai"; echo "Opening Perplexity..."; pause ;;

      3) safe_open_url "https://www.google.com"; echo "Opening search..."; pause ;;

      4) return ;;

      *) echo "Invalid selection."; sleep 1 ;;

    esac

  done

}



# ---------- Dashboard ----------

dashboard_menu() {

  while true; do

    clear

    echo -e "${CYAN}${BOLD}DASHBOARD / SYNC${RESET}"

    echo "----------------------------------------"

    echo "1) Open text dashboard"

    echo "2) Open HTML dashboard"

    echo "3) Edit today's goals"

    echo "4) Edit project status"

    echo "5) Edit questions queue"

    echo "6) Open progress log"

    echo "7) Back"

    echo

    read -r -p "Select option: " dchoice



    case "$dchoice" in

      1) nano "$DASHBOARD_TXT" ;;

      2)

        if [ -f "$DASHBOARD_HTML" ]; then

          xdg-open "$DASHBOARD_HTML" >/dev/null 2>&1 &

          echo "Opening HTML dashboard..."

        else

          echo "HTML dashboard file not found."

        fi

        pause

        ;;

      3) nano "$CONTROL_DIR/today.txt" ;;

      4) nano "$CONTROL_DIR/project_status.txt" ;;

      5) nano "$CONTROL_DIR/questions.txt" ;;

      6) nano "$CONTROL_DIR/progress.log" ;;

      7) return ;;

      *) echo "Invalid selection."; sleep 1 ;;

    esac

  done

}



# ---------- Main ----------

main_menu() {

  while true; do

    banner

    echo "1) Cybersecurity Lab"

    echo "2) GitHub Workspace"

    echo "3) Operations Workspaces"

    echo "4) AI / Research"

    echo "5) Diagnostics"

    echo "6) Guided Workflow"

    echo "7) Cyber Career Mode"

    echo "8) Dashboard / Sync"

    echo "9) View Today's Goals"

    echo "10) View Project Status"

    echo "11) Record Progress Note"

    echo "12) Add Assistant Question"

    echo "13) View Assistant Inbox"

    echo "14) Log Heartbeat"

    echo "15) View Heartbeat Log"

    echo "16) System Snapshot"

    echo "17) Standard Backup"

    echo "18) Encrypted Backup"

    echo "19) Exit"

    echo

    read -r -p "Select option: " choice



    case "$choice" in

      1) cyber_lab_menu ;;

      2) github_menu ;;

      3) operations_menu ;;

      4) research_menu ;;

      5) diagnostics ;;

      6) guided_workflow ;;

      7) career_mode ;;

      8) dashboard_menu ;;

      9) show_today ;;

      10) show_project_status ;;

      11) record_progress ;;

      12) add_assistant_question ;;

      13) view_assistant_inbox ;;

      14) log_heartbeat ;;

      15) view_heartbeat ;;

      16) snapshot ;;

      17) backup_standard ;;

      18) backup_encrypted ;;

      19) clear; echo "Closing Freedom Architect Console..."; sleep 1; exit ;;

      *) echo "Invalid selection."; sleep 1 ;;

    esac

  done

}



ensure_layout

main_menu

