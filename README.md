# 🔬 AI-Powered Code Review Copilot

An intelligent developer assistant that performs automated, repository-level code reviews using a combination of static analysis and AI-based reasoning.

The system analyzes GitHub repositories to detect bugs, security vulnerabilities, performance issues, and maintainability risks, and provides structured, actionable feedback.

---

## 🚀 Key Features

### 🔗 Repository Ingestion
- Accepts GitHub repository URLs
- Automatically clones and processes codebase
- Handles different GitHub URL formats (`/tree/main`, etc.)

### 🧠 Code Understanding (AST-Based)
- Extracts functions, classes, and structure
- Builds internal representation of code

### 🐛 Bug Detection
- Detects logical issues (e.g., bare except, risky patterns)
- Identifies potential runtime failures

### 🔐 Security Analysis
- Hardcoded secrets detection
- Unsafe coding patterns

### ⚡ Performance Analysis
- Nested loops (inefficiency)
- Large file detection
- Potential scalability risks

### 🧹 Code Smell Detection
- Large files
- Maintainability concerns
- Poor coding practices

### 🔗 Correlation Engine
- Identifies repeated patterns across files
- Detects systemic issues
- Highlights hotspots

### 📊 Severity Scoring
- Critical / High / Medium / Low classification
- Overall repository risk score

### 🌐 Language Distribution Analysis
- Detects programming languages used
- Shows percentage distribution across repository

### 🤖 AI (LLM) Review
- Uses Hugging Face models for contextual insights
- Provides intelligent suggestions
- Graceful fallback if LLM unavailable

### 🖥️ Interactive Dashboard (Streamlit)
- Visual analytics
- Issue filtering
- File-level insights
- Correlation visualization

---

## 🏗️ System Architecture

User (Streamlit UI)
↓
Repository Ingestion (GitPython)
↓
Code Parsing (AST)
↓
Static Analysis Engine
↓
LLM Review Engine
↓
Correlation Engine
↓
Severity Scoring Engine
↓
Report Generation


---

## 🧩 Tech Stack

| Component | Technology |
|----------|----------|
| Backend | Python |
| Frontend | Streamlit |
| LLM | Hugging Face Transformers |
| Git Handling | GitPython |
| Visualization | Plotly |
| Data Handling | Pandas |

---

## 📁 Project Structure

ai-code-review-copilot/
│
├── app.py # Streamlit UI
├── pipeline.py # Core pipeline
├── requirements.txt
├── README.md
│
├── config/ # Configurations
├── services/ # Core engines
├── utils/ # Helper functions
├── models/ # Data models


---

## ⚙️ Installation

```bash
git clone https://github.com/<your-username>/ai-code-review-copilot.git
cd ai-code-review-copilot

pip install -r requirements.txt