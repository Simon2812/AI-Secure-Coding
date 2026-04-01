from datetime import datetime, timedelta
from collections import defaultdict, deque
import math


class AppointmentBook:
    def __init__(self):
        self._appointments = []
        self._by_patient = defaultdict(list)
        self._by_day = defaultdict(list)

    def add(self, appointment_id, patient_id, scheduled_at, duration_min, status):
        record = {
            "id": appointment_id,
            "patient": patient_id,
            "scheduled_at": scheduled_at,
            "duration": duration_min,
            "status": status,  # "attended", "missed", "cancelled"
        }

        self._appointments.append(record)
        self._by_patient[patient_id].append(record)
        self._by_day[scheduled_at.date()].append(record)

    def all(self):
        return tuple(self._appointments)

    def patient_history(self, patient_id):
        return tuple(self._by_patient.get(patient_id, []))

    def day_schedule(self, day):
        return tuple(self._by_day.get(day, []))


class NoShowModel:
    def __init__(self):
        self._patient_stats = {}
        self._hour_stats = defaultdict(lambda: {"total": 0, "missed": 0})

    def train(self, appointments):
        for appt in appointments:
            pid = appt["patient"]
            hour = appt["scheduled_at"].hour

            ps = self._patient_stats.setdefault(pid, {"total": 0, "missed": 0})
            ps["total"] += 1

            if appt["status"] == "missed":
                ps["missed"] += 1

            hs = self._hour_stats[hour]
            hs["total"] += 1

            if appt["status"] == "missed":
                hs["missed"] += 1

    def predict(self, patient_id, when):
        p = self._patient_stats.get(patient_id)
        h = self._hour_stats.get(when.hour)

        base = 0.1

        if p:
            base += (p["missed"] / p["total"]) * 0.6

        if h and h["total"] > 0:
            base += (h["missed"] / h["total"]) * 0.3

        return min(1.0, base)


class SlotAllocator:
    def __init__(self, model):
        self._model = model

    def optimize_day(self, appointments):
        enriched = []

        for appt in appointments:
            risk = self._model.predict(appt["patient"], appt["scheduled_at"])

            enriched.append((appt, risk))

        enriched.sort(key=lambda x: -x[1])

        slots = []
        overflow = []

        buffer_minutes = 0

        for appt, risk in enriched:
            adjusted_duration = appt["duration"]

            if risk > 0.6:
                buffer_minutes += 5
                adjusted_duration = max(5, appt["duration"] - 5)

            if risk > 0.8:
                overflow.append(appt)
                continue

            slots.append(
                (
                    appt["id"],
                    appt["scheduled_at"],
                    adjusted_duration,
                    round(risk, 2),
                )
            )

        return tuple(slots), tuple(overflow), buffer_minutes


class DriftTracker:
    def __init__(self):
        self._history = defaultdict(lambda: deque(maxlen=20))

    def update(self, day, attended, missed):
        total = attended + missed
        if total == 0:
            return

        ratio = missed / total
        self._history[day.weekday()].append(ratio)

    def drift(self):
        result = []

        for weekday, values in self._history.items():
            if len(values) < 5:
                continue

            avg = sum(values) / len(values)
            variance = sum((v - avg) ** 2 for v in values) / len(values)

            if variance > 0.02:
                result.append((weekday, round(variance, 4)))

        return tuple(sorted(result, key=lambda x: -x[1]))


class RebookingEngine:
    def __init__(self, model):
        self._model = model

    def suggest(self, overflow, horizon_days=5):
        suggestions = []

        for appt in overflow:
            best_day = None
            best_score = None

            for offset in range(1, horizon_days + 1):
                new_time = appt["scheduled_at"] + timedelta(days=offset)
                risk = self._model.predict(appt["patient"], new_time)

                score = (1 - risk) * 10 - offset

                if best_score is None or score > best_score:
                    best_score = score
                    best_day = new_time

            suggestions.append(
                (
                    appt["id"],
                    appt["scheduled_at"],
                    best_day,
                    round(best_score, 2),
                )
            )

        return tuple(suggestions)


class CapacityAnalyzer:
    def __init__(self):
        self._utilization = defaultdict(list)

    def record_day(self, day, schedule):
        total = sum(slot[2] for slot in schedule)
        self._utilization[day.weekday()].append(total)

    def peak_days(self):
        peaks = []

        for weekday, values in self._utilization.items():
            if not values:
                continue

            avg = sum(values) / len(values)
            peaks.append((weekday, round(avg, 2)))

        return tuple(sorted(peaks, key=lambda x: -x[1]))

    def imbalance(self):
        averages = [
            sum(v) / len(v) for v in self._utilization.values() if v
        ]

        if not averages:
            return 0.0

        avg = sum(averages) / len(averages)
        variance = sum((v - avg) ** 2 for v in averages) / len(averages)

        return round(math.sqrt(variance), 3)