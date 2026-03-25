"""
FGSM (Fast Gradient Sign Method) Evasion Attack

Performs a white-box adversarial attack on the ReceiptCNN by computing
gradient-based perturbations that fool the classifier.

Usage:
    python 01_fgsm_evasion.py
    python 01_fgsm_evasion.py --model-path ../classifier/checkpoints/receipt_cnn_poisoned.pt
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
    """Apply FGSM perturbation: x_adv = x + epsilon * sign(grad)"""
    sign_data_grad = data_grad.sign()
    perturbed_image = image + epsilon * sign_data_grad
    return torch.clamp(perturbed_image, 0, 1)


def evaluate_fgsm(model_path, test_dir, epsilon):
    """Run FGSM attack across entire test set and return metrics."""
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
        image.requires_grad = True

        output = model(image)
        clean_pred = (output > 0.5).float()
        clean_is_correct = clean_pred.item() == label_t.item()
        if clean_is_correct:
            clean_correct += 1

        loss = torch.nn.BCELoss()(output, label_t)
        model.zero_grad()
        loss.backward()

        perturbed_image = fgsm_attack(image, epsilon, image.grad.data)

        with torch.no_grad():
            adv_output = model(perturbed_image)
        adv_pred = (adv_output > 0.5).float()
        adv_is_correct = adv_pred.item() == label_t.item()
        if adv_is_correct:
            adv_correct += 1
        if clean_is_correct and not adv_is_correct:
            flipped += 1

        total += 1

    return {
        "epsilon": epsilon,
        "clean_accuracy": clean_correct / total,
        "adversarial_accuracy": adv_correct / total,
        "attack_success_rate": flipped / clean_correct if clean_correct > 0 else 0.0,
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
