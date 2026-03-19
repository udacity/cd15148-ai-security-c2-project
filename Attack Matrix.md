## Attack Matrix

| # | Attack Type                     | Target                        | Technique                      | Student Evidence |
|---|--------------------------------|-------------------------------|--------------------------------|------------------|
| 1 | White-box evasion              | CNN model                     | FGSM attack                    | Adversarial examples + accuracy drop |
| 2 | Black-box evasion              | CNN model                     | Transferability attack         | Successful misclassification |
| 3 | Data poisoning                | Training dataset              | Label flipping                 | Poisoned dataset + retraining results |
| 4 | Model extraction (optional)   | Model API / predictions       | Query-based extraction         | Reconstructed behavior |
| 5 | Supply chain vulnerability    | Docker image / dependencies   | Trivy container scan           | Analysis of `06_trivy_report.json` + Dockerfile review |