import json
from datetime import datetime

def to_json(adrs, path="adr-registry.json"):
    data = {
        "generated_at": datetime.utcnow().isoformat(),
        "adrs": [a.__dict__ for a in adrs],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    return data

def to_index_markdown(adrs):
    lines = ["# Architecture Decision Records", "",
             f"Всего решений: {len(adrs)}", "",
             "| ID | Title | Status | Date |",
             "|----|-------|--------|------|"]
    for a in adrs:
        lines.append(f"| {a.id} | {a.title} | {a.status.value} | {a.date} |")
    return "\n".join(lines)

def to_html(adrs):
    html = ["<html><body><h1>ADR Registry</h1><ul>"]
    for a in adrs:
        html.append(f"<li><b>{a.id}</b> — {a.title} [{a.status.value}]</li>")
    html.append("</ul></body></html>")
    return "\n".join(html)
