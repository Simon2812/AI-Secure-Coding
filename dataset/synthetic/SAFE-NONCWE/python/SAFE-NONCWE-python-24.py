from collections import defaultdict, deque


DIRECTIONS = ("N", "S", "E", "W")


def _delta(direction):
    if direction == "N":
        return (-1, 0)
    if direction == "S":
        return (1, 0)
    if direction == "E":
        return (0, 1)
    if direction == "W":
        return (0, -1)
    return (0, 0)


class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self._cells = {}

    def in_bounds(self, pos):
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def set_cell(self, pos, kind):
        self._cells[pos] = kind

    def get_cell(self, pos):
        return self._cells.get(pos, "road")

    def neighbors(self, pos):
        for d in DIRECTIONS:
            dr, dc = _delta(d)
            nxt = (pos[0] + dr, pos[1] + dc)
            if self.in_bounds(nxt):
                yield nxt


class TrafficLight:
    def __init__(self, cycle):
        self._cycle = list(cycle)
        self._index = 0
        self._timer = self._cycle[0][1]

    def step(self):
        self._timer -= 1
        if self._timer <= 0:
            self._index = (self._index + 1) % len(self._cycle)
            self._timer = self._cycle[self._index][1]

    def allows(self, direction):
        state = self._cycle[self._index][0]
        return direction in state


class Vehicle:
    def __init__(self, vid, position, direction):
        self.id = vid
        self.pos = position
        self.dir = direction
        self.wait = 0
        self.history = []

    def next_position(self):
        dr, dc = _delta(self.dir)
        return (self.pos[0] + dr, self.pos[1] + dc)

    def record(self):
        self.history.append(self.pos)


class RoadNetwork:
    def __init__(self, grid):
        self._grid = grid
        self._lights = {}
        self._vehicles = {}
        self._occupied = {}
        self._entry_points = set()

    def add_light(self, pos, light):
        self._lights[pos] = light

    def add_vehicle(self, vehicle):
        self._vehicles[vehicle.id] = vehicle
        self._occupied[vehicle.pos] = vehicle.id

    def add_entry(self, pos):
        self._entry_points.add(pos)

    def step(self):
        proposals = []
        blocked = set()

        for vid, vehicle in self._vehicles.items():
            vehicle.record()

            nxt = vehicle.next_position()

            if not self._grid.in_bounds(nxt):
                blocked.add(vid)
                continue

            if self._grid.get_cell(nxt) == "wall":
                blocked.add(vid)
                continue

            if nxt in self._lights:
                light = self._lights[nxt]
                if not light.allows(vehicle.dir):
                    blocked.add(vid)
                    vehicle.wait += 1
                    continue

            proposals.append((vid, vehicle.pos, nxt))

        resolved = self._resolve_conflicts(proposals)

        self._apply_moves(resolved, blocked)
        self._update_lights()

    def _resolve_conflicts(self, proposals):
        target_map = defaultdict(list)

        for vid, src, dst in proposals:
            target_map[dst].append((vid, src, dst))

        resolved = []

        for dst, moves in target_map.items():
            if len(moves) == 1:
                resolved.append(moves[0])
            else:
                best = min(moves, key=lambda m: self._vehicles[m[0]].wait)
                resolved.append(best)

        return resolved

    def _apply_moves(self, moves, blocked):
        new_occupied = {}

        for vid, vehicle in self._vehicles.items():
            if vid in blocked:
                new_occupied[vehicle.pos] = vid
                continue

            moved = False

            for m_vid, src, dst in moves:
                if m_vid == vid:
                    vehicle.pos = dst
                    vehicle.wait = 0
                    new_occupied[dst] = vid
                    moved = True
                    break

            if not moved:
                new_occupied[vehicle.pos] = vid

        self._occupied = new_occupied

    def _update_lights(self):
        for light in self._lights.values():
            light.step()

    def density(self):
        return len(self._vehicles) / (self._grid.rows * self._grid.cols)

    def congestion_map(self):
        heat = defaultdict(int)

        for v in self._vehicles.values():
            heat[v.pos] += 1

        return dict(heat)

    def stalled_vehicles(self, threshold=3):
        result = []

        for v in self._vehicles.values():
            if v.wait >= threshold:
                result.append((v.id, v.pos, v.wait))

        return tuple(result)

    def flow_rate(self):
        total_moves = 0

        for v in self._vehicles.values():
            total_moves += len(v.history)

        if not self._vehicles:
            return 0.0

        return total_moves / len(self._vehicles)

    def longest_wait(self):
        if not self._vehicles:
            return 0

        return max(v.wait for v in self._vehicles.values())

    def region_pressure(self, center, radius):
        cr, cc = center
        count = 0

        for v in self._vehicles.values():
            r, c = v.pos
            if abs(r - cr) <= radius and abs(c - cc) <= radius:
                count += 1

        return count

    def redistribute(self):
        overloaded = self.stalled_vehicles(5)

        for vid, pos, _ in overloaded:
            vehicle = self._vehicles[vid]

            for d in DIRECTIONS:
                dr, dc = _delta(d)
                alt = (pos[0] + dr, pos[1] + dc)

                if self._grid.in_bounds(alt) and alt not in self._occupied:
                    vehicle.dir = d
                    break

    def snapshot(self):
        return {
            "vehicles": len(self._vehicles),
            "density": round(self.density(), 3),
            "flow": round(self.flow_rate(), 2),
            "max_wait": self.longest_wait(),
        }