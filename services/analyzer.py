import re
from models.issue import Issue
import uuid

def detect_issues(code, file_path):
    issues = []

    lines = code.split("\n")

    # 🔐 Security
    for i, line in enumerate(lines):
        if "password" in line.lower() or "api_key" in line.lower():
            issues.append(Issue(
                issue_id=str(uuid.uuid4()),
                severity="critical",
                category="security",
                title="Hardcoded Secret",
                description="Sensitive data exposed in code",
                file_path=file_path,
                start_line=i+1,
                end_line=i+1,
                code_snippet=line,
                suggestion="Use environment variables"
            ))

    # 🐛 Bugs
    for i, line in enumerate(lines):
        if "except:" in line:
            issues.append(Issue(
                issue_id=str(uuid.uuid4()),
                severity="high",
                category="bug",
                title="Bare Except",
                description="Catching all exceptions hides errors",
                file_path=file_path,
                start_line=i+1,
                end_line=i+1,
                code_snippet=line,
                suggestion="Specify exception type"
            ))

    # ⚡ Performance
    if "for" in code and "for" in code:
        issues.append(Issue(
            issue_id=str(uuid.uuid4()),
            severity="medium",
            category="performance",
            title="Nested Loops",
            description="Potential O(n^2) complexity",
            file_path=file_path,
            start_line=1,
            end_line=10,
            suggestion="Optimize loops or use vectorization"
        ))

    # 🧹 Code Smell
    if len(lines) > 300:
        issues.append(Issue(
            issue_id=str(uuid.uuid4()),
            severity="low",
            category="code_smell",
            title="Large File",
            description="File too long, hard to maintain",
            file_path=file_path,
            start_line=1,
            end_line=len(lines),
            suggestion="Split into modules"
        ))

    return issues