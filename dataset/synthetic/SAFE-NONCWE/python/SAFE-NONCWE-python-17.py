from datetime import date, timedelta
from collections import defaultdict, deque


class Ledger:
    def __init__(self):
        self._entries = []

    def add(self, when, category, amount, note=""):
        self._entries.append((when, category, float(amount), note))

    def entries(self):
        return tuple(self._entries)

    def between(self, start, end):
        return [
            e for e in self._entries
            if start <= e[0] <= end
        ]


class CategoryProfile:
    def __init__(self, name):
        self.name = name
        self._history = deque(maxlen=30)
        self._total = 0.0

    def record(self, amount):
        self._history.append(amount)
        self._total += amount

    def rolling_average(self):
        if not self._history:
            return 0.0
        return sum(self._history) / len(self._history)

    def total(self):
        return self._total

    def volatility(self):
        if len(self._history) < 2:
            return 0.0

        avg = self.rolling_average()
        variance = sum((x - avg) ** 2 for x in self._history) / len(self._history)
        return variance ** 0.5


class BudgetModel:
    def __init__(self):
        self._profiles = {}
        self._daily_totals = defaultdict(float)

    def ingest(self, ledger):
        for when, category, amount, _ in ledger.entries():
            profile = self._profiles.setdefault(category, CategoryProfile(category))
            profile.record(amount)
            self._daily_totals[when] += amount

    def forecast(self, days_forward):
        today = max(self._daily_totals.keys(), default=date.today())
        forecast = []

        for i in range(1, days_forward + 1):
            day = today + timedelta(days=i)
            estimate = self._estimate_day()

            forecast.append((day, round(estimate, 2)))

        return tuple(forecast)

    def category_breakdown(self):
        result = []

        for category, profile in self._profiles.items():
            result.append(
                (
                    category,
                    round(profile.total(), 2),
                    round(profile.rolling_average(), 2),
                    round(profile.volatility(), 2),
                )
            )

        result.sort(key=lambda x: -x[1])
        return tuple(result)

    def detect_drift(self, threshold=0.25):
        drifted = []

        for category, profile in self._profiles.items():
            avg = profile.rolling_average()
            vol = profile.volatility()

            if avg == 0:
                continue

            ratio = vol / avg

            if ratio > threshold:
                drifted.append((category, round(ratio, 2)))

        drifted.sort(key=lambda x: -x[1])
        return tuple(drifted)

    def peak_spending_days(self, top_n=5):
        days = sorted(
            self._daily_totals.items(),
            key=lambda x: -x[1]
        )
        return tuple((d, round(v, 2)) for d, v in days[:top_n])

    def _estimate_day(self):
        if not self._profiles:
            return 0.0

        base = 0.0

        for profile in self._profiles.values():
            base += profile.rolling_average()

        fluctuation = sum(profile.volatility() for profile in self._profiles.values())

        return base + fluctuation * 0.3


class AnomalyScanner:
    def __init__(self, ledger):
        self._ledger = ledger

    def unusual_spikes(self, multiplier=2.5):
        per_category = defaultdict(list)

        for when, category, amount, _ in self._ledger.entries():
            per_category[category].append((when, amount))

        anomalies = []

        for category, entries in per_category.items():
            amounts = [a for _, a in entries]
            if not amounts:
                continue

            avg = sum(amounts) / len(amounts)

            for when, amount in entries:
                if avg > 0 and amount > avg * multiplier:
                    anomalies.append((category, when, amount, round(avg, 2)))

        anomalies.sort(key=lambda x: -x[2])
        return tuple(anomalies)

    def category_imbalance(self):
        totals = defaultdict(float)

        for _, category, amount, _ in self._ledger.entries():
            totals[category] += amount

        if not totals:
            return ()

        avg = sum(totals.values()) / len(totals)

        imbalance = []
        for category, total in totals.items():
            delta = total - avg
            imbalance.append((category, round(delta, 2)))

        imbalance.sort(key=lambda x: -abs(x[1]))
        return tuple(imbalance)


class ReportBuilder:
    def __init__(self, model, scanner):
        self._model = model
        self._scanner = scanner

    def build_lines(self):
        lines = []

        lines.append("=== CATEGORY BREAKDOWN ===")
        for category, total, avg, vol in self._model.category_breakdown():
            lines.append(
                f"{category}: total={total} avg={avg} volatility={vol}"
            )

        lines.append("\n=== DRIFT DETECTION ===")
        for category, ratio in self._model.detect_drift():
            lines.append(f"{category}: drift_ratio={ratio}")

        lines.append("\n=== PEAK DAYS ===")
        for d, val in self._model.peak_spending_days():
            lines.append(f"{d.isoformat()}: {val}")

        lines.append("\n=== ANOMALIES ===")
        for category, when, amount, avg in self._scanner.unusual_spikes():
            lines.append(
                f"{category} on {when.isoformat()} -> {amount} (avg {avg})"
            )

        return tuple(lines)

    def render(self):
        return "\n".join(self.build_lines())