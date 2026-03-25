# System Architecture

## Overview

FinanceGuard's AI infrastructure consists of two primary systems with distinct attack surfaces.

## Receipt Classifier

```mermaid
graph LR
    A[Employee uploads image] --> B[Resize to 224x224]
    B --> C[ReceiptCNN]
    C --> D{Score > 0.5?}
    D -->|Yes| E[Receipt - Process expense]
    D -->|No| F[Non-receipt - Reject]

    style C fill:#ff6b6b,stroke:#333

    G[Training Data] --> H[DataLoader]
    H --> I[Train ReceiptCNN]
    I --> J[Checkpoint .pt file]
    J --> C

    style G fill:#ff6b6b,stroke:#333
```

**Attack Surfaces:**
- **Model input (FGSM):** Adversarial perturbations to input images can flip predictions
- **Training data (Poisoning):** Corrupted labels in training data degrade model accuracy

### Model Architecture

```
ReceiptCNN:
  Conv2d(3→16) → BatchNorm → ReLU → MaxPool    # 224→112
  Conv2d(16→32) → BatchNorm → ReLU → MaxPool    # 112→56
  Conv2d(32→64) → BatchNorm → ReLU → MaxPool    # 56→28
  GlobalAvgPool                                   # 28→1
  Dropout(0.3)
  Linear(64→32) → ReLU
  Linear(32→1) → Sigmoid                         # Binary output
```

- **Input:** 224×224 RGB image
- **Output:** Score in [0, 1] — receipt if > 0.5
- **Loss:** BCELoss
- **Parameters:** ~26K (lightweight custom CNN)

## RAG Chatbot

```mermaid
graph TD
    A[Employee question] --> B[Embed query]
    B --> C[FAISS similarity search]
    C --> D[Top-k policy chunks]
    D --> E[System prompt + context + question]
    E --> F[LLM gpt-4o-mini]
    F --> G[Answer]

    H[Policy docs .md] --> I[Chunk text]
    I --> J[Embed chunks]
    J --> K[FAISS Index]
    K --> C

    style K fill:#ff6b6b,stroke:#333
    style E fill:#ff6b6b,stroke:#333
```

**Attack Surfaces:**
- **Vector store (Exfiltration):** FAISS has no access control — any semantically similar query retrieves any document, including confidential ones
- **System prompt (Injection):** The LLM's system prompt can potentially be overridden by crafted user inputs

### RAG Pipeline Flow

1. **Build phase:** Policy documents are chunked (500 chars, 50-char overlap), embedded via `text-embedding-3-small`, and stored in a FAISS IndexFlatL2
2. **Query phase:** User question is embedded → FAISS returns top-3 nearest chunks → chunks are passed as context to `gpt-4o-mini` → LLM generates answer

### Key Vulnerability

The `data/policies/` directory contains 4 documents:
- `expense_policy.md` (public)
- `travel_policy.md` (public)
- `reimbursements_faq.md` (public)
- `executive_bonus_structure_CONFIDENTIAL.md` (restricted)

All 4 are indexed in the same FAISS vector store with **no access control differentiation**. Any query semantically related to compensation will retrieve the confidential document.

## Deployment Infrastructure

```mermaid
graph TD
    A[Dockerfile] --> B[python:3.11-slim base]
    B --> C[Install build-essential, gcc, curl, git]
    C --> D[pip install requirements.txt]
    D --> E[COPY . /app]
    E --> F[Container runs as ROOT]

    style F fill:#ff6b6b,stroke:#333
    style E fill:#ff6b6b,stroke:#333
```

**Attack Surface:** The Dockerfile and container dependencies contain known vulnerabilities (CVEs) and configuration weaknesses that could be exploited.
