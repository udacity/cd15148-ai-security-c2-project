# Supply Chain Vulnerability Analysis

## Scope

- **Trivy report:** `06_trivy_report.json` — Trivy v0.69.3 scan of `offensive-ai-course` container image
- **Dockerfile:** `Dockerfile` — python:3.11-slim based image

## Vulnerability Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH | 34 |
| MEDIUM | 160 |
| LOW | 601 |
| UNKNOWN | 9 |
| **Total** | **804** |

## High Severity Findings

### OS-Level (linux-libc-dev / kernel)

Most HIGH severity findings are in `linux-libc-dev 6.12.74-2` (kernel headers), including:

| CVE | Description |
|-----|------------|
| CVE-2013-7445 | Memory exhaustion via crafted GEM objects |
| CVE-2021-3847 | Low-privileged user privilege escalation |
| CVE-2021-3864 | Descendant's dumpable setting SUID bypass |
| CVE-2024-26599 | Null pointer dereference in GPIO driver |

These kernel CVEs have no fixes available and are carried by the Debian base image.

### Python-Specific

| CVE | Package | Severity |
|-----|---------|----------|
| CVE-2026-23949 | jaraco.context | HIGH |
| CVE-2026-24049 | wheel | HIGH |

These directly affect the Python supply chain and should be updated immediately.

## Dockerfile Issues

### 1. Container Runs as Root — HIGH

No `USER` directive found. All processes run as root, increasing the blast radius of any container escape or code execution vulnerability.

**Fix:** Add `RUN useradd -r appuser && USER appuser` after dependency installation.

### 2. Unpinned Base Image — MEDIUM

`FROM python:3.11-slim` uses a tag without a SHA256 digest pin. Tags are mutable — the same tag can point to different images over time, introducing supply chain risk.

**Fix:** Pin with digest: `FROM python:3.11-slim@sha256:<digest>`

### 3. COPY . Copies Entire Context — MEDIUM

`COPY . /app` includes everything: `.env` files, `.git` directory, test data, potentially credentials.

**Fix:** Use `.dockerignore` and copy only required files.

### 4. Build Tools in Production — MEDIUM

`build-essential` and `gcc` are installed but remain in the final image, increasing attack surface by ~200MB.

**Fix:** Use multi-stage build — compile in a builder stage, copy only runtime artifacts.

### 5. Unnecessary Tools — LOW

`curl` and `git` are installed but not needed at runtime. An attacker could use these for lateral movement.

### 6. No HEALTHCHECK — LOW

No HEALTHCHECK instruction means container orchestrators cannot detect application failures.

## AI Pipeline Risk Assessment

The supply chain poses specific risks to the AI system:

1. **Model integrity:** `COPY . /app` copies model checkpoints into the container. If the build context is compromised, malicious model weights could be injected.

2. **Dependency confusion:** Python packages are installed via `pip install -r requirements.txt` without hash verification. A typosquatting or dependency confusion attack could inject malicious packages.

3. **Runtime privilege:** Running as root means a successful prompt injection or code execution attack against the Flask chatbot would have full container access.

## Remediation Priority

| Priority | Action |
|----------|--------|
| 1 | Add USER directive (runs as non-root) |
| 2 | Pin base image with SHA256 digest |
| 3 | Use multi-stage build |
| 4 | Add .dockerignore |
| 5 | Update Python packages (jaraco.context, wheel) |
| 6 | Add pip --require-hashes |
| 7 | Add HEALTHCHECK |
