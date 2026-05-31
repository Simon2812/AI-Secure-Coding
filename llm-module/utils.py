from collections import defaultdict

def metric_dict():
    """
    Create empty metric structure.
    """
    return {
        "final": [],
        "cwe": [],
        "fix": [],
    }


def print_group_stats(title, stats_dict):
    """
    Print averaged metrics per group (CWE, language, etc.).
    """

    print(f"\n{title}")

    for key in sorted(stats_dict):
        data = stats_dict[key]

        # Safety against empty lists
        if len(data["final"]) == 0:
            continue

        final_avg = sum(data["final"]) / len(data["final"])
        cwe_avg = sum(data["cwe"]) / len(data["cwe"])
        fix_avg = sum(data["fix"]) / len(data["fix"])

        print(
            f"{key} | "
            f"Final: {final_avg:.4f} | "
            f"CWE: {cwe_avg:.4f} | "
            f"Fix: {fix_avg:.4f}"
        )
