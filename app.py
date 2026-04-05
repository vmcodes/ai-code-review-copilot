"""
app.py
AI-Powered Code Review Copilot — Streamlit Frontend
"""

import os
import sys
import logging
from typing import Optional

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Ensure repo root path
sys.path.insert(0, os.path.dirname(__file__))

from pipeline import run_pipeline
from services.report import ReviewReport

logging.basicConfig(level=logging.INFO)

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Code Review Copilot",
    page_icon="🔬",
    layout="wide",
)

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
def init_state():
    if "report" not in st.session_state:
        st.session_state.report: Optional[ReviewReport] = None


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.title("🔬 Code Review Copilot")

        repo_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/user/repo"
        )

        analyze = st.button("🚀 Analyze")

        st.markdown("---")
        st.caption("Static + LLM-based analysis")

    return repo_url, analyze


# ─────────────────────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────────────────────
def severity_chart(report):
    labels = list(report.severity_counts.keys())
    values = list(report.severity_counts.values())

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.5
    ))
    return fig


def category_chart(report):
    labels = list(report.category_counts.keys())
    values = list(report.category_counts.values())

    fig = go.Figure(go.Bar(
        x=labels,
        y=values
    ))
    return fig


# ─────────────────────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────────────────────
def dashboard(report):
    st.header("📊 Repository Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Risk Score", f"{report.overall_score}/100")
    col2.metric("Files", report.total_files)
    col3.metric("Lines", report.total_lines)
    col4.metric("Issues", report.total_issues)

    st.markdown("---")

    # Charts
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Severity Distribution")
        st.plotly_chart(severity_chart(report), use_container_width=True)

    with c2:
        st.subheader("Category Distribution")
        st.plotly_chart(category_chart(report), use_container_width=True)

    st.markdown("---")

    # 🔥 LANGUAGE DISTRIBUTION (FIXED)
    if report.languages:
        st.subheader("🌐 Language Distribution (%)")

        lang_df = pd.DataFrame(
            list(report.languages.items()),
            columns=["Language", "Percentage"]
        ).sort_values("Percentage", ascending=False)

        st.dataframe(lang_df, use_container_width=True)

        fig_lang = px.treemap(
            lang_df,
            path=["Language"],
            values="Percentage",
            color="Percentage",
            color_continuous_scale="Blues",
        )

        st.plotly_chart(fig_lang, use_container_width=True)


# ─────────────────────────────────────────────────────────────
# FINDINGS
# ─────────────────────────────────────────────────────────────
def findings(report):
    st.header("🔍 Detailed Findings")

    if not report.issues:
        st.success("No issues found!")
        return

    for issue in report.issues:
        with st.expander(f"{issue['title']} ({issue['severity']})"):
            st.write(f"📄 File: {issue['file_path']}")
            st.write(f"Line: {issue['start_line']}")
            st.write(issue["description"])

            if issue.get("code_snippet"):
                st.code(issue["code_snippet"])

            if issue.get("suggestion"):
                st.success(issue["suggestion"])


# ─────────────────────────────────────────────────────────────
# FILE VIEW
# ─────────────────────────────────────────────────────────────
def file_view(report):
    st.header("📁 File Analysis")

    if not report.file_issues:
        st.info("No file-level issues found.")
        return

    files = list(report.file_issues.keys())

    selected = st.selectbox("Select File", files)

    issues = report.file_issues[selected]

    st.subheader(selected)

    if not issues:
        st.success("No issues in this file.")
        return

    for issue in issues:
        st.write(f"- {issue['title']} ({issue['severity']})")


# ─────────────────────────────────────────────────────────────
# CORRELATION
# ─────────────────────────────────────────────────────────────
def correlation(report):
    st.header("🔗 Correlation & Patterns")

    if report.hotspot_files:
        st.subheader("🔥 Hotspots")
        for f, count in report.hotspot_files[:5]:
            st.write(f"{f} → {count} issues")

    if report.clusters:
        st.subheader("🧩 Issue Clusters")
        for c in report.clusters:
            st.write(f"{c['title']} ({len(c['issue_ids'])} issues)")


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    init_state()

    repo_url, analyze = sidebar()

    # Reset report if new repo URL entered
    if "last_repo" not in st.session_state:
        st.session_state.last_repo = ""

    if repo_url != st.session_state.last_repo:
        st.session_state.report = None
        st.session_state.last_repo = repo_url

    st.title("🔬 AI Code Review Copilot")

    if analyze:
        if not repo_url:
            st.error("Please enter a valid GitHub URL")
        else:
            run(repo_url)

    if st.session_state.report:
        report = st.session_state.report

        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Dashboard",
            "🔍 Findings",
            "🔗 Correlation",
            "📁 Files"
        ])

        with tab1:
            dashboard(report)

        with tab2:
            findings(report)

        with tab3:
            correlation(report)

        with tab4:
            file_view(report)


def run(repo_url):
    progress = st.progress(0)
    status = st.empty()

    def cb(msg, pct):
        progress.progress(min(pct, 100))
        status.write(msg)

    try:
        report = run_pipeline(repo_url, progress_callback=cb)
        st.session_state.report = report
        st.success("Analysis complete!")
    except Exception as e:
        st.error(str(e))


if __name__ == "__main__":
    main()