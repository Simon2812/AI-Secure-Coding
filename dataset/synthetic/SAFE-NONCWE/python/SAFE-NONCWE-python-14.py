from collections import deque


def build_graph(courses):
    graph = {}
    reverse = {}

    for course in courses:
        cid = course["id"]
        prereqs = set(course.get("prerequisites", []))

        graph[cid] = prereqs

        for p in prereqs:
            reverse.setdefault(p, set()).add(cid)

    return graph, reverse


def detect_cycles(graph):
    visited = set()
    stack = set()
    cycles = []

    def dfs(node, path):
        if node in stack:
            idx = path.index(node)
            cycles.append(tuple(path[idx:]))
            return

        if node in visited:
            return

        visited.add(node)
        stack.add(node)

        for neighbor in graph.get(node, ()):
            dfs(neighbor, path + [neighbor])

        stack.remove(node)

    for node in graph:
        dfs(node, [node])

    return cycles


def compute_unlock_levels(graph):
    indegree = {node: 0 for node in graph}

    for node in graph:
        for prereq in graph[node]:
            indegree[node] += 1

    queue = deque([n for n in graph if indegree[n] == 0])
    level = {n: 0 for n in queue}

    while queue:
        current = queue.popleft()

        for node in graph:
            if current in graph[node]:
                indegree[node] -= 1
                if indegree[node] == 0:
                    level[node] = level[current] + 1
                    queue.append(node)

    return level


def reachable_courses(graph, completed):
    reachable = set(completed)
    changed = True

    while changed:
        changed = False

        for course, prereqs in graph.items():
            if course in reachable:
                continue

            if prereqs.issubset(reachable):
                reachable.add(course)
                changed = True

    return reachable


def blocking_dependencies(graph, target, completed):
    missing = set()

    def collect(course):
        for prereq in graph.get(course, ()):
            if prereq not in completed:
                missing.add(prereq)
                collect(prereq)

    collect(target)
    return missing


def prioritize_courses(graph, completed, weights):
    candidates = []

    for course, prereqs in graph.items():
        if course in completed:
            continue

        if not prereqs.issubset(completed):
            continue

        score = weights.get(course, 1)

        dependents = _count_dependents(graph, course)
        depth = _max_depth(graph, course)

        score += dependents * 2
        score += depth

        candidates.append((score, course))

    candidates.sort(reverse=True)
    return [c for _, c in candidates]


def _count_dependents(graph, node):
    count = 0

    for course, prereqs in graph.items():
        if node in prereqs:
            count += 1

    return count


def _max_depth(graph, node):
    visited = set()

    def dfs(n):
        if n in visited:
            return 0
        visited.add(n)

        depths = [dfs(child) for child, prereqs in graph.items() if n in prereqs]
        return 1 + (max(depths) if depths else 0)

    return dfs(node)


def learning_path(graph, start_courses):
    path = []
    completed = set(start_courses)

    while True:
        next_batch = []

        for course, prereqs in graph.items():
            if course in completed:
                continue

            if prereqs.issubset(completed):
                next_batch.append(course)

        if not next_batch:
            break

        next_batch.sort()
        path.append(tuple(next_batch))
        completed.update(next_batch)

    return tuple(path)


def validate_catalog(graph):
    issues = []

    for course, prereqs in graph.items():
        if course in prereqs:
            issues.append((course, "self_dependency"))

        for prereq in prereqs:
            if prereq not in graph:
                issues.append((course, "unknown_prerequisite", prereq))

    cycles = detect_cycles(graph)
    for cycle in cycles:
        issues.append(("cycle", cycle))

    return issues