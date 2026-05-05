from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def generate_report(raw_results: list, defended_results: list, output_path="report.html"):
    combined = []
    for r, d in zip(raw_results, defended_results):
        combined.append({
            "id": r["id"],
            "name": r["name"],
            "owasp": r["owasp"],
            "raw_outcome": r["outcome"],
            "def_outcome": d["outcome"],
        })

    raw_success = sum(1 for r in raw_results if r["outcome"] == "success")
    def_fail = sum(1 for d in defended_results if d["outcome"] == "fail")
    total = len(raw_results)
    improvement = round((def_fail / total) * 100) if total else 0

    env = Environment(loader=FileSystemLoader("templates"))
    tmpl = env.get_template("report.html")
    html = tmpl.render(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
        results=combined,
        raw_success=raw_success,
        def_blocked=def_fail,
        total=total,
        improvement=improvement,
    )
    with open(output_path, "w") as f:
        f.write(html)
    print(f"Report saved → {output_path}")
