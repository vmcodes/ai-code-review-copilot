def compute_score(issues):
    weights = {
        "critical": 10,
        "high": 7,
        "medium": 5,
        "low": 2,
        "info": 1
    }

    score = sum(weights[i.severity] for i in issues)
    return min(100, score)

def risk_level(score):
    if score > 75: return "Critical"
    if score > 50: return "High"
    if score > 25: return "Medium"
    return "Low"