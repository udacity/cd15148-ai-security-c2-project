# Environment Setup

This project can be completed in either the **Udacity workspace** (recommended — GPU + libraries pre-installed) or on your **local machine**. Complete the setup section that matches your environment, then continue with the **Common Steps** that follow.

---

## Setup A: Udacity Workspace

Open the Udacity workspace with GPU support. The starter files are pre-loaded and all required libraries (`torch`, `torchvision`, `flask`, `faiss-cpu`, `openai`, etc.) are already installed — you do not need to run `pip install`.

Skip ahead to **Common Steps**.

---

## Setup B: Local Machine

### B1. Python Version

This project targets **Python 3.12.13** (the version used in the Udacity workspace). Other 3.12.x patch versions will likely work, but pinned dependencies were verified against 3.12.13.

### B2. Create a Virtual Environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate    # macOS/Linux
# .venv\Scripts\activate     # Windows
```

### B3. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs the full pinned set (torch, torchvision, scikit-learn, numpy, Pillow, matplotlib, flask, faiss-cpu, openai, python-dotenv, requests).

> **Note on GPU:** the workspace ships CUDA 12.1 builds of PyTorch (`torch==2.5.1+cu121`). The pinned `torch==2.5.1` will install the appropriate variant for your platform — CPU on macOS/Windows, CUDA on Linux with NVIDIA drivers. The training scripts also auto-detect Apple Silicon GPUs (`mps`), which is much faster than CPU on M-series Macs.

> **macOS quirk:** when running `train.py` locally on macOS, the script may pause for ~30s after printing `Saved checkpoint to ...` before exiting cleanly. This is a known PyTorch DataLoader cleanup issue with multi-worker loading on macOS — the checkpoint is already saved to disk by the time you see that line, so it's safe to Ctrl+C if you want to skip the wait. Doesn't affect Linux or the Udacity workspace.

---

## Common Steps

These apply to both environments.

### Step 1: Configure API Credentials

The RAG chatbot uses OpenAI-compatible APIs via the classroom endpoint.

```bash
cp .env.example rag_chatbot/.env
```

Edit `rag_chatbot/.env` with your classroom API key:

```
OPENAI_API_KEY=your-classroom-api-key
OPENAI_BASE_URL=https://openai.vocareum.com/v1
```

### Step 2: Verify the Pre-trained Model

A clean pre-trained checkpoint and the balanced dataset are provided. Verify the checkpoint loads and evaluates correctly:

```bash
cd classifier
python evaluate.py --model-path checkpoints/receipt_cnn_clean.pt --test-dir balanced_data/test
```

**Expected:** ~94% accuracy on the balanced test set.

### Step 3: Build the RAG Index

```bash
cd ../rag_chatbot
python build_index.py
```

**Expected output:**
```
Total chunks: ~23
FAISS index built: 23 vectors, dim=1536
Index saved to faiss_index/
```

### Step 4: Verify the Chatbot

```bash
python app.py &
curl -X POST http://localhost:5001/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the meal expense limit?"}'
```

**Expected:** The chatbot should respond with "$75 per person per meal" based on the expense policy.

---

## Project Structure

```
starter/
├── classifier/
│   ├── model.py              # ReceiptCNN architecture (given)
│   ├── data.py               # Dataset utilities (given)
│   ├── train.py              # Training script (given)
│   ├── evaluate.py           # Evaluation script (given)
│   ├── predict.py            # Single image prediction (given)
│   ├── balanced_data/        # Pre-resized 256x256 dataset (given)
│   └── checkpoints/
│       └── receipt_cnn_clean.pt  # Pre-trained clean model (given)
├── attacks/
│   ├── 01_fgsm_evasion.py         # YOU IMPLEMENT
│   ├── 02_label_flip_poisoning.py # YOU IMPLEMENT
│   ├── 03_prompt_injection.py     # YOU IMPLEMENT
│   ├── 04_data_exfiltration.py    # YOU IMPLEMENT
│   └── 05_supply_chain_analysis.py # YOU IMPLEMENT
├── rag_chatbot/
│   ├── app.py                # Flask API (given)
│   ├── rag.py                # RAG pipeline (given)
│   ├── build_index.py        # Index builder (given)
│   ├── load_index.py         # Index loader (given)
│   └── data/policies/        # Policy documents (given)
├── docs/                     # Templates for your documentation
├── .env.example              # API key configuration template (given)
├── 06_trivy_report.json      # Real Trivy scan report (given)
└── Dockerfile                # Container configuration (given)
```
