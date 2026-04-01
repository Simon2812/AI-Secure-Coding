from bisect import insort
from collections import Counter


def normalize_tag(tag):
    cleaned = []
    previous_dash = False

    for ch in tag.strip().lower():
        if ch.isalnum():
            cleaned.append(ch)
            previous_dash = False
        elif ch in (" ", "_", "-") and not previous_dash:
            cleaned.append("-")
            previous_dash = True

    while cleaned and cleaned[-1] == "-":
        cleaned.pop()

    while cleaned and cleaned[0] == "-":
        cleaned.pop(0)

    return "".join(cleaned)


def tokenize_title(title):
    word = []
    result = []

    for ch in title.lower():
        if ch.isalpha():
            word.append(ch)
        else:
            if len(word) >= 3:
                result.append("".join(word))
            word.clear()

    if len(word) >= 3:
        result.append("".join(word))

    return result


def compact_preview(text, limit):
    if len(text) <= limit:
        return text

    cut = text[:limit].rstrip()
    last_space = cut.rfind(" ")
    if last_space >= 20:
        cut = cut[:last_space]

    return cut + "..."


def estimate_reading_minutes(text):
    words = [part for part in text.split() if part]
    count = len(words)
    if count == 0:
        return 0
    return max(1, (count + 179) // 180)


class NoteIndex:
    def __init__(self):
        self._notes = {}
        self._clusters = {}
        self._tag_popularity = Counter()
        self._cluster_order = []

    def add_note(self, note_id, title, body, tags, created_on, pinned=False):
        normalized_tags = tuple(
            tag for tag in (normalize_tag(item) for item in tags) if tag
        )

        keywords = tuple(self._extract_keywords(title, body))
        cluster_key = self._choose_cluster(normalized_tags, keywords)

        self._notes[note_id] = {
            "title": title.strip(),
            "body": body.strip(),
            "tags": normalized_tags,
            "created_on": created_on,
            "pinned": bool(pinned),
            "keywords": keywords,
            "cluster": cluster_key,
            "reading_minutes": estimate_reading_minutes(body),
        }

        if cluster_key not in self._clusters:
            self._clusters[cluster_key] = {
                "notes": [],
                "tags": Counter(),
                "keywords": Counter(),
                "pinned_count": 0,
            }
            insort(self._cluster_order, cluster_key)

        self._clusters[cluster_key]["notes"].append(note_id)
        self._clusters[cluster_key]["keywords"].update(keywords)
        self._clusters[cluster_key]["tags"].update(normalized_tags)

        if pinned:
            self._clusters[cluster_key]["pinned_count"] += 1

        self._tag_popularity.update(normalized_tags)

    def cluster_cards(self):
        cards = []

        for cluster_key in self._cluster_order:
            bucket = self._clusters[cluster_key]
            note_ids = bucket["notes"]
            note_ids.sort(key=self._sort_key_for_note)

            total_minutes = 0
            previews = []
            oldest = None
            newest = None

            for note_id in note_ids:
                note = self._notes[note_id]
                total_minutes += note["reading_minutes"]

                preview = compact_preview(note["body"], 72)
                previews.append((note["title"], preview))

                created_on = note["created_on"]
                if oldest is None or created_on < oldest:
                    oldest = created_on
                if newest is None or created_on > newest:
                    newest = created_on

            cards.append(
                {
                    "cluster": cluster_key,
                    "note_count": len(note_ids),
                    "pinned_count": bucket["pinned_count"],
                    "top_tags": self._top_items(bucket["tags"], 4),
                    "top_keywords": self._top_items(bucket["keywords"], 5),
                    "estimated_reading_minutes": total_minutes,
                    "date_span": (oldest, newest),
                    "previews": previews[:3],
                }
            )

        cards.sort(
            key=lambda item: (
                -item["pinned_count"],
                -item["note_count"],
                item["cluster"],
            )
        )
        return cards

    def top_tags(self, limit=10):
        return self._top_items(self._tag_popularity, limit)

    def notes_for_tag(self, tag):
        normalized = normalize_tag(tag)
        matched = []

        for note_id, note in self._notes.items():
            if normalized in note["tags"]:
                matched.append(
                    (
                        note_id,
                        note["title"],
                        note["created_on"],
                        note["reading_minutes"],
                    )
                )

        matched.sort(key=lambda item: (item[2], item[1]), reverse=True)
        return matched

    def weekly_activity(self):
        activity = {}

        for note in self._notes.values():
            year, week, _ = note["created_on"].isocalendar()
            key = f"{year}-W{week:02d}"

            bucket = activity.setdefault(
                key,
                {
                    "notes": 0,
                    "pinned": 0,
                    "minutes": 0,
                },
            )

            bucket["notes"] += 1
            bucket["minutes"] += note["reading_minutes"]
            if note["pinned"]:
                bucket["pinned"] += 1

        return dict(sorted(activity.items()))

    def search_titles(self, phrase):
        terms = [word for word in tokenize_title(phrase) if word]
        if not terms:
            return []

        scored = []

        for note_id, note in self._notes.items():
            title_terms = tokenize_title(note["title"])
            overlap = sum(1 for term in terms if term in title_terms)
            if overlap:
                scored.append(
                    (
                        overlap,
                        note["pinned"],
                        note["created_on"],
                        note_id,
                        note["title"],
                    )
                )

        scored.sort(reverse=True)
        return [(item[3], item[4]) for item in scored]

    def _sort_key_for_note(self, note_id):
        note = self._notes[note_id]
        return (
            not note["pinned"],
            -note["created_on"].toordinal(),
            note["title"].lower(),
        )

    def _extract_keywords(self, title, body):
        terms = Counter()
        for token in tokenize_title(title):
            terms[token] += 3

        for token in tokenize_title(body):
            if len(token) >= 4:
                terms[token] += 1

        ignored = {
            "this", "that", "with", "from", "into", "about", "have", "were",
            "them", "then", "when", "where", "need", "note", "notes", "todo",
            "very", "more", "than", "after", "before", "because", "while",
        }

        ranked = []
        for token, weight in terms.items():
            if token not in ignored:
                ranked.append((weight, token))

        ranked.sort(reverse=True)
        return [token for _, token in ranked[:8]]

    def _choose_cluster(self, tags, keywords):
        if tags:
            return tags[0]

        if keywords:
            return "kw:" + keywords[0]

        return "uncategorized"

    def _top_items(self, counter, limit):
        pairs = list(counter.items())
        pairs.sort(key=lambda item: (-item[1], item[0]))
        return [name for name, _ in pairs[:limit]]