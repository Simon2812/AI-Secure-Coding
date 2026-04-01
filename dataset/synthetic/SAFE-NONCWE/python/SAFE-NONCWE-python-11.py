from datetime import timedelta


class TimetableScanner:
    def __init__(self, routes):
        self._routes = routes
        self._route_index = 0
        self._trip_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self._route_index < len(self._routes):
            route = self._routes[self._route_index]
            trips = route[1]

            if self._trip_index >= len(trips):
                self._route_index += 1
                self._trip_index = 0
                continue

            trip = trips[self._trip_index]
            self._trip_index += 1

            issue = _check_trip(route[0], trip)
            if issue is not None:
                return issue

        raise StopIteration


def _check_trip(route_id, trip):
    stops = trip[0]
    times = trip[1]

    if len(stops) != len(times):
        return (route_id, "length_mismatch", stops, times)

    for i in range(len(times) - 1):
        if times[i + 1] <= times[i]:
            return (route_id, "non_increasing_time", trip)

    total_duration = times[-1] - times[0]
    if total_duration <= timedelta(minutes=1):
        return (route_id, "too_short_trip", trip)

    return None


def find_large_gaps(routes, threshold_minutes):
    threshold = timedelta(minutes=threshold_minutes)

    for route_id, trips in routes:
        ordered = sorted(trips, key=lambda t: t[1][0])

        for i in range(len(ordered) - 1):
            end_current = ordered[i][1][-1]
            start_next = ordered[i + 1][1][0]

            gap = start_next - end_current
            if gap > threshold:
                yield (route_id, gap, ordered[i], ordered[i + 1])


def detect_route_direction_conflicts(routes):
    for route_id, trips in routes:
        seen_patterns = set()

        for trip in trips:
            stops = tuple(trip[0])
            reversed_stops = tuple(reversed(stops))

            if reversed_stops in seen_patterns:
                yield (route_id, "reverse_direction_overlap", stops)

            seen_patterns.add(stops)


def compress_route_signature(trip):
    stops = trip[0]
    signature = []

    last = None
    for stop in stops:
        if stop != last:
            signature.append(stop)
            last = stop

    return tuple(signature)


def group_similar_trips(routes):
    for route_id, trips in routes:
        signatures = {}

        for trip in trips:
            sig = compress_route_signature(trip)
            signatures.setdefault(sig, []).append(trip)

        yield route_id, tuple((sig, len(group)) for sig, group in signatures.items())