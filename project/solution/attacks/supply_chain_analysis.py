import json, sys

def summarize(report_path):
    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)
    vulns = []
    for result in report.get("Results", []):
        for v in result.get("Vulnerabilities", []) or []:
            vulns.append((v["VulnerabilityID"], v["Severity"], v.get("PkgName", "")))
    return vulns

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "trivy_report.json"
    for vuln in summarize(path):
        print(vuln)