import json
import random
from pathlib import Path

# ===================== CONFIG =====================

BASE_PATH = Path(r"C:\Users\semen\AI Secure Coding\dataset\metadata")

REGULAR_RATIOS = (0.8, 0.1, 0.1)
SPECIAL_RATIOS = (0.6, 0.2, 0.2)

SPECIAL_FOLDERS = {"MULTI-CWE", "SAFE-NONCWE"}

random.seed(42)

# ===================== SPLIT LOGIC =====================

def split_list(items, ratios):
    train_r, val_r, test_r = ratios

    items = items[:]  # copy
    random.shuffle(items)

    n = len(items)

    n_train = int(n * train_r)
    n_val = int(n * val_r)
    n_test = int(n * test_r)

    assigned = n_train + n_val + n_test
    remainder = n - assigned

    # distribute remainder → prefer test, then val
    while remainder > 0:
        n_test += 1
        remainder -= 1
        if remainder > 0:
            n_val += 1
            remainder -= 1

    train = items[:n_train]
    val = items[n_train:n_train + n_val]
    test = items[n_train + n_val:]

    return train, val, test


# ===================== LABELING =====================

def label_files(file_paths, split_name):
    for path in file_paths:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        new_data = {}

        for key, value in data.items():
            new_data[key] = value

            if key == "path":
                new_data["split"] = split_name

        with open(path, "w", encoding="utf-8") as f:
            json.dump(new_data, f, indent=2)


# ===================== PROCESSING =====================

def process_regular_folder(lang_dir):
    files = sorted(lang_dir.glob("*.json"))

    if not files:
        return

    n = len(files)
    split_idx = int(n * 0.6)

    vuln = files[:split_idx]
    safe = files[split_idx:]

    train_v, val_v, test_v = split_list(vuln, REGULAR_RATIOS)
    train_s, val_s, test_s = split_list(safe, REGULAR_RATIOS)

    train = train_v + train_s
    val = val_v + val_s
    test = test_v + test_s

    random.shuffle(train)

    label_files(train, "train")
    label_files(val, "val")
    label_files(test, "test")


def process_special_folder(lang_dir):
    files = sorted(lang_dir.glob("*.json"))

    if not files:
        return

    train, val, test = split_list(files, SPECIAL_RATIOS)

    label_files(train, "train")
    label_files(val, "val")
    label_files(test, "test")


def process_dataset(base_path: Path):
    for cwe_dir in base_path.glob("*"):
        if not cwe_dir.is_dir():
            continue

        cwe_name = cwe_dir.name
        print(f"\nProcessing: {cwe_name}")

        for lang_dir in cwe_dir.glob("*"):
            if not lang_dir.is_dir():
                continue

            print(f"  → {lang_dir.name}")

            if cwe_name in SPECIAL_FOLDERS:
                process_special_folder(lang_dir)
            else:
                process_regular_folder(lang_dir)


# ===================== RUN =====================

if __name__ == "__main__":
    process_dataset(BASE_PATH)
    print("\nDone.")