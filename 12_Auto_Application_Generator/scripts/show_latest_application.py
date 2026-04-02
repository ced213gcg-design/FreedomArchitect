#!/usr/bin/env python3
from pathlib import Path

out = Path.home() / "FreedomArchitect/12_Auto_Application_Generator/output"
files = sorted([p for p in out.iterdir() if p.is_file()], key=lambda p: p.stat().st_mtime, reverse=True)

covers = [p for p in files if "_cover.txt" in p.name]
resumes = [p for p in files if "_resume.txt" in p.name]

print("\nLATEST FILES\n")
if covers:
    print("Latest cover :")
    print(covers[0])
    print("\n" + covers[0].read_text(encoding="utf-8", errors="ignore"))
else:
    print("No cover file found.")

print("\n" + "="*60 + "\n")

if resumes:
    print("Latest resume :")
    print(resumes[0])
    print("\n" + resumes[0].read_text(encoding="utf-8", errors="ignore"))
else:
    print("No resume file found.")
