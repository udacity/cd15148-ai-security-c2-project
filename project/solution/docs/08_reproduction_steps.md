# Reproduction Steps

## Prerequisites

- Python 3.11+
- pip or uv package manager
- ~2GB disk space for dataset and dependencies

## Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install torch torchvision scikit-learn numpy Pillow
pip install flask faiss-cpu openai python-dotenv requests

# Configure API credentials
cp solution/.env.example solution/rag_chatbot/.env
# Edit .env with your Vocareum API key
```

## Step 1: Prepare Dataset

```bash
cd solution/classifier
python data.py --source /path/to/raw/receipt/data --target balanced_data
# Expected: 577 train receipts, 577 train non-receipts, ~200 test each
```

## Step 2: Train Clean Model

```bash
python train.py --data-dir balanced_data --epochs 20
# Expected: Loss decreases, checkpoint saved to checkpoints/receipt_cnn_clean.pt
```

## Step 3: Evaluate Clean Model

```bash
python evaluate.py --model-path checkpoints/receipt_cnn_clean.pt --test-dir balanced_data/test
# Expected: >95% accuracy, >95% recall
```

## Step 4: Run FGSM Attack

```bash
cd ../attacks
python 01_fgsm_evasion.py
# Expected: Accuracy drops from ~97% to ~19% at epsilon=0.1
# Output: results/01_fgsm/fgsm_results.json
```

## Step 5: Run Data Poisoning

```bash
python 02_label_flip_poisoning.py
# Expected: Creates poisoned_data/ with 5% flipped labels

cd ../classifier
python train.py --data-dir poisoned_data --epochs 20 --checkpoint-name receipt_cnn_poisoned.pt
python evaluate.py --model-path checkpoints/receipt_cnn_poisoned.pt --test-dir balanced_data/test
# Expected: Accuracy drops to ~62%, recall drops to ~23%
```

## Step 6: Build RAG Chatbot Index

```bash
cd ../rag_chatbot
python build_index.py
# Expected: 23 chunks embedded, FAISS index saved to faiss_index/
```

## Step 7: Start Chatbot

```bash
python app.py
# Expected: Flask server running on port 5001
# Test: curl http://localhost:5001/health
```

## Step 8: Run Prompt Injection Attack

```bash
# In a new terminal
cd solution/attacks
python 03_prompt_injection.py
# Expected: 2/5 injection attempts succeed
# Output: results/03_prompt_injection/prompt_injection_results.json
```

## Step 9: Run Data Exfiltration Attack

```bash
python 04_data_exfiltration.py
# Expected: 6/6 queries exfiltrate confidential data
# Output: results/04_exfiltration/data_exfiltration_results.json
```

## Step 10: Run Supply Chain Analysis

```bash
python 05_supply_chain_analysis.py
# Expected: 804 vulnerabilities parsed, 6 Dockerfile issues found
# Output: results/05_supply_chain/supply_chain_report.json
```

## Expected Results Summary

| Attack | Metric | Expected Result |
|--------|--------|----------------|
| FGSM (ε=0.1) | Adversarial accuracy | ~19% (from 97%) |
| Poisoning (5%) | Clean test accuracy | ~62% (from 97%) |
| Prompt injection | Success rate | ≥2/5 techniques |
| Data exfiltration | Success rate | 6/6 queries |
| Supply chain | HIGH CVEs | 34 |
