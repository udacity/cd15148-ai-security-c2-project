# AI Security — Offensive AI Red Team Capstone

## Folder Structure

```
project/
├── starter/              # Student-facing starter code
│   ├── classifier/       # CNN architecture + clean checkpoint
│   ├── rag_chatbot/      # Flask app, RAG engine, policy docs
│   ├── attacks/          # TODO stubs for 5 attacks
│   ├── docs/             # Templates, Dockerfile, Trivy report
│   ├── .env.example
│   └── README.md
│
├── solution/             # Reference solution
│   ├── classifier/       # CNN + training pipeline
│   ├── rag_chatbot/      # Complete RAG chatbot
│   ├── attacks/          # Completed attack scripts
│   └── notebooks/        # FGSM and Poisoning walkthroughs
│
├── SUBMISSION/           # Example submission artifacts
│   ├── 00_red_team_charter.md
│   ├── 01_overview.md
│   ├── 02_attack_matrix.md
│   ├── 03_prompt_injection_transcript.md
│   ├── 04_poisoning_results.md
│   ├── 05_executive_risk_summary.md
│   ├── 06_trivy_report.json
│   └── 07_reproduction_steps.md
│
├── instructor/           # Instructor-only files
│   ├── SMOKE_TEST_CHECKLIST.md
│   ├── BLOCKER_REGISTER.md
│   ├── DATASET_MANIFEST.md
│   └── VALIDATION_NOTES.md
│
└── grader/               # Reviewer rubric
    └── Udacity_Reviewer_Rubric.csv
```

## License

[License](../LICENSE.md)