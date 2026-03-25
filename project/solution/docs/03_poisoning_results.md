# Data Poisoning Results

## Attack Configuration

- **Method:** Label-flip poisoning
- **Flip rate:** 5% of training labels
- **Labels flipped:** 58 out of 1,154 training images
- **Test set:** Unchanged (clean, 195 + 195 images)

## Baseline (Clean Model)

| Metric | Value |
|--------|-------|
| Accuracy | 97.44% |
| Precision | 98.43% |
| Recall | 96.41% |
| F1 Score | 97.41% |
| Confusion Matrix | TN=192 FP=3 / FN=7 TP=188 |

## Poisoned Model

| Metric | Value |
|--------|-------|
| Accuracy | 61.54% |
| Precision | 100.00% |
| Recall | 23.08% |
| F1 Score | 37.50% |
| Confusion Matrix | TN=195 FP=0 / FN=150 TP=45 |

## Impact Analysis

| Metric | Clean | Poisoned | Change |
|--------|-------|----------|--------|
| Accuracy | 97.44% | 61.54% | **-35.90pp** |
| Precision | 98.43% | 100.00% | +1.57pp |
| Recall | 96.41% | 23.08% | **-73.33pp** |
| F1 | 97.41% | 37.50% | **-59.91pp** |

## Key Findings

1. **Dramatic accuracy drop with minimal poisoning:** Only 5% label corruption caused a 36-point accuracy drop — far exceeding the 5-15% drop threshold.

2. **Severe recall degradation:** The poisoned model only detects 23% of receipts (down from 96%). This means 77% of valid receipts would be rejected, causing significant operational impact.

3. **High precision is misleading:** The poisoned model has 100% precision because when it does predict "receipt," it's always correct — but it rarely predicts "receipt" at all. The model is heavily biased toward "non-receipt."

4. **Asymmetric impact:** The poisoning primarily affects the positive class (receipts). The model perfectly classifies non-receipts (195/195) but misses most receipts. This pattern is typical of label-flip poisoning in binary classifiers.

## Implications

A malicious actor with access to 5% of the training pipeline could effectively disable the receipt classifier, causing legitimate receipts to be rejected. This could be used for denial-of-service against the expense system or to create confusion that masks fraudulent activity.
