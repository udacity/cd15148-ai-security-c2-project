# Red Team Charter — FinanceGuard AI Security Assessment

## Engagement Details

| Field | Value |
|-------|-------|
| **Engagement Name** | FinanceGuard AI System Security Assessment |
| **Date** | March 2026 |
| **Assessor** | Junior AI Red Team Operator |
| **Sponsor** | CISO, FinanceGuard Inc. |

## Objectives

Evaluate the security posture of FinanceGuard's AI-powered financial systems by executing controlled adversarial attacks across five vectors:

1. **FGSM Evasion Attack** — Test the Receipt Classifier CNN's robustness against gradient-based adversarial perturbations
2. **Data Poisoning** — Assess the impact of training data manipulation on model accuracy
3. **Prompt Injection** — Test the RAG chatbot's resistance to instruction override and role manipulation
4. **Data Exfiltration** — Evaluate whether confidential documents are accessible through the RAG pipeline
5. **Supply Chain Analysis** — Identify vulnerabilities in the container image and deployment dependencies

## Scope

### In Scope
- Receipt Classifier CNN (ReceiptCNN model, training pipeline, inference)
- Expense Policy RAG Chatbot (FAISS vector store, LLM integration, Flask API)
- Deployment infrastructure (Dockerfile, container dependencies via Trivy report)

### Out of Scope
- Production network infrastructure
- Employee credentials and authentication systems
- Third-party vendor systems
- Physical security

## Rules of Engagement

1. All testing is performed in an isolated development environment
2. No attacks against production systems or live user data
3. Adversarial images and poisoned datasets remain within the test environment
4. RAG chatbot testing uses controlled API endpoints only
5. All findings are documented and reported through proper channels
6. No modifications to production model checkpoints

## Success Criteria

| Attack Vector | Success Metric |
|---------------|---------------|
| FGSM Evasion | Demonstrate >20% accuracy degradation at ε ≤ 0.1 |
| Data Poisoning | Achieve ≥5% accuracy drop with ≤5% label flip rate |
| Prompt Injection | Successfully bypass system prompt restrictions in ≥1 technique |
| Data Exfiltration | Retrieve confidential document contents via RAG queries |
| Supply Chain | Identify all HIGH severity CVEs and Dockerfile misconfigurations |

## Deliverables

1. This Red Team Charter
2. Vulnerability Log with severity ratings
3. Attack result documentation for each vector
4. Executive Risk Summary
5. Reproduction steps for all findings
