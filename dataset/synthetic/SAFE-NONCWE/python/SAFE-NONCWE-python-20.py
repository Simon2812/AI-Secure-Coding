import sys


class DiffEngine:
    def __init__(self, left_lines, right_lines):
        self.left = left_lines
        self.right = right_lines
        self._dp = None

    def compute(self):
        n = len(self.left)
        m = len(self.right)

        dp = [[0] * (m + 1) for _ in range(n + 1)]

        for i in range(n - 1, -1, -1):
            for j in range(m - 1, -1, -1):
                if self.left[i] == self.right[j]:
                    dp[i][j] = 1 + dp[i + 1][j + 1]
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])

        self._dp = dp

    def build_diff(self):
        if self._dp is None:
            self.compute()

        i = 0
        j = 0
        n = len(self.left)
        m = len(self.right)

        result = []

        while i < n and j < m:
            if self.left[i] == self.right[j]:
                result.append(("=", self.left[i]))
                i += 1
                j += 1
            elif self._dp[i + 1][j] >= self._dp[i][j + 1]:
                result.append(("-", self.left[i]))
                i += 1
            else:
                result.append(("+", self.right[j]))
                j += 1

        while i < n:
            result.append(("-", self.left[i]))
            i += 1

        while j < m:
            result.append(("+", self.right[j]))
            j += 1

        return result


def normalize_lines(text):
    return [line.rstrip() for line in text.splitlines()]


def collapse_changes(diff):
    blocks = []
    current = None

    for op, line in diff:
        if current is None or current[0] != op:
            if current:
                blocks.append(current)
            current = [op, [line]]
        else:
            current[1].append(line)

    if current:
        blocks.append(current)

    return blocks


def compute_similarity(diff):
    equal = sum(1 for op, _ in diff if op == "=")
    total = len(diff)

    if total == 0:
        return 1.0

    return round(equal / total, 3)


def detect_moved_blocks(diff):
    removed = []
    added = []

    for op, line in diff:
        if op == "-":
            removed.append(line)
        elif op == "+":
            added.append(line)

    moved = set(removed) & set(added)
    return tuple(sorted(moved))


def format_unified(diff):
    output = []

    for op, line in diff:
        if op == "=":
            output.append(" " + line)
        elif op == "-":
            output.append("-" + line)
        elif op == "+":
            output.append("+" + line)

    return "\n".join(output)


def read_input():
    left = []
    right = []

    target = left

    for line in sys.stdin:
        if line.strip() == "---":
            target = right
            continue
        target.append(line.rstrip("\n"))

    return left, right


def main():
    left, right = read_input()

    engine = DiffEngine(left, right)
    diff = engine.build_diff()

    blocks = collapse_changes(diff)
    similarity = compute_similarity(diff)
    moved = detect_moved_blocks(diff)

    print("Similarity:", similarity)
    print("\nChanges:\n")
    print(format_unified(diff))

    if moved:
        print("\nPotential moved lines:")
        for line in moved:
            print(" *", line)


if __name__ == "__main__":
    main()