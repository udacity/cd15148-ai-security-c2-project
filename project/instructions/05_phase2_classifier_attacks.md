# Phase 2: Classifier Attacks

## Attack 1: FGSM Evasion

### Background

The **Fast Gradient Sign Method (FGSM)** is a white-box adversarial attack introduced by Goodfellow et al. (2014). It exploits the model's gradients to create a small perturbation that maximizes the loss:

```
x_adversarial = x + ε × sign(∇x L(θ, x, y))
```

Where:
- `x` is the original input image
- `ε` (epsilon) controls the perturbation magnitude
- `∇x L` is the gradient of the loss with respect to the input
- `sign()` takes the element-wise sign (+1 or -1)

The key insight: neural networks are linear enough that small changes in the direction of the gradient can significantly change the output.

### Implementation

Open `attacks/01_fgsm_evasion.py`. You need to implement:

1. **`fgsm_attack(image, epsilon, data_grad)`**
   - Compute `sign(data_grad)`
   - Create perturbed image: `image + epsilon * sign(data_grad)`
   - Clamp to [0, 1] to keep valid pixel values
   - Return the perturbed image

2. **The attack loop in `evaluate_fgsm()`**
   - Enable gradient computation on the input: `image.requires_grad = True`
   - Forward pass to get the model's prediction
   - Compute BCELoss between output and true label
   - Backpropagate: `model.zero_grad()` then `loss.backward()`
   - Get input gradients from `image.grad.data`
   - Apply `fgsm_attack()` to create the adversarial image
   - Evaluate the model on the perturbed image

3. **Visualize the attacks for FGSM `visualize_fgsm()`**
   - Use matplotlib to visualize the clean image and then adversarial image
   - Create a title that describes the image and the epsilon used
   - Use the same image for each of the evaluations
   - Note where the image starts to degrade and where a target would start to notice changes in the image 
   - An attacker would like to change the outcome of a classifier without detection
   - Save each image as a PNG called 'fgsm_results_<image_name>_<epsilon>.png'

4. **Expectations**
   - There should be gradual degradation of the accuracy of the model as episolon increases for FGSM

### Run and Record Results

```bash
cd attacks
python 01_fgsm_evasion.py
```

Record the epsilon sweep results in `docs/fgsm_results_template.md`. Include the images and commentary on when FGSM degrades the results of the image.

---

## Attack 2: Label-Flip Data Poisoning

### Background

Data poisoning attacks corrupt the training data to degrade model performance. **Label flipping** is the simplest form: randomly change a small percentage of training labels to the wrong class. Even a 5% flip rate can significantly impact model accuracy.

### Implementation

Open `attacks/02_label_flip_poisoning.py`. You need to implement:

1. **The label flipping logic in `poison_dataset()`**

   The function already copies the clean dataset. You need to add the flipping:
   - For each class folder in training data
   - Calculate how many files to flip: `int(len(files) * flip_ratio)`
   - Randomly select that many files
   - Move them to the opposite class folder (use a prefix to avoid name collisions)

### Run, Retrain, and Compare

```bash
# 1. Create poisoned dataset
python 02_label_flip_poisoning.py

# 2. Retrain on poisoned data
cd ../classifier
python train.py --data-dir poisoned_data --epochs 20 --checkpoint-name receipt_cnn_poisoned.pt

# 3. Evaluate poisoned model on clean test set
python evaluate.py --model-path checkpoints/receipt_cnn_poisoned.pt --test-dir balanced_data/test

# 4. Compare with clean model
python evaluate.py --model-path checkpoints/receipt_cnn_clean.pt --test-dir balanced_data/test
```

Record the before/after metrics in `docs/poisoning_results_template.md`. Pay attention to:
- Overall accuracy change
- Per-class precision and recall
- The confusion matrix pattern
