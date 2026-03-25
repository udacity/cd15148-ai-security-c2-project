# Smoke Test Checklist

Run through this checklist to verify the starter and solution are working before publishing.

## Starter Verification

- [ ] `starter/classifier/model.py` contains ReceiptCNN with custom architecture (not pretrained)
- [ ] `starter/classifier/checkpoints/receipt_cnn_clean.pt` loads into ReceiptCNN successfully (~1MB)
- [ ] `starter/classifier/data.py`, `train.py`, `evaluate.py`, `predict.py` are complete (no TODOs)
- [ ] `starter/attacks/01_fgsm_evasion.py` has TODO comments for `fgsm_attack()` and the attack loop
- [ ] `starter/attacks/02_label_flip_poisoning.py` has TODO for the label flipping logic
- [ ] `starter/attacks/03_prompt_injection.py` has empty `INJECTION_PROMPTS` list with TODO
- [ ] `starter/attacks/04_data_exfiltration.py` has empty `EXFILTRATION_QUERIES` list with TODO
- [ ] `starter/attacks/05_supply_chain_analysis.py` has TODOs in `parse_trivy_report()` and `analyze_dockerfile()`
- [ ] `starter/rag_chatbot/app.py`, `rag.py`, `build_index.py`, `load_index.py` are complete
- [ ] All 4 policy documents present in `starter/rag_chatbot/data/policies/`
- [ ] `starter/06_trivy_report.json` contains ~804 vulnerabilities
- [ ] `starter/Dockerfile` is the real Dockerfile
- [ ] All 9 doc templates present in `starter/docs/`
- [ ] No `.env` files with real API keys in starter
- [ ] `.env.example` present

## Solution Verification

- [ ] `python data.py --source <raw_data> --target balanced_data` creates balanced dataset
- [ ] `python train.py --data-dir balanced_data --epochs 20` trains successfully, loss decreases
- [ ] `python evaluate.py` shows >95% accuracy on balanced test
- [ ] `python attacks/02_label_flip_poisoning.py` creates poisoned_data/
- [ ] `python train.py --data-dir poisoned_data --epochs 20 --checkpoint-name receipt_cnn_poisoned.pt` completes
- [ ] Poisoned model accuracy drops ≥5pp (actual: ~36pp drop)
- [ ] `python attacks/01_fgsm_evasion.py` shows accuracy degradation across epsilons
- [ ] `python build_index.py` creates faiss_index/ without errors
- [ ] `python app.py` starts Flask server
- [ ] Legitimate query returns correct policy answer
- [ ] `python attacks/03_prompt_injection.py` records transcript, some injections succeed
- [ ] `python attacks/04_data_exfiltration.py` retrieves confidential data
- [ ] `python attacks/05_supply_chain_analysis.py` parses all vulns and finds Dockerfile issues
- [ ] All 9 solution docs populated with real results

## Files That Should NOT Be in Starter

- [ ] No `checkpoints/receipt_cnn_poisoned.pt`
- [ ] No `balanced_data/` or `poisoned_data/` directories
- [ ] No `faiss_index/` directory
- [ ] No `.env` with real keys
- [ ] No `__pycache__/`, `.DS_Store`, or `venv/`
- [ ] No completed solution docs
