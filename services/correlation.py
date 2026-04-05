from collections import Counter

def find_hotspots(issues):
    file_counts = Counter([i.file_path for i in issues])
    return file_counts.most_common()

def find_clusters(issues):
    clusters = []
    grouped = {}

    for i in issues:
        key = i.category
        grouped.setdefault(key, []).append(i)

    for k, v in grouped.items():
        if len(v) > 2:
            clusters.append({
                "cluster_id": k.upper(),
                "title": f"Repeated {k} issues",
                "severity": v[0].severity,
                "pattern_type": k,
                "description": f"{len(v)} similar issues found",
                "affected_files": list(set([i.file_path for i in v])),
                "issue_ids": [i.issue_id for i in v]
            })
    return clusters