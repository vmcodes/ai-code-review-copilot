"""
helpers.py
Utility functions for file handling, language detection, and snippets
"""

import os
from typing import List, Dict


# ─────────────────────────────────────────────────────────────
# FILE DISCOVERY
# ─────────────────────────────────────────────────────────────
def get_code_files(repo_path: str, extensions: List[str]) -> List[str]:
    code_files = []

    for root, _, files in os.walk(repo_path):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                code_files.append(os.path.join(root, file))

    return code_files


# ─────────────────────────────────────────────────────────────
# LANGUAGE DETECTION
# ─────────────────────────────────────────────────────────────
def detect_language(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1]

    mapping = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".go": "Go",
        ".rb": "Ruby",
    }

    return mapping.get(ext, "Other")


def aggregate_languages(files: List[str]) -> Dict[str, float]:
    """
    Returns percentage distribution of languages
    """
    lang_count = {}

    for file in files:
        lang = detect_language(file)
        lang_count[lang] = lang_count.get(lang, 0) + 1

    total = sum(lang_count.values())

    if total == 0:
        return {}

    lang_percent = {
        lang: round((count / total) * 100, 2)
        for lang, count in lang_count.items()
    }

    return lang_percent