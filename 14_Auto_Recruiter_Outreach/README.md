# Auto Recruiter Outreach Engine

## Purpose
Generate recruiter outreach messages, log outreach activity, and keep execution aligned with the application system.

## What It Does
- reads recruiter/contact input
- generates a recruiter message
- generates a follow-up message
- stores outputs
- logs the outreach event
- updates mission and executive tracking

## Run
python3 scripts/generate_outreach.py

## Output
- output/<company>_<role>_recruiter_message.txt
- output/<company>_<role>_followup_message.txt

## Rule
No recruiter contact should happen without logging and follow-up readiness.
