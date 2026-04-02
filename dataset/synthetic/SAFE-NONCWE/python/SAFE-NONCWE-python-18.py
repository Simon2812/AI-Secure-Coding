import re
from collections import defaultdict


class Rule:
    def __init__(self, name, condition, action, weight=1):
        self.name = name
        self.condition = condition
        self.action = action
        self.weight = weight

    def matches(self, item):
        return self.condition(item)


class ModerationContext:
    def __init__(self):
        self.flags = defaultdict(int)
        self.labels = set()
        self.score = 0
        self.actions = []

    def apply(self, action, weight):
        if action == "flag":
            self.flags["generic"] += 1
        elif action.startswith("label:"):
            self.labels.add(action.split(":", 1)[1])
        elif action == "boost":
            self.score += weight
        elif action == "penalize":
            self.score -= weight
        elif action.startswith("flag:"):
            self.flags[action.split(":", 1)[1]] += 1

        self.actions.append(action)


class RuleEngine:
    def __init__(self):
        self._rules = []

    def register(self, rule):
        self._rules.append(rule)

    def evaluate(self, item):
        ctx = ModerationContext()

        for rule in self._rules:
            if rule.matches(item):
                ctx.apply(rule.action, rule.weight)

        return ctx


def keyword_condition(words):
    words = tuple(w.lower() for w in words)

    def check(item):
        text = item.get("text", "").lower()
        return any(w in text for w in words)

    return check


def regex_condition(pattern):
    compiled = re.compile(pattern, re.IGNORECASE)

    def check(item):
        return bool(compiled.search(item.get("text", "")))

    return check


def length_condition(min_len=None, max_len=None):
    def check(item):
        length = len(item.get("text", ""))
        if min_len is not None and length < min_len:
            return False
        if max_len is not None and length > max_len:
            return False
        return True

    return check


def repetition_condition():
    def check(item):
        text = item.get("text", "")
        words = text.split()
        counts = defaultdict(int)

        for w in words:
            counts[w] += 1

        return any(v > 5 for v in counts.values())

    return check


def build_default_engine():
    engine = RuleEngine()

    engine.register(Rule(
        "spam_keywords",
        keyword_condition(["buy now", "free money", "click here"]),
        "flag:spam",
        weight=3
    ))

    engine.register(Rule(
        "toxic_language",
        keyword_condition(["hate", "stupid", "idiot"]),
        "flag:toxic",
        weight=2
    ))

    engine.register(Rule(
        "shouting",
        regex_condition(r"[A-Z]{6,}"),
        "penalize",
        weight=2
    ))

    engine.register(Rule(
        "short_message",
        length_condition(max_len=10),
        "penalize",
        weight=1
    ))

    engine.register(Rule(
        "long_quality",
        length_condition(min_len=120),
        "boost",
        weight=2
    ))

    engine.register(Rule(
        "repetition",
        repetition_condition(),
        "flag:spam",
        weight=2
    ))

    return engine


def classify(ctx):
    if ctx.flags.get("spam", 0) >= 2:
        return "reject"

    if ctx.flags.get("toxic", 0) >= 1:
        return "review"

    if ctx.score > 2:
        return "promote"

    if ctx.score < -2:
        return "demote"

    return "neutral"


def summarize(items, engine):
    summary = {
        "reject": 0,
        "review": 0,
        "promote": 0,
        "demote": 0,
        "neutral": 0,
    }

    decisions = []

    for item in items:
        ctx = engine.evaluate(item)
        decision = classify(ctx)

        summary[decision] += 1

        decisions.append({
            "id": item.get("id"),
            "decision": decision,
            "flags": dict(ctx.flags),
            "labels": sorted(ctx.labels),
            "score": ctx.score,
        })

    return decisions, summary


def render(decisions):
    lines = []

    for d in decisions:
        lines.append(
            f"{d['id']} -> {d['decision']} "
            f"(score={d['score']}, flags={d['flags']})"
        )

    return "\n".join(lines)


def main():
    sample_items = [
        {"id": "p1", "text": "BUY NOW this is FREE MONEY click here"},
        {"id": "p2", "text": "I think this is a very detailed and helpful explanation of the topic."},
        {"id": "p3", "text": "you are stupid and I hate this"},
        {"id": "p4", "text": "ok"},
        {"id": "p5", "text": "hello hello hello hello hello hello hello"},
    ]

    engine = build_default_engine()
    decisions, summary = summarize(sample_items, engine)

    print(render(decisions))
    print("\nSummary:", summary)


if __name__ == "__main__":
    main()