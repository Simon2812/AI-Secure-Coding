from collections import deque, defaultdict


class RotationState:
    def __init__(self, members, chores):
        self._members = list(members)
        self._chores = dict(chores)  # chore -> difficulty

        self._history = defaultdict(list)   # member -> [chore,...]
        self._fatigue = {m: 0 for m in members}
        self._last_assigned = {m: None for m in members}

        self._queue = deque(self._members)

    def step(self):
        assignments = []

        for chore, difficulty in self._chores.items():
            member = self._select_member(chore, difficulty)
            assignments.append((member, chore))

            self._apply_assignment(member, chore, difficulty)

        self._queue.rotate(-1)
        return tuple(assignments)

    def simulate(self, days):
        timeline = []

        for _ in range(days):
            daily = self.step()
            timeline.append(daily)

        return tuple(timeline)

    def fairness_score(self):
        scores = []

        for member in self._members:
            load = sum(self._difficulty(c) for c in self._history[member])
            variance = abs(load - self._average_load())

            repetition_penalty = self._repetition_penalty(member)

            score = load - variance - repetition_penalty
            scores.append(score)

        return round(sum(scores) / len(scores), 2) if scores else 0.0

    def member_load(self, member):
        return sum(self._difficulty(c) for c in self._history[member])

    def history(self, member):
        return tuple(self._history[member])

    def _select_member(self, chore, difficulty):
        best = None
        best_score = None

        for member in self._queue:
            score = self._candidate_score(member, chore, difficulty)

            if best_score is None or score < best_score:
                best_score = score
                best = member

        return best

    def _candidate_score(self, member, chore, difficulty):
        fatigue = self._fatigue[member]
        last = self._last_assigned[member]

        repetition = 5 if last == chore else 0
        imbalance = abs(self.member_load(member) - self._average_load())

        return fatigue + repetition + imbalance + difficulty

    def _apply_assignment(self, member, chore, difficulty):
        self._history[member].append(chore)
        self._fatigue[member] += difficulty

        if len(self._history[member]) > 3:
            self._fatigue[member] = max(0, self._fatigue[member] - 1)

        self._last_assigned[member] = chore

    def _average_load(self):
        if not self._members:
            return 0

        total = sum(self.member_load(m) for m in self._members)
        return total / len(self._members)

    def _repetition_penalty(self, member):
        history = self._history[member]
        penalty = 0

        for i in range(1, len(history)):
            if history[i] == history[i - 1]:
                penalty += 2

        return penalty

    def _difficulty(self, chore):
        return self._chores.get(chore, 0)


class RotationInspector:
    def __init__(self, state):
        self._state = state

    def imbalance_report(self):
        report = []

        avg = self._state._average_load()

        for member in self._state._members:
            load = self._state.member_load(member)
            delta = round(load - avg, 2)

            report.append((member, load, delta))

        report.sort(key=lambda x: -abs(x[2]))
        return tuple(report)

    def most_repeated_chore(self):
        counter = defaultdict(int)

        for member in self._state._members:
            for chore in self._state.history(member):
                counter[chore] += 1

        if not counter:
            return None

        return max(counter.items(), key=lambda x: x[1])[0]

    def streaks(self, member):
        history = self._state.history(member)
        streaks = []

        if not history:
            return tuple()

        current = history[0]
        length = 1

        for item in history[1:]:
            if item == current:
                length += 1
            else:
                if length > 1:
                    streaks.append((current, length))
                current = item
                length = 1

        if length > 1:
            streaks.append((current, length))

        return tuple(streaks)