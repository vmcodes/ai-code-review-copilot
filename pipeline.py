import os
import time
from collections import Counter

from services.ingestion import clone_repo
from services.analyzer import detect_issues
from services.llm import llm_review
from services.correlation import find_hotspots, find_clusters
from services.scoring import compute_score, risk_level
from services.report import ReviewReport

from utils.helpers import get_code_files, aggregate_languages


def run_pipeline(repo_url, progress_callback=None):
    start = time.time()

    report = ReviewReport()
    report.repo_url = repo_url

    if progress_callback:
        progress_callback("Cloning repository...", 10)

    repo_path = clone_repo(repo_url)

    # ─────────────────────────────────────────────
    # MULTI-LANGUAGE FILE COLLECTION
    # ─────────────────────────────────────────────
    all_files = get_code_files(
        repo_path,
        extensions=[".py", ".js", ".ts", ".java", ".cpp", ".c"]
    )

    report.total_files = len(all_files)

    # 🔥 LANGUAGE PERCENTAGE (NEW FEATURE)
    report.languages = aggregate_languages(all_files)

    # Only analyze Python files for now
    py_files = [f for f in all_files if f.endswith(".py")]

    all_issues = []

    for idx, file in enumerate(py_files):
        if progress_callback:
            progress_callback(
                f"Analyzing {file}",
                20 + int(idx / max(len(py_files), 1) * 50)
            )

        try:
            with open(file, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception:
            continue

        report.total_lines += len(code.split("\n"))

        issues = detect_issues(code, file)

        # LLM review (safe fallback inside function)
        try:
            llm_review(code)
        except:
            pass

        report.file_issues[file] = [i.__dict__ for i in issues]
        report.file_scores[file] = len(issues) * 5

        all_issues.extend(issues)

    report.issues = [i.__dict__ for i in all_issues]
    report.total_issues = len(all_issues)

    # ─────────────────────────────────────────────
    # COUNTS
    # ─────────────────────────────────────────────
    report.severity_counts = Counter([i.severity for i in all_issues])
    report.category_counts = Counter([i.category for i in all_issues])

    # ─────────────────────────────────────────────
    # CORRELATION
    # ─────────────────────────────────────────────
    report.hotspot_files = find_hotspots(all_issues)
    report.clusters = find_clusters(all_issues)

    # ─────────────────────────────────────────────
    # SCORING
    # ─────────────────────────────────────────────
    score = compute_score(all_issues)
    report.overall_score = score
    report.risk_level = risk_level(score)

    report.duration_seconds = round(time.time() - start, 2)

    return report