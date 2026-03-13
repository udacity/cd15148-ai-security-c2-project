# Attack Matrix

| Attack | Target | Evidence | Outcome |
|---|---|---|---|
| FGSM | CNN classifier | accuracy drop | success |
| Poisoning | CNN training data | degraded post-training accuracy | success |
| Prompt injection | Chatbot | transcript | success |
| Data exfiltration | RAG corpus | confidential retrieval attempt | risk shown |
| Supply chain | Container image | Trivy JSON | vulnerabilities found |