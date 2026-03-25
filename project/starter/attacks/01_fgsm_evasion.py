"""
FGSM (Fast Gradient Sign Method) Evasion Attack

Performs a white-box adversarial attack on the ReceiptCNN by computing
gradient-based perturbations that fool the classifier.

The FGSM formula is: x_adv = x + epsilon * sign(grad_x(loss))

Usage:
    python 01_fgsm_evasion.py
    python 01_fgsm_evasion.py --model-path ../classifier/checkpoints/receipt_cnn_clean.pt
"""
import sys
import os
import json
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "classifier"))

import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from model import ReceiptCNN

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def fgsm_attack(image, epsilon, data_grad):
    """
    Apply FGSM perturbation to an image.

    Args:
        image: Original input image tensor
        epsilon: Perturbation magnitude
        data_grad: Gradient of the loss w.r.t. the input image

    Returns:
        Perturbed image tensor, clamped to valid pixel range [0, 1]
    """
    # TODO: Implement the FGSM perturbation formula
    # 1. Compute the sign of the gradient (data_grad.sign())
    # 2. Create perturbed image: original + epsilon * sign(gradient)
    # 3. Clamp the result to [0, 1] to maintain valid pixel values
    # 4. Return the perturbed image
    pass


def evaluate_fgsm(model_path, test_dir, epsilon):
    """
    Run FGSM attack across the entire test set and return metrics.

    Args:
        model_path: Path to model checkpoint
        test_dir: Path to test dataset directory
        epsilon: FGSM perturbation magnitude

    Returns:
        Dictionary with clean_accuracy, adversarial_accuracy, attack_success_rate
    """
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    dataset = datasets.ImageFolder(test_dir, transform=transform)
    loader = DataLoader(dataset, batch_size=1, shuffle=False)

    model = ReceiptCNN().to(DEVICE)
    model.load_state_dict(torch.load(model_path, map_location=DEVICE, weights_only=True))
    model.eval()

    clean_correct = 0
    adv_correct = 0
    flipped = 0
    total = 0

    for image, label in loader:
        image = image.to(DEVICE)
        label_t = label.float().unsqueeze(1).to(DEVICE)

        # TODO: Implement the FGSM attack loop
        # 1. Enable gradient computation on the input image (image.requires_grad = True)
        # 2. Forward pass: get model output
        # 3. Check if clean prediction is correct
        # 4. Compute BCELoss between output and true label
        # 5. Zero model gradients, then backpropagate to get input gradients
        # 6. Apply fgsm_attack() using the input gradient (image.grad.data)
        # 7. Run the model on the perturbed image (with torch.no_grad())
        # 8. Check if adversarial prediction is correct
        # 9. Track: clean_correct, adv_correct, flipped (correct→incorrect), total
        pass

    return {
        "epsilon": epsilon,
        "clean_accuracy": clean_correct / total if total > 0 else 0,
        "adversarial_accuracy": adv_correct / total if total > 0 else 0,
        "attack_success_rate": flipped / clean_correct if clean_correct > 0 else 0,
        "total_samples": total,
    }


def main():
    parser = argparse.ArgumentParser(description="FGSM Evasion Attack")
    parser.add_argument(
        "--model-path",
        default=os.path.join(os.path.dirname(__file__),
                             "..", "classifier", "checkpoints", "receipt_cnn_clean.pt"),
    )
    parser.add_argument(
        "--test-dir",
        default=os.path.join(os.path.dirname(__file__),
                             "..", "classifier", "balanced_data", "test"),
    )
    parser.add_argument("--output", default="fgsm_results.json")
    args = parser.parse_args()

    epsilons = [0.0, 0.01, 0.03, 0.05, 0.1, 0.15]
    results = []

    print(f"Model: {args.model_path}")
    print(f"Test dir: {args.test_dir}")
    print(f"\n{'Epsilon':>10} {'Clean Acc':>12} {'Adv Acc':>12} {'Attack Rate':>12}")
    print("-" * 50)

    for eps in epsilons:
        r = evaluate_fgsm(args.model_path, args.test_dir, eps)
        results.append(r)
        print(f"{eps:>10.3f} {r['clean_accuracy']:>12.4f} {r['adversarial_accuracy']:>12.4f} {r['attack_success_rate']:>12.4f}")

    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {args.output}")


if __name__ == "__main__":
    main()
