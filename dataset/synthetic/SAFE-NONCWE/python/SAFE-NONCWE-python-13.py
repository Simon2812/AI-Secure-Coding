from itertools import combinations


def optimize_packing(items, constraints, capacity):
    valid_sets = _generate_valid_sets(items, constraints, capacity)

    best = None
    best_score = None

    for candidate in valid_sets:
        score = _score(candidate)

        if best_score is None or score > best_score:
            best_score = score
            best = candidate

    return best


def _generate_valid_sets(items, constraints, capacity):
    pool = list(items)
    n = len(pool)

    for r in range(1, n + 1):
        for subset in combinations(pool, r):
            if _fits_capacity(subset, capacity) and _respects_rules(subset, constraints):
                yield subset


def _fits_capacity(subset, capacity):
    total_weight = 0
    total_volume = 0

    for item in subset:
        total_weight += item[1]
        total_volume += item[2]

        if total_weight > capacity[0] or total_volume > capacity[1]:
            return False

    return True


def _respects_rules(subset, constraints):
    names = {item[0] for item in subset}

    for rule in constraints:
        kind = rule[0]

        if kind == "requires":
            if rule[1] in names and rule[2] not in names:
                return False

        elif kind == "conflict":
            if rule[1] in names and rule[2] in names:
                return False

        elif kind == "limit":
            tag = rule[1]
            limit = rule[2]
            count = sum(1 for item in subset if tag in item[3])
            if count > limit:
                return False

    return True


def _score(subset):
    utility = 0
    diversity = set()
    redundancy_penalty = 0

    for item in subset:
        name, weight, volume, tags, value = item

        utility += value
        diversity.update(tags)

        if "duplicate" in tags:
            redundancy_penalty += 1

    diversity_bonus = len(diversity) * 2

    return utility + diversity_bonus - redundancy_penalty * 3


def explain_selection(selection):
    explanation = []

    for item in selection:
        name, weight, volume, tags, value = item

        explanation.append(
            {
                "item": name,
                "weight": weight,
                "volume": volume,
                "value": value,
                "tags": tuple(tags),
            }
        )

    explanation.sort(key=lambda x: (-x["value"], x["item"]))
    return explanation


def category_distribution(selection):
    distribution = {}

    for item in selection:
        for tag in item[3]:
            distribution[tag] = distribution.get(tag, 0) + 1

    return dict(sorted(distribution.items(), key=lambda x: (-x[1], x[0])))


def detect_missing_essentials(selection, essentials):
    present = {item[0] for item in selection}
    missing = []

    for required in essentials:
        if required not in present:
            missing.append(required)

    return tuple(missing)


def swap_improvements(selection, items, constraints, capacity):
    current_score = _score(selection)
    best_moves = []

    selected_names = {item[0] for item in selection}

    for remove_item in selection:
        for add_item in items:
            if add_item[0] in selected_names:
                continue

            new_set = tuple(
                item for item in selection if item != remove_item
            ) + (add_item,)

            if not _fits_capacity(new_set, capacity):
                continue

            if not _respects_rules(new_set, constraints):
                continue

            new_score = _score(new_set)

            if new_score > current_score:
                best_moves.append(
                    (
                        remove_item[0],
                        add_item[0],
                        new_score - current_score,
                    )
                )

    best_moves.sort(key=lambda x: -x[2])
    return best_moves