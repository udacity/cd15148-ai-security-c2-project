"""
Evaluate a trained ReceiptCNN checkpoint.

Prints accuracy, precision, recall, F1, and confusion matrix.

Usage:
    python evaluate.py                                              # Evaluate clean model
    python evaluate.py --model-path checkpoints/receipt_cnn_poisoned.pt  # Evaluate poisoned model
"""
import argparse
import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from model import ReceiptCNN
from data import get_transform

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def evaluate_model(model_path, test_dir):
    transform = get_transform()
    dataset = datasets.ImageFolder(test_dir, transform=transform)
    loader = DataLoader(dataset, batch_size=32, shuffle=False)

    model = ReceiptCNN().to(DEVICE)
    model.load_state_dict(torch.load(model_path, map_location=DEVICE, weights_only=True))
    model.eval()

    y_true = []
    y_pred = []

    with torch.no_grad():
        for images, labels in loader:
            images = images.to(DEVICE)
            outputs = model(images)
            preds = (outputs > 0.5).int().squeeze(1).cpu().numpy()
            y_pred.extend(preds.tolist())
            y_true.extend(labels.numpy().tolist())

    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
    }
    return metrics


def print_metrics(metrics, label="Model"):
    print(f"\n{'=' * 40}")
    print(f"  {label}")
    print(f"{'=' * 40}")
    print(f"  Accuracy:  {metrics['accuracy']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  Recall:    {metrics['recall']:.4f}")
    print(f"  F1 Score:  {metrics['f1']:.4f}")
    print(f"  Confusion Matrix:")
    cm = metrics["confusion_matrix"]
    print(f"    [[{cm[0][0]:4d}, {cm[0][1]:4d}]")
    print(f"     [{cm[1][0]:4d}, {cm[1][1]:4d}]]")
    print(f"{'=' * 40}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate ReceiptCNN")
    parser.add_argument(
        "--model-path", default="checkpoints/receipt_cnn_clean.pt",
        help="Path to model checkpoint"
    )
    parser.add_argument(
        "--test-dir", default="balanced_data/test",
        help="Path to test dataset directory"
    )
    args = parser.parse_args()

    metrics = evaluate_model(args.model_path, args.test_dir)
    print_metrics(metrics, label=args.model_path)
