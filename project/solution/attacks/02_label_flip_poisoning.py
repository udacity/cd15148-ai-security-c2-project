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
    """Copy dataset and flip flip_ratio of training labels."""
    random.seed(seed)

    # Copy entire dataset first
    if os.path.exists(target_root):
        shutil.rmtree(target_root)
    shutil.copytree(source_root, target_root)

    # Only flip training labels — test stays clean
    flipped = 0
    total = 0

    for cls in ["receipt", "non_receipt"]:
        src_dir = os.path.join(target_root, "train", cls)
        other_cls = "non_receipt" if cls == "receipt" else "receipt"
        dst_dir = os.path.join(target_root, "train", other_cls)

        files = [
            f for f in os.listdir(src_dir)
            if os.path.isfile(os.path.join(src_dir, f))
            and os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS
        ]
        total += len(files)

        n_flip = int(len(files) * flip_ratio)
        to_flip = random.sample(files, n_flip)

        for f in to_flip:
            # Rename to avoid collision with existing files
            new_name = f"flipped_{cls}_{f}"
            shutil.move(
                os.path.join(src_dir, f),
                os.path.join(dst_dir, new_name),
            )
            flipped += 1

    # Report
    print(f"Poisoned dataset created at: {target_root}")
    print(f"Flip ratio: {flip_ratio:.1%}")
    print(f"Total training images: {total}")
    print(f"Labels flipped: {flipped}")
    print(f"Actual flip rate: {flipped / total:.2%}")

    for split in ["train", "test"]:
        for cls in ["receipt", "non_receipt"]:
            d = os.path.join(target_root, split, cls)
            count = len([
                f for f in os.listdir(d)
                if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS
            ])
            print(f"  {split}/{cls}: {count}")


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
