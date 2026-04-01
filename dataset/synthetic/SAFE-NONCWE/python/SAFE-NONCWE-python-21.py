from collections import defaultdict


def build_standings(matches):
    table = {}

    for match in matches:
        a, b, score_a, score_b = match

        _ensure_team(table, a)
        _ensure_team(table, b)

        table[a]["played"] += 1
        table[b]["played"] += 1

        table[a]["scored"] += score_a
        table[a]["conceded"] += score_b

        table[b]["scored"] += score_b
        table[b]["conceded"] += score_a

        if score_a > score_b:
            table[a]["points"] += 3
            table[a]["wins"] += 1
            table[b]["losses"] += 1
        elif score_b > score_a:
            table[b]["points"] += 3
            table[b]["wins"] += 1
            table[a]["losses"] += 1
        else:
            table[a]["points"] += 1
            table[b]["points"] += 1
            table[a]["draws"] += 1
            table[b]["draws"] += 1

    for team in table:
        table[team]["goal_diff"] = table[team]["scored"] - table[team]["conceded"]

    return table


def rank_teams(table, matches):
    teams = list(table.keys())

    teams.sort(
        key=lambda t: (
            -table[t]["points"],
            -table[t]["goal_diff"],
            -table[t]["scored"],
            t,
        )
    )

    return _resolve_ties(teams, table, matches)


def _resolve_ties(ordered, table, matches):
    i = 0
    result = []

    while i < len(ordered):
        j = i + 1

        while j < len(ordered) and _tie_equal(ordered[i], ordered[j], table):
            j += 1

        group = ordered[i:j]

        if len(group) > 1:
            group = _break_tie(group, table, matches)

        result.extend(group)
        i = j

    return result


def _tie_equal(a, b, table):
    return (
        table[a]["points"] == table[b]["points"] and
        table[a]["goal_diff"] == table[b]["goal_diff"] and
        table[a]["scored"] == table[b]["scored"]
    )


def _break_tie(group, table, matches):
    head_table = _mini_table(group, matches)

    ranked = list(group)
    ranked.sort(
        key=lambda t: (
            -head_table[t]["points"],
            -head_table[t]["goal_diff"],
            -head_table[t]["scored"],
            t,
        )
    )

    return ranked


def _mini_table(group, matches):
    subset = defaultdict(lambda: {
        "points": 0,
        "scored": 0,
        "conceded": 0,
        "goal_diff": 0,
    })

    group_set = set(group)

    for a, b, sa, sb in matches:
        if a not in group_set or b not in group_set:
            continue

        subset[a]["scored"] += sa
        subset[a]["conceded"] += sb

        subset[b]["scored"] += sb
        subset[b]["conceded"] += sa

        if sa > sb:
            subset[a]["points"] += 3
        elif sb > sa:
            subset[b]["points"] += 3
        else:
            subset[a]["points"] += 1
            subset[b]["points"] += 1

    for team in subset:
        subset[team]["goal_diff"] = subset[team]["scored"] - subset[team]["conceded"]

    return subset


def _ensure_team(table, name):
    if name not in table:
        table[name] = {
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "points": 0,
            "scored": 0,
            "conceded": 0,
            "goal_diff": 0,
        }


def extract_form(matches, team, last_n=5):
    recent = []

    for a, b, sa, sb in matches:
        if a == team or b == team:
            if a == team:
                if sa > sb:
                    recent.append("W")
                elif sa < sb:
                    recent.append("L")
                else:
                    recent.append("D")
            else:
                if sb > sa:
                    recent.append("W")
                elif sb < sa:
                    recent.append("L")
                else:
                    recent.append("D")

    return tuple(recent[-last_n:])


def scoring_distribution(matches):
    distribution = defaultdict(int)

    for _, _, sa, sb in matches:
        distribution[sa] += 1
        distribution[sb] += 1

    return dict(sorted(distribution.items()))


def detect_dominant_teams(table, threshold=0.7):
    total_matches = sum(team["played"] for team in table.values()) / 2
    dominant = []

    for team, stats in table.items():
        if stats["played"] == 0:
            continue

        win_ratio = stats["wins"] / stats["played"]

        if win_ratio >= threshold:
            dominant.append((team, round(win_ratio, 2)))

    dominant.sort(key=lambda x: -x[1])
    return tuple(dominant)


def consistency_index(matches, team):
    results = extract_form(matches, team, last_n=20)

    if not results:
        return 0.0

    streak = 0
    current = None
    switches = 0

    for r in results:
        if r != current:
            if current is not None:
                switches += 1
            current = r
        streak += 1

    return round(1 / (1 + switches), 3)