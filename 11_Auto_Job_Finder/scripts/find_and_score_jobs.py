#!/usr/bin/env python3
from pathlib import Path
import json
import re
import csv
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from html import unescape

BASE = Path.home() / "FreedomArchitect" / "11_Auto_Job_Finder"
DATA = BASE / "data"
OUT = BASE / "output"

def load_sources():
    src = (DATA / "sources.txt").read_text(encoding="utf-8").splitlines()
    return [s.strip() for s in src if s.strip() and not s.strip().startswith("#")]

def load_criteria():
    return json.loads((DATA / "criteria.json").read_text(encoding="utf-8"))

def fetch(url: str) -> str:
    req = Request(url, headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome Safari"
    })
    with urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", errors="ignore")

def clean(text: str) -> str:
    text = unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def extract_candidates(html: str, source_url: str):
    # Generic candidate extraction from anchor tags
    links = re.findall(r'<a[^>]+href=["\\\']([^"\\\']+)["\\\'][^>]*>(.*?)</a>', html, flags=re.I|re.S)
    candidates = []
    for href, inner in links:
        title = clean(inner)
        if len(title) < 8 or len(title) > 140:
            continue
        low = title.lower()
        if not any(k in low for k in ["security", "cyber", "soc", "network", "incident", "threat", "analyst"]):
            continue
        if href.startswith("/"):
            # preserve relative links by attaching domain root
            m = re.match(r"(https?://[^/]+)", source_url)
            if m:
                href = m.group(1) + href
        candidates.append({
            "title": title,
            "company": "Unknown",
            "location": "Unknown",
            "link": href,
            "source": source_url
        })
    # de-duplicate by title+link
    seen = set()
    deduped = []
    for c in candidates:
        key = (c["title"], c["link"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(c)
    return deduped[:50]

def score_job(job, criteria):
    title_blob = " ".join([
        job.get("title",""),
        job.get("company",""),
        job.get("location",""),
        job.get("source","")
    ]).lower()

    w = criteria["weights"]
    score = 0
    matched = []

    for kw in criteria["target_keywords"]:
        if kw.lower() in title_blob:
            score += w["target_keyword"]
            matched.append(f"+kw:{kw}")

    for loc in criteria["preferred_locations"]:
        if loc.lower() in title_blob:
            score += w["preferred_location"]
            matched.append(f"+loc:{loc}")

    if "remote" in title_blob:
        score += w["remote_bonus"]
        matched.append("+remote")

    for ek in criteria["entry_keywords"]:
        if ek.lower() in title_blob:
            score += w["entry_bonus"]
            matched.append(f"+entry:{ek}")
            break

    for nk in criteria["negative_keywords"]:
        if nk.lower() in title_blob:
            score += w["negative_penalty"]
            matched.append(f"-neg:{nk}")

    return score, ", ".join(matched)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sources = load_sources()
    criteria = load_criteria()

    all_jobs = []
    for src in sources:
        try:
            html = fetch(src)
            candidates = extract_candidates(html, src)
            all_jobs.extend(candidates)
        except (URLError, HTTPError, TimeoutError, Exception) as e:
            all_jobs.append({
                "title": f"[SOURCE ERROR] {src}",
                "company": "N/A",
                "location": "N/A",
                "link": src,
                "source": src,
                "score": -999,
                "matched": f"error:{type(e).__name__}"
            })

    ranked = []
    for job in all_jobs:
        if "score" not in job:
            score, matched = score_job(job, criteria)
            job["score"] = score
            job["matched"] = matched
        ranked.append(job)

    ranked.sort(key=lambda x: x["score"], reverse=True)

    csv_path = OUT / "jobs_ranked.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["score", "title", "company", "location", "link", "source", "matched"]
        )
        writer.writeheader()
        writer.writerows(ranked)

    md_path = OUT / "jobs_ranked.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Ranked Job Results\n\n")
        f.write("| Score | Title | Company | Location | Match Notes |\n")
        f.write("|------:|-------|---------|----------|-------------|\n")
        for r in ranked[:50]:
            title = r["title"].replace("|", "/")
            company = r["company"].replace("|", "/")
            location = r["location"].replace("|", "/")
            matched = r["matched"].replace("|", "/")
            f.write(f"| {r['score']} | [{title}]({r['link']}) | {company} | {location} | {matched} |\n")

    print(f"Created: {csv_path}")
    print(f"Created: {md_path}")
    print(f"Ranked jobs: {len(ranked)}")

if __name__ == "__main__":
    main()
