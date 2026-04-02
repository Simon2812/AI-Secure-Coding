from bisect import insort
from datetime import timedelta


class TableLayout:
    def __init__(self):
        self._tables = {}              # table_id -> (capacity, zone)
        self._by_zone = {}             # zone -> [table_id]

    def add_table(self, table_id, capacity, zone):
        self._tables[table_id] = (capacity, zone)
        self._by_zone.setdefault(zone, []).append(table_id)

    def tables_in_zone(self, zone):
        return tuple(self._by_zone.get(zone, ()))

    def capacity(self, table_id):
        return self._tables[table_id][0]

    def zone(self, table_id):
        return self._tables[table_id][1]

    def all_tables(self):
        return tuple(self._tables.keys())


class ReservationBook:
    def __init__(self, layout):
        self._layout = layout
        self._timeline = {}     # table_id -> sorted list of (start, end, res_id)
        self._reservations = {} # res_id -> record

    def place(self, res_id, party_size, start, duration_minutes, preferred_zone=None):
        end = start + timedelta(minutes=duration_minutes)

        candidates = self._candidate_tables(party_size, preferred_zone)
        best = self._select_best_table(candidates, start, end, party_size)

        if best is None:
            return False

        self._commit(best, res_id, party_size, start, end)
        return True

    def cancel(self, res_id):
        record = self._reservations.pop(res_id, None)
        if record is None:
            return False

        table_id = record[0]
        slots = self._timeline.get(table_id, [])

        self._timeline[table_id] = [
            entry for entry in slots if entry[2] != res_id
        ]
        return True

    def rebalance(self, threshold=0.25):
        moves = []

        for table_id in self._layout.all_tables():
            schedule = list(self._timeline.get(table_id, []))

            for entry in schedule:
                res_id = entry[2]
                record = self._reservations.get(res_id)
                if record is None:
                    continue

                party_size = record[1]
                start = record[2]
                end = record[3]

                current_capacity = self._layout.capacity(table_id)
                waste = (current_capacity - party_size) / current_capacity

                if waste < threshold:
                    continue

                better = self._find_tighter_fit(
                    table_id, party_size, start, end
                )

                if better is not None:
                    self._move(res_id, table_id, better, start, end)
                    moves.append((res_id, table_id, better))

        return tuple(moves)

    def occupancy(self, window_start, window_end):
        result = {}

        for table_id in self._layout.all_tables():
            occupied = 0
            total = int((window_end - window_start).total_seconds() // 60)

            for start, end, _ in self._timeline.get(table_id, []):
                overlap = _overlap(start, end, window_start, window_end)
                occupied += overlap

            ratio = (occupied / total) if total else 0
            result[table_id] = round(ratio * 100, 1)

        return result

    def idle_gaps(self, table_id):
        slots = sorted(self._timeline.get(table_id, []))
        gaps = []

        for i in range(len(slots) - 1):
            end_current = slots[i][1]
            start_next = slots[i + 1][0]

            if start_next > end_current:
                gaps.append((end_current, start_next))

        return tuple(gaps)

    def _candidate_tables(self, party_size, preferred_zone):
        if preferred_zone is not None:
            tables = self._layout.tables_in_zone(preferred_zone)
        else:
            tables = self._layout.all_tables()

        return [
            t for t in tables
            if self._layout.capacity(t) >= party_size
        ]

    def _select_best_table(self, candidates, start, end, party_size):
        best = None
        best_score = None

        for table_id in candidates:
            if not self._is_free(table_id, start, end):
                continue

            capacity = self._layout.capacity(table_id)
            slack = capacity - party_size
            density = len(self._timeline.get(table_id, []))

            score = slack * 10 + density

            if best_score is None or score < best_score:
                best_score = score
                best = table_id

        return best

    def _is_free(self, table_id, start, end):
        for s, e, _ in self._timeline.get(table_id, []):
            if not (end <= s or start >= e):
                return False
        return True

    def _commit(self, table_id, res_id, party_size, start, end):
        slots = self._timeline.setdefault(table_id, [])
        insort(slots, (start, end, res_id))

        self._reservations[res_id] = (
            table_id,
            party_size,
            start,
            end,
        )

    def _move(self, res_id, from_table, to_table, start, end):
        self._timeline[from_table] = [
            entry for entry in self._timeline[from_table]
            if entry[2] != res_id
        ]

        insort(self._timeline.setdefault(to_table, []), (start, end, res_id))

        record = self._reservations[res_id]
        self._reservations[res_id] = (
            to_table,
            record[1],
            start,
            end,
        )

    def _find_tighter_fit(self, current_table, party_size, start, end):
        candidates = self._candidate_tables(party_size, None)

        best = None
        best_capacity = None

        for table_id in candidates:
            if table_id == current_table:
                continue

            if not self._is_free(table_id, start, end):
                continue

            capacity = self._layout.capacity(table_id)

            if best_capacity is None or capacity < best_capacity:
                best_capacity = capacity
                best = table_id

        return best


def _overlap(a_start, a_end, b_start, b_end):
    latest = max(a_start, b_start)
    earliest = min(a_end, b_end)

    if latest >= earliest:
        return 0

    return int((earliest - latest).total_seconds() // 60)