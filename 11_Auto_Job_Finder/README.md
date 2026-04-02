# Auto Job Finder + Scoring Engine

## Purpose
Find cybersecurity-aligned job opportunities from selected source pages, score them, and write ranked outputs for execution.

## What It Does
- reads source URLs from data/sources.txt
- reads keywords and scoring logic from data/criteria.json
- fetches source pages
- extracts likely jobs
- scores them
- writes ranked CSV + Markdown reports

## Run
python3 scripts/find_and_score_jobs.py

## Output
- output/jobs_ranked.csv
- output/jobs_ranked.md

## Rule
No job lead should exist without scoring and capture.
