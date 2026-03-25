# Environment Setup

## Step 1: Open Your Workspace

Open the Udacity workspace with GPU support. The starter files are pre-loaded in your workspace.

## Step 2: Install Dependencies

```bash
pip install torch torchvision scikit-learn numpy Pillow
pip install flask faiss-cpu openai python-dotenv requests
```

## Step 3: Configure API Credentials

The RAG chatbot uses OpenAI-compatible APIs via the classroom endpoint.

```bash
# Copy the example env file
cp .env.example rag_chatbot/.env
```

Edit `rag_chatbot/.env` with your classroom API key:

```
OPENAI_API_KEY=your-classroom-api-key
OPENAI_BASE_URL=https://openai.vocareum.com/v1
```

## Step 4: Prepare the Dataset

The raw receipt dataset needs to be balanced before training:

```bash
cd classifier
python data.py --source /path/to/raw/data --target balanced_data
```

This downsamples the majority class to create a balanced 1:1 dataset.

**Expected output:**
```
[train] receipt: 577 images
[train] non_receipt: 577 images
[test] receipt: ~200 images
[test] non_receipt: ~200 images
```

## Step 5: Verify the Pre-trained Model

A clean pre-trained checkpoint is provided. Verify it loads and evaluates correctly:

```bash
python evaluate.py --model-path checkpoints/receipt_cnn_clean.pt --test-dir balanced_data/test
```

**Expected:** >95% accuracy on the balanced test set.

## Step 6: Build the RAG Index

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

## Step 7: Verify the Chatbot

```bash
python app.py &
curl -X POST http://localhost:5001/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the meal expense limit?"}'
```

**Expected:** The chatbot should respond with "$75 per person per meal" based on the expense policy.

## Project Structure

```
starter/
├── classifier/
│   ├── model.py              # ReceiptCNN architecture (given)
│   ├── data.py               # Dataset utilities (given)
│   ├── train.py              # Training script (given)
│   ├── evaluate.py           # Evaluation script (given)
│   ├── predict.py            # Single image prediction (given)
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
