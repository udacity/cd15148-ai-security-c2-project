# FGSM Evasion Attack Results

## Clean Model Baseline

- **Model:** ReceiptCNN (3 conv layers with BatchNorm, GAP, 26K parameters)
- **Test accuracy:** 97.44%
- **Precision:** 98.43% | **Recall:** 96.41% | **F1:** 97.41%

## FGSM Results (Clean Model)

| Epsilon | Clean Accuracy | Adversarial Accuracy | Attack Success Rate |
|---------|---------------|---------------------|-------------------|
| 0.000 | 97.44% | 97.44% | 0.00% |
| 0.010 | 97.44% | 88.72% | 8.95% |
| 0.030 | 97.44% | 64.62% | 33.68% |
| 0.050 | 97.44% | 41.79% | 57.11% |
| 0.100 | 97.44% | 19.23% | 80.26% |
| 0.150 | 97.44% | 16.67% | 82.89% |

*Attack Success Rate = fraction of correctly classified samples flipped by FGSM perturbation*

## Analysis

1. **Significant vulnerability to adversarial perturbations:** Even a small epsilon of 0.01 causes ~9% of correctly classified images to be misclassified.

2. **Steep degradation curve:** Accuracy drops below 50% by ε=0.05, meaning perturbations invisible to the human eye can fool the classifier more than half the time.

3. **Near-complete evasion at ε=0.1:** The model retains only 19.2% accuracy, with over 80% of previously correct predictions flipped by the attack.

4. **Plateau effect:** Beyond ε=0.1, additional perturbation yields diminishing returns — the model is already near-random performance.

## Implications

The receipt classifier has no built-in robustness to adversarial inputs. An attacker could submit a slightly modified non-receipt image that the model confidently classifies as a valid receipt, potentially enabling expense fraud. The perturbations at ε=0.01–0.03 would be visually imperceptible to a human reviewer.
