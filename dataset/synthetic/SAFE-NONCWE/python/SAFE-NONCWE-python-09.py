from typing import List, Tuple


# Order: (order_id, zone, size, preferred_start, preferred_end)
# Vehicle: (vehicle_id, zone, capacity, shift_start, shift_end)


def assign_orders(orders: List[Tuple], vehicles: List[Tuple]):
    assignments = []
    unassigned = []

    vehicle_state = [
        {
            "vehicle": v,
            "remaining_capacity": v[2],
            "timeline": [],
        }
        for v in vehicles
    ]

    sorted_orders = sorted(
        orders,
        key=lambda o: (o[3], o[4], -o[2])
    )

    for order in sorted_orders:
        best_fit_index = _select_vehicle(order, vehicle_state)

        if best_fit_index == -1:
            unassigned.append(order)
            continue

        vehicle_state[best_fit_index]["remaining_capacity"] -= order[2]
        vehicle_state[best_fit_index]["timeline"].append(order)

        assignments.append(
            (
                order[0],
                vehicle_state[best_fit_index]["vehicle"][0],
                order[3],
                order[4],
            )
        )

    return assignments, unassigned


def _select_vehicle(order, vehicle_state):
    best_index = -1
    best_score = None

    for idx, state in enumerate(vehicle_state):
        vehicle = state["vehicle"]

        if vehicle[1] != order[1]:
            continue

        if state["remaining_capacity"] < order[2]:
            continue

        if not _time_fits(order, state["timeline"], vehicle):
            continue

        score = _fit_score(order, state)

        if best_score is None or score < best_score:
            best_score = score
            best_index = idx

    return best_index


def _time_fits(order, assigned_orders, vehicle):
    start, end = order[3], order[4]

    if start < vehicle[3] or end > vehicle[4]:
        return False

    for existing in assigned_orders:
        if not (end <= existing[3] or start >= existing[4]):
            return False

    return True


def _fit_score(order, state):
    slack_capacity = state["remaining_capacity"] - order[2]
    timeline_load = len(state["timeline"])

    return slack_capacity * 10 + timeline_load


def build_vehicle_timeline(assignments: List[Tuple]):
    timeline = {}

    for order_id, vehicle_id, start, end in assignments:
        bucket = timeline.setdefault(vehicle_id, [])
        bucket.append((start, end, order_id))

    for vehicle_id in timeline:
        timeline[vehicle_id].sort(key=lambda x: x[0])

    return timeline


def detect_overflow(unassigned_orders: List[Tuple]):
    overflow_by_zone = {}

    for order in unassigned_orders:
        zone = order[1]
        overflow_by_zone[zone] = overflow_by_zone.get(zone, 0) + order[2]

    return overflow_by_zone


def compress_idle_gaps(timeline: List[Tuple]):
    if not timeline:
        return []

    timeline = sorted(timeline, key=lambda x: x[0])
    gaps = []

    for i in range(len(timeline) - 1):
        current_end = timeline[i][1]
        next_start = timeline[i + 1][0]

        if next_start > current_end:
            gaps.append((current_end, next_start))

    return gaps


def reassign_small_orders(unassigned_orders: List[Tuple], vehicles: List[Tuple]):
    reassigned = []
    still_unassigned = []

    small_orders = [o for o in unassigned_orders if o[2] <= 1]
    large_orders = [o for o in unassigned_orders if o[2] > 1]

    for order in small_orders:
        for vehicle in vehicles:
            if vehicle[1] == order[1]:
                reassigned.append((order[0], vehicle[0]))
                break
        else:
            still_unassigned.append(order)

    still_unassigned.extend(large_orders)

    return reassigned, still_unassigned