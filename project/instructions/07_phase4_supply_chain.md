# Phase 4: Supply Chain Analysis

## Background

Supply chain attacks target the software dependencies and deployment infrastructure rather than the AI model itself. A compromised container image or vulnerable dependency can provide an attacker with initial access to the system.

You are given two artifacts to analyze:
- `06_trivy_report.json` — A real Trivy vulnerability scan of the container image
- `Dockerfile` — The container build configuration

You do **not** need to build the Docker image or run Trivy — these are pre-generated artifacts.

## Attack 5: Supply Chain Vulnerability Analysis

### Implementation

Open `attacks/05_supply_chain_analysis.py`. You need to implement:

1. **`parse_trivy_report(path)`**
   - Load the JSON file
   - Navigate the structure: `data["Results"]` → each result has `"Vulnerabilities"`
   - Extract for each vulnerability: ID, severity, package name, installed version, fixed version, title, description, target, target type
   - Return a list of vulnerability dictionaries

2. **`analyze_dockerfile(path)`**
   - Read the Dockerfile content
   - Check for common security issues:
     - **No USER directive** → container runs as root (HIGH)
     - **Unpinned base image** → no SHA256 digest (MEDIUM)
     - **COPY .** → copies entire build context including secrets (MEDIUM)
     - **No HEALTHCHECK** → orchestrators can't detect failures (LOW)
     - **Build tools in production** → build-essential, gcc left in final image (MEDIUM)
     - **Unnecessary tools** → curl, git available for lateral movement (LOW)
   - Return a list of issue dictionaries with: issue, severity, detail, recommendation

3. **`generate_report(vulns, dockerfile_issues)`**
   - Create a structured report with:
     - Summary: total vulnerabilities, severity breakdown
     - Top HIGH severity CVEs
     - Python-specific vulnerabilities
     - Dockerfile issues
     - Overall risk assessment

### Trivy JSON Structure

```json
{
  "Results": [
    {
      "Target": "offensive-ai-course (debian 13.4)",
      "Type": "debian",
      "Vulnerabilities": [
        {
          "VulnerabilityID": "CVE-2024-XXXXX",
          "Severity": "HIGH",
          "PkgName": "package-name",
          "InstalledVersion": "1.2.3",
          "FixedVersion": "1.2.4",
          "Title": "Short description",
          "Description": "Detailed description..."
        }
      ]
    }
  ]
}
```

### Run and Record

```bash
cd attacks
python 05_supply_chain_analysis.py
```

Record findings in `docs/supply_chain_analysis_template.md`. Include:
- Severity breakdown
- Top HIGH findings with remediation
- Dockerfile issues with specific fixes
- AI-specific pipeline risks (model integrity, dependency confusion)
