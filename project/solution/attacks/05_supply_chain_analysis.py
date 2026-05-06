"""
Supply Chain Vulnerability Analysis.

Parses a Trivy JSON report and analyzes a Dockerfile for security issues.
Produces a structured risk assessment of the AI system's deployment pipeline.

Usage:
    python 05_supply_chain_analysis.py
    python 05_supply_chain_analysis.py --trivy-report ../06_trivy_report.json --dockerfile ../Dockerfile
"""
import json
import argparse
import os

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results", "05_supply_chain")


def parse_trivy_report(path):
    """Parse Trivy JSON report and extract vulnerability details."""
    with open(path) as f:
        data = json.load(f)

    vulns = []
    for result in data.get("Results", []):
        target = result.get("Target", "unknown")
        target_type = result.get("Type", "unknown")
        for vuln in result.get("Vulnerabilities", []):
            vulns.append({
                "id": vuln.get("VulnerabilityID", ""),
                "severity": vuln.get("Severity", "UNKNOWN"),
                "package": vuln.get("PkgName", ""),
                "installed_version": vuln.get("InstalledVersion", ""),
                "fixed_version": vuln.get("FixedVersion", ""),
                "title": vuln.get("Title", ""),
                "description": vuln.get("Description", "")[:200],
                "target": target,
                "target_type": target_type,
            })
    return vulns


def analyze_dockerfile(path):
    """Analyze a Dockerfile for common security issues."""
    with open(path) as f:
        content = f.read()
    lines = content.strip().split("\n")

    issues = []

    # Check for running as root (no USER directive)
    has_user = any(line.strip().startswith("USER") for line in lines)
    if not has_user:
        issues.append({
            "issue": "Container runs as root",
            "severity": "HIGH",
            "detail": "No USER directive found. Container processes run as root by default, "
                      "which increases blast radius if the container is compromised.",
            "recommendation": "Add 'USER nonroot' or 'USER 1000' after installing dependencies.",
        })

    # Check for unpinned base image
    from_lines = [l for l in lines if l.strip().startswith("FROM")]
    for from_line in from_lines:
        if "@sha256:" not in from_line:
            issues.append({
                "issue": "Unpinned base image tag",
                "severity": "MEDIUM",
                "detail": f"'{from_line.strip()}' does not use a SHA256 digest pin. "
                          "Tag-based references can change without notice.",
                "recommendation": "Pin the base image with a SHA256 digest: "
                                  "FROM python:3.11-slim@sha256:<digest>",
            })

    # Check for COPY . (copies everything including secrets)
    copy_all = any("COPY . " in line or "COPY ." in line for line in lines)
    if copy_all:
        issues.append({
            "issue": "COPY . copies entire build context",
            "severity": "MEDIUM",
            "detail": "'COPY . /app' copies everything from the build context, "
                      "potentially including .env files, .git directory, and other secrets.",
            "recommendation": "Use a .dockerignore file and copy only needed files, "
                              "or use multi-stage builds.",
        })

    # Check for no HEALTHCHECK
    has_healthcheck = any(line.strip().startswith("HEALTHCHECK") for line in lines)
    if not has_healthcheck:
        issues.append({
            "issue": "No HEALTHCHECK defined",
            "severity": "LOW",
            "detail": "No HEALTHCHECK instruction found. Container orchestrators "
                      "cannot automatically detect if the application is healthy.",
            "recommendation": "Add HEALTHCHECK --interval=30s CMD curl -f http://localhost:5001/health || exit 1",
        })

    # Check for build tools left in final image
    if "build-essential" in content or "gcc" in content:
        if "multi-stage" not in content.lower() and content.count("FROM") == 1:
            issues.append({
                "issue": "Build tools in production image",
                "severity": "MEDIUM",
                "detail": "Build tools (build-essential, gcc) are installed but not removed "
                          "in the final image. This increases attack surface and image size.",
                "recommendation": "Use a multi-stage build: compile in a builder stage, "
                                  "copy only artifacts to a clean runtime stage.",
            })

    # Check for curl/git in production image
    if "curl" in content or "git" in content:
        issues.append({
            "issue": "Unnecessary tools in production image",
            "severity": "LOW",
            "detail": "curl and/or git are installed in the final image but are "
                      "unlikely to be needed at runtime. They could be used by an "
                      "attacker for lateral movement.",
            "recommendation": "Remove curl and git, or install them only in a build stage.",
        })

    return issues


def generate_report(vulns, dockerfile_issues):
    """Generate a structured supply chain risk report."""
    # Severity counts
    severity_counts = {}
    for v in vulns:
        sev = v["severity"]
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    # Top HIGH findings
    high_vulns = [v for v in vulns if v["severity"] == "HIGH"]
    high_vulns.sort(key=lambda v: v["id"])

    # Python-specific vulns
    python_vulns = [v for v in vulns if v["target_type"] == "python-pkg"]

    report = {
        "summary": {
            "total_vulnerabilities": len(vulns),
            "severity_breakdown": severity_counts,
            "dockerfile_issues": len(dockerfile_issues),
        },
        "high_severity_vulnerabilities": [
            {
                "id": v["id"],
                "package": v["package"],
                "installed": v["installed_version"],
                "fixed": v["fixed_version"],
                "title": v["title"],
            }
            for v in high_vulns[:15]
        ],
        "python_specific": [
            {
                "id": v["id"],
                "package": v["package"],
                "severity": v["severity"],
                "title": v["title"],
            }
            for v in python_vulns
        ],
        "dockerfile_issues": dockerfile_issues,
        "risk_assessment": {
            "overall_risk": "HIGH" if severity_counts.get("CRITICAL", 0) > 0
                           or severity_counts.get("HIGH", 0) > 10
                           else "MEDIUM",
            "key_concerns": [
                f"{severity_counts.get('HIGH', 0)} HIGH severity vulnerabilities in container dependencies",
                f"{len(python_vulns)} vulnerabilities in Python packages",
                f"{len(dockerfile_issues)} Dockerfile configuration issues",
            ],
        },
    }
    return report


def main():
    parser = argparse.ArgumentParser(description="Supply Chain Vulnerability Analysis")
    parser.add_argument(
        "--trivy-report",
        default=os.path.join(os.path.dirname(__file__), "..", "06_trivy_report.json"),
    )
    parser.add_argument(
        "--dockerfile",
        default=os.path.join(os.path.dirname(__file__), "..", "Dockerfile"),
    )
    parser.add_argument(
        "--output",
        default=os.path.join(RESULTS_DIR, "supply_chain_report.json"),
    )
    args = parser.parse_args()
    if not os.path.dirname(args.output):
        args.output = os.path.join(RESULTS_DIR, args.output)
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    print("Parsing Trivy report...")
    vulns = parse_trivy_report(args.trivy_report)

    print("Analyzing Dockerfile...")
    dockerfile_issues = analyze_dockerfile(args.dockerfile)

    report = generate_report(vulns, dockerfile_issues)

    # Print summary
    print(f"\n{'=' * 50}")
    print("  SUPPLY CHAIN RISK ASSESSMENT")
    print(f"{'=' * 50}")
    s = report["summary"]
    print(f"\n  Total vulnerabilities: {s['total_vulnerabilities']}")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        count = s["severity_breakdown"].get(sev, 0)
        if count:
            print(f"    {sev}: {count}")

    print(f"\n  Top HIGH severity findings:")
    for v in report["high_severity_vulnerabilities"][:5]:
        print(f"    {v['id']}: {v['package']} {v['installed']} → {v['fixed'] or 'no fix'}")
        print(f"      {v['title'][:80]}")

    if report["python_specific"]:
        print(f"\n  Python-specific vulnerabilities:")
        for v in report["python_specific"]:
            print(f"    [{v['severity']}] {v['id']}: {v['package']}")

    print(f"\n  Dockerfile issues ({len(dockerfile_issues)}):")
    for issue in dockerfile_issues:
        print(f"    [{issue['severity']}] {issue['issue']}")

    print(f"\n  Overall risk: {report['risk_assessment']['overall_risk']}")
    print(f"{'=' * 50}")

    with open(args.output, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nFull report saved to {args.output}")


if __name__ == "__main__":
    main()
