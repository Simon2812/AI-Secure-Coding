import json
import random
from pathlib import Path

BASE_PATH = Path(r"C:\Users\semen\AI-Secure-Coding\dataset\metadata")

REGULAR_RATIOS = (0.8, 0.1, 0.1)
SPECIAL_RATIOS = (0.6, 0.2, 0.2)

SPECIAL_FOLDERS = {"MULTI-CWE", "SAFE-NONCWE"}

random.seed(42)


# ===================== SPLIT =====================

def split_list(items, ratios):
    train_r, val_r, test_r = ratios

    items = items[:]
    random.shuffle(items)

    n = len(items)

    n_train = int(n * train_r)
    n_val = int(n * val_r)
    n_test = int(n * test_r)

    remainder = n - (n_train + n_val + n_test)

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


# ===================== LABEL =====================

def label_files(file_paths, split_name):
    for path in file_paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    print(f"[SKIP EMPTY] {path}")
                    continue
                data = json.loads(content)
        except Exception as e:
            print(f"[SKIP INVALID] {path} → {e}")
            continue

        new_data = {}

        for key, value in data.items():
            new_data[key] = value
            if key == "path":
                new_data["split"] = split_name

        with open(path, "w", encoding="utf-8") as f:
            json.dump(new_data, f, indent=2)


# ===================== HELPERS =====================

def folder_already_processed(files):
    """
    Check first valid JSON for 'split'
    """
    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return "split" in data
        except:
            continue
    return False


def process_files(files, ratios, use_vuln_split):
    if not files:
        return

    if folder_already_processed(files):
        print("    [SKIP] already has split")
        return

    if use_vuln_split:
        n = len(files)
        split_idx = int(n * 0.6)

        vuln = files[:split_idx]
        safe = files[split_idx:]

        train_v, val_v, test_v = split_list(vuln, ratios)
        train_s, val_s, test_s = split_list(safe, ratios)

        train = train_v + train_s
        val = val_v + val_s
        test = test_v + test_s

        random.shuffle(train)

    else:
        train, val, test = split_list(files, ratios)

    label_files(train, "train")
    label_files(val, "val")
    label_files(test, "test")


# ===================== MAIN =====================

def process_dataset(base_path: Path):
    for cwe_dir in base_path.glob("*"):
        if not cwe_dir.is_dir():
            continue

        cwe_name = cwe_dir.name
        print(f"\nProcessing: {cwe_name}")

        # detect if folder has json directly OR lang subfolders
        json_files = sorted(cwe_dir.glob("*.json"))

        if json_files:
            # no language level
            print("  → direct JSON files")

            if cwe_name in SPECIAL_FOLDERS:
                process_files(json_files, SPECIAL_RATIOS, use_vuln_split=False)
            else:
                process_files(json_files, REGULAR_RATIOS, use_vuln_split=True)

        else:
            # has language subfolders
            for lang_dir in cwe_dir.glob("*"):
                if not lang_dir.is_dir():
                    continue

                print(f"  → {lang_dir.name}")

                files = sorted(lang_dir.glob("*.json"))

                if cwe_name in SPECIAL_FOLDERS:
                    process_files(files, SPECIAL_RATIOS, use_vuln_split=False)
                else:
                    process_files(files, REGULAR_RATIOS, use_vuln_split=True)


# ===================== RUN =====================

if __name__ == "__main__":
    process_dataset(BASE_PATH)
    print("\nDone.")
