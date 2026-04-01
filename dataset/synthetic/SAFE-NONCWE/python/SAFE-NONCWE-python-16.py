import sys


class BlockParser:
    def __init__(self):
        self._entries = []
        self._current = None

    def feed_line(self, line):
        line = line.rstrip()

        if not line:
            self._commit()
            return

        if line.startswith("#"):
            self._commit()
            self._current = {"title": line[1:].strip(), "fields": {}}
            return

        if ":" in line and self._current is not None:
            key, value = line.split(":", 1)
            self._current["fields"][key.strip().lower()] = value.strip()
        else:
            if self._current is None:
                return
            self._current.setdefault("body", []).append(line.strip())

    def finalize(self):
        self._commit()
        return tuple(self._entries)

    def _commit(self):
        if self._current:
            if "body" in self._current:
                self._current["body"] = " ".join(self._current["body"])
            else:
                self._current["body"] = ""
            self._entries.append(self._current)
        self._current = None


class EntryAnalyzer:
    def __init__(self, entries):
        self._entries = entries

    def stats(self):
        total = len(self._entries)
        by_type = {}
        longest = None

        for entry in self._entries:
            t = entry["fields"].get("type", "unknown")
            by_type[t] = by_type.get(t, 0) + 1

            length = len(entry["body"])
            if longest is None or length > longest[1]:
                longest = (entry["title"], length)

        return {
            "total": total,
            "by_type": by_type,
            "longest_entry": longest,
        }

    def filter_by_tag(self, tag):
        tag = tag.lower()
        result = []

        for entry in self._entries:
            tags = entry["fields"].get("tags", "")
            parts = [t.strip().lower() for t in tags.split(",") if t.strip()]

            if tag in parts:
                result.append(entry)

        return result

    def group_by_field(self, field):
        groups = {}

        for entry in self._entries:
            value = entry["fields"].get(field, "unknown")
            groups.setdefault(value, []).append(entry["title"])

        return groups


def render_summary(stats):
    lines = []
    lines.append(f"Total entries: {stats['total']}")

    lines.append("By type:")
    for key, value in sorted(stats["by_type"].items()):
        lines.append(f"  {key}: {value}")

    if stats["longest_entry"]:
        title, length = stats["longest_entry"]
        lines.append(f"Longest entry: {title} ({length} chars)")

    return "\n".join(lines)


def render_entries(entries):
    lines = []

    for entry in entries:
        lines.append(f"# {entry['title']}")
        for k, v in entry["fields"].items():
            lines.append(f"{k}: {v}")
        if entry["body"]:
            lines.append(entry["body"])
        lines.append("")

    return "\n".join(lines).rstrip()


def main():
    parser = BlockParser()

    for line in sys.stdin:
        parser.feed_line(line)

    entries = parser.finalize()
    analyzer = EntryAnalyzer(entries)

    stats = analyzer.stats()
    print(render_summary(stats))

    if len(sys.argv) > 1:
        tag = sys.argv[1]
        filtered = analyzer.filter_by_tag(tag)

        print("\nFiltered entries:\n")
        print(render_entries(filtered))


if __name__ == "__main__":
    main()