# Dataset Manifest

## Balanced Dataset

| Split | Class | Count | Source |
|-------|-------|-------|--------|
| train | receipt | 577 | SROIE (scanned receipts) + mixed receipt images |
| train | non_receipt | 577 | Google Open Images V7 (CC-BY licensed) |
| test | receipt | 195 | Mixed from both receipt sources (reshuffled) |
| test | non_receipt | 195 | Google Open Images V7 (CC-BY licensed) |

**Total:** 1,544 images

## Receipt Sources

- **SROIE:** Scanned Receipt OCR and Information Extraction dataset. Academic research dataset of real scanned receipts.
- **Mixed receipts:** Additional receipt images from public receipt datasets.

## Non-Receipt Sources

- **Google Open Images V7:** Diverse everyday images (furniture, food, landscapes, animals, objects) downloaded via the fiftyone library. Licensed under CC-BY 4.0.

## Balancing Strategy

The original dataset was heavily imbalanced (1:7.5 receipt:non-receipt ratio). Non-receipts were downsampled to match receipt count per split.

## Train/Test Split

Receipt images from both SROIE and mixed sources are **randomly shuffled** across train/test splits (75/25) to ensure both splits have the same distribution. This prevents distribution mismatch between train and test.
