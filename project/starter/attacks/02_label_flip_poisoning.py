"""
Label-Flip Data Poisoning Attack

Copies the balanced dataset and flips a percentage of training labels
(moves images between receipt/non_receipt folders) to degrade model accuracy.

Usage:
    python 02_label_flip_poisoning.py
    python 02_label_flip_poisoning.py --flip-rate 0.10
"""
import os
import shutil
import random
import argparse

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}


def poison_dataset(source_root, target_root, flip_ratio=0.05, seed=42):
    """
    Copy dataset and flip a percentage of training labels.

    Label flipping works by moving images between class folders:
    - A receipt image moved to non_receipt/ gets a flipped label
    - A non_receipt image moved to receipt/ gets a flipped label

    Only training labels are flipped — the test set stays clean so we can
    measure the true impact of poisoning on model performance.

    Args:
        source_root: Path to clean balanced dataset
        target_root: Path for poisoned dataset output
        flip_ratio: Fraction of training labels to flip (default 0.05 = 5%)
        seed: Random seed for reproducibility
    """
    random.seed(seed)

    # Step 1: Copy the entire clean dataset to target
    if os.path.exists(target_root):
        shutil.rmtree(target_root)
    shutil.copytree(source_root, target_root)

    # TODO: Implement the label flipping logic
    #
    # Only flip TRAINING labels — the test set must stay clean so we can
    # measure the true impact of poisoning on model performance.
    #
    # Steps:
    # 1. For each class in training data ("receipt" and "non_receipt"):
    #    a. List all image files in the class folder (filter by IMAGE_EXTENSIONS)
    #    b. Calculate how many to flip: n_flip = int(len(files) * flip_ratio)
    #    c. Randomly sample n_flip files using random.sample()
    #    d. Move each selected file to the OPPOSITE class folder using shutil.move()
    #       (add a "flipped_" prefix to avoid filename collisions)
    #    e. Track total flipped count
    #
    # 2. Print a summary showing:
    #    - Total training images, number flipped, actual flip rate
    #    - Image counts per class per split (train/test x receipt/non_receipt)
    #
    # Hint: The opposite class of "receipt" is "non_receipt" and vice versa.
    #        Use os.path.join(target_root, "train", class_name) to build paths.
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Label-Flip Poisoning Attack")
    parser.add_argument(
        "--source",
        default=os.path.join(os.path.dirname(__file__),
                             "..", "classifier", "balanced_data"),
    )
    parser.add_argument(
        "--target",
        default=os.path.join(os.path.dirname(__file__),
                             "..", "classifier", "poisoned_data"),
    )
    parser.add_argument("--flip-rate", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    poison_dataset(args.source, args.target, args.flip_rate, args.seed)
