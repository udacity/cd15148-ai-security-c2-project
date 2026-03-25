# Phase 5: Reporting

## Overview

Red team assessments are only valuable if the findings are clearly communicated. In this phase, you complete the documentation that turns your attack results into actionable intelligence.

## Step 1: Complete the Vulnerability Log

Using `docs/vulnerability_log_template.md`, create a summary table of all 5 vulnerabilities found:

For each vulnerability:
- **ID:** Sequential (VUL-001 through VUL-005)
- **System:** Which system is affected (classifier, chatbot, infrastructure)
- **Vulnerability:** Clear description of the issue
- **Severity:** CRITICAL, HIGH, MEDIUM, or LOW (justify your rating)
- **Evidence:** Reference to the output file or documentation
- **Recommendation:** Specific, actionable fix

## Step 2: Write the Executive Risk Summary

Using `docs/executive_summary_template.md`, write a business-audience summary:

- **Audience:** CISO and executive leadership (non-technical)
- **Tone:** Professional, risk-focused, actionable
- **Structure:**
  1. One-paragraph overview of what was tested and found
  2. Risk dashboard (system, risk level, key finding)
  3. Finding summaries with business impact (not technical details)
  4. Prioritized remediation table (priority, action, effort, impact)
  5. Conclusion with top recommendation

**Tips for writing for executives:**
- Lead with business impact, not technical details
- Use risk levels (CRITICAL/HIGH/MEDIUM/LOW), not CVSS scores
- Frame recommendations by effort and impact
- Highlight the most urgent finding first

## Step 3: Document Reproduction Steps

Using `docs/reproduction_steps_template.md`, document how to reproduce every finding:

- Include exact commands (copy-pasteable)
- Note expected output for each step
- List prerequisites and environment setup
- Include a results summary table

This is critical for:
- Peer review of your findings
- Verification by the security team
- Future regression testing after fixes are applied

## Step 4: Self-Review

Before submitting, verify against the rubric:

1. All 5 attack scripts are implemented and produce output
2. Clean model achieves >85% accuracy
3. FGSM shows clear accuracy degradation across epsilons
4. Poisoning shows measurable accuracy drop
5. Prompt injection has at least 5 diverse attempts with transcript
6. Data exfiltration shows evidence of leaked confidential data
7. Supply chain analysis categorizes vulnerabilities and identifies Dockerfile issues
8. Red Team Charter has scope, objectives, and rules of engagement
9. Executive Summary is written for a business audience
10. All code runs and is reproducible
