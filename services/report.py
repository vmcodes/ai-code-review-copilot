import json
from collections import Counter

class ReviewReport:
    def __init__(self):
        self.repo_name = ""
        self.repo_url = ""
        self.total_files = 0
        self.total_lines = 0
        self.languages = {}
        self.issues = []
        self.total_issues = 0
        self.severity_counts = {}
        self.category_counts = {}
        self.file_issues = {}
        self.file_scores = {}
        self.hotspot_files = []
        self.clusters = []
        self.dependency_edges = []
        self.systemic_risks = []
        self.overall_score = 0
        self.risk_level = "Low"
        self.duration_seconds = 0


class ReportGenerator:
    def to_json(self, report: ReviewReport):
        return json.dumps(report.__dict__, indent=2, default=str)