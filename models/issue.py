from dataclasses import dataclass

@dataclass
class Issue:
    issue_id: str
    severity: str
    category: str
    title: str
    description: str
    file_path: str
    start_line: int
    end_line: int
    code_snippet: str = ""
    suggestion: str = ""
    element_name: str = ""