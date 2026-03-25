# Project Overview: AI System Compromise & Resilience Assessment

## Scenario

You are a **Junior AI Red Team Operator** at FinanceGuard Inc., a financial technology company. FinanceGuard has deployed two AI-powered systems:

1. **Receipt Classifier (CNN)** — A convolutional neural network that classifies uploaded images as valid receipts or non-receipts for automated expense processing.

2. **Expense Policy RAG Chatbot** — An LLM-powered assistant connected to a FAISS vector database containing company expense and travel policies. Employees use it to ask questions about reimbursement procedures.

Your CISO has authorized a red team engagement to evaluate the security posture of these AI systems before they go into wider production deployment.

## The Challenge

Execute **5 adversarial attacks** across the AI systems and infrastructure:

| # | Attack | Target | Objective |
|---|--------|--------|-----------|
| 1 | FGSM Evasion | Receipt Classifier | Craft adversarial images that fool the classifier |
| 2 | Label-Flip Poisoning | Training Pipeline | Corrupt training data to degrade model accuracy |
| 3 | Prompt Injection | RAG Chatbot | Override system instructions to manipulate behavior |
| 4 | Data Exfiltration | RAG Vector Store | Extract confidential documents through the chatbot |
| 5 | Supply Chain Analysis | Docker/Dependencies | Identify vulnerabilities in the deployment pipeline |

## Learning Objectives

By completing this project, you will:

- Implement a white-box adversarial attack (FGSM) against a neural network
- Execute a data poisoning attack and measure its impact on model performance
- Craft prompt injection techniques against a RAG-based LLM system
- Demonstrate data exfiltration vulnerabilities in vector store architectures
- Analyze supply chain risks using Trivy vulnerability reports and Dockerfile review
- Document findings in a professional red team report format

## What You Build vs. What's Given

**You implement** (the attack scripts in `attacks/`):
- `01_fgsm_evasion.py` — FGSM attack implementation
- `02_label_flip_poisoning.py` — Data poisoning logic
- `03_prompt_injection.py` — Injection prompt design and execution
- `04_data_exfiltration.py` — Exfiltration query design and analysis
- `05_supply_chain_analysis.py` — Trivy report parsing and Dockerfile analysis

**Given to you** (infrastructure — do not modify):
- Receipt Classifier: `model.py`, `train.py`, `evaluate.py`, `predict.py`, `data.py`, pre-trained checkpoint
- RAG Chatbot: `app.py`, `rag.py`, `build_index.py`, `load_index.py`, policy documents
- Trivy report (`06_trivy_report.json`) and `Dockerfile`

**You write** (documentation in `docs/`):
- Red Team Charter
- Vulnerability Log
- Attack results for each vector
- Executive Risk Summary
- Reproduction Steps

## Deliverables

1. **5 completed attack scripts** in `attacks/`
2. **9 documentation files** in `docs/` (use the provided templates)
3. **Attack output files** (JSON results from running your scripts)
