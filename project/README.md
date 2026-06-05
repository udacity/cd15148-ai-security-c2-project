# AI System Compromise & Resilience Assessment (Finance Edition)

A capstone project for offensive AI security. Students act as Junior AI Red Team Operators executing 5 adversarial attacks against a financial AI system.

## Project Structure

```
project/
├── instructions/          # Step-by-step project instructions (9 pages)
├── starter/               # Student starting files
│   ├── classifier/        # Receipt CNN (given — model, train, evaluate)
│   ├── attacks/           # Attack script scaffolds (students implement)
│   ├── rag_chatbot/       # Expense chatbot (given — app, rag, index)
│   ├── docs/              # Documentation templates
│   ├── .env.example       # API key configuration template
│   ├── 06_trivy_report.json  # Real Trivy scan report
│   └── Dockerfile         # Container configuration
├── solution/              # Complete reference solution
│   ├── classifier/        # Trained models + balanced dataset
│   ├── attacks/           # Completed attack scripts
│   ├── rag_chatbot/       # Working chatbot with policies
│   ├── requirements.txt   # All Python dependencies
│   └── docs/              # Completed documentation
├── docs/                  # Instructor-facing materials
└── .gitignore
```

## 5 Attacks

1. **FGSM Evasion** — White-box adversarial perturbation against the receipt classifier
2. **Label-Flip Poisoning** — Training data corruption (5% flip rate)
3. **Prompt Injection** — System prompt override against the RAG chatbot
4. **Data Exfiltration** — Retrieving confidential documents from the vector store
5. **Supply Chain Analysis** — Trivy vulnerability report + Dockerfile review

## Quick Start (Solution)

```bash
cd solution/classifier
python data.py --source /path/to/data --target balanced_data
python train.py --data-dir balanced_data --epochs 20
python evaluate.py

cd ../rag_chatbot
python build_index.py
python app.py &

cd ../attacks
python 01_fgsm_evasion.py
python 02_label_flip_poisoning.py
python 03_prompt_injection.py
python 04_data_exfiltration.py
python 05_supply_chain_analysis.py
```
