from datetime import date, timedelta


PRIORITY_WEIGHTS = {
    "low": 1.0,
    "medium": 1.35,
    "high": 1.8,
}


def daterange(start_day, end_day):
    current = start_day
    while current <= end_day:
        yield current
        current += timedelta(days=1)


def normalize_topics(raw_topics):
    normalized = []

    for entry in raw_topics:
        topic = {
            "name": entry["name"].strip(),
            "subject": entry["subject"].strip(),
            "difficulty": max(1, min(5, int(entry["difficulty"]))),
            "estimated_hours": max(1.0, float(entry["estimated_hours"])),
            "deadline": entry["deadline"],
            "priority": entry["priority"].strip().lower(),
            "requires_review": bool(entry.get("requires_review", False)),
        }
        normalized.append(topic)

    return normalized


def score_topic(topic, today):
    days_left = max(1, (topic["deadline"] - today).days)
    urgency = 1 / days_left
    difficulty_factor = 0.7 + (topic["difficulty"] * 0.25)
    priority_factor = PRIORITY_WEIGHTS.get(topic["priority"], 1.0)
    review_factor = 1.15 if topic["requires_review"] else 1.0

    return (
        topic["estimated_hours"]
        * difficulty_factor
        * priority_factor
        * review_factor
        * (1 + urgency * 7)
    )


def split_topic_into_sessions(topic, today):
    days_left = max(1, (topic["deadline"] - today).days)

    if topic["estimated_hours"] <= 2:
        chunks = [topic["estimated_hours"]]
    elif topic["estimated_hours"] <= 5:
        chunks = _split_hours(topic["estimated_hours"], 2)
    else:
        target_parts = 3 if days_left > 3 else 2
        chunks = _split_hours(topic["estimated_hours"], target_parts)

    sessions = []
    for index, hours in enumerate(chunks, start=1):
        sessions.append(
            {
                "subject": topic["subject"],
                "topic": topic["name"],
                "session_label": f"{topic['name']} — part {index}",
                "hours": round(hours, 1),
                "deadline": topic["deadline"],
                "priority": topic["priority"],
                "difficulty": topic["difficulty"],
                "requires_review": topic["requires_review"],
            }
        )

    if topic["requires_review"]:
        sessions.append(
            {
                "subject": topic["subject"],
                "topic": topic["name"],
                "session_label": f"{topic['name']} — review",
                "hours": 1.0,
                "deadline": topic["deadline"],
                "priority": topic["priority"],
                "difficulty": max(1, topic["difficulty"] - 1),
                "requires_review": False,
            }
        )

    return sessions


def _split_hours(total_hours, parts):
    base = total_hours / parts
    pieces = [round(base, 1) for _ in range(parts)]

    difference = round(total_hours - sum(pieces), 1)
    index = 0
    step = 0.1 if difference > 0 else -0.1

    while round(difference, 1) != 0:
        pieces[index] = round(pieces[index] + step, 1)
        difference = round(difference - step, 1)
        index = (index + 1) % len(pieces)

    return pieces


def rank_sessions(topics, today):
    sessions = []

    for topic in topics:
        for session in split_topic_into_sessions(topic, today):
            days_left = max(1, (session["deadline"] - today).days)
            session_score = (
                session["hours"]
                * (0.8 + 0.2 * session["difficulty"])
                * PRIORITY_WEIGHTS.get(session["priority"], 1.0)
                * (1 + 6 / days_left)
            )
            session["score"] = round(session_score, 2)
            sessions.append(session)

    sessions.sort(
        key=lambda item: (
            -item["score"],
            item["deadline"],
            item["subject"],
            item["topic"],
        )
    )
    return sessions


def allocate_sessions(sessions, daily_capacity):
    calendar = []
    remaining = [dict(item) for item in sessions]

    for current_day in daily_capacity:
        free_hours = float(current_day["hours"])
        assigned = []

        cursor = 0
        while cursor < len(remaining) and free_hours > 0:
            session = remaining[cursor]

            if session["hours"] <= free_hours:
                assigned.append(session)
                free_hours = round(free_hours - session["hours"], 1)
                remaining.pop(cursor)
                continue

            if free_hours >= 1.0 and session["hours"] > 1.5:
                partial = dict(session)
                partial["session_label"] = session["session_label"] + " (partial)"
                partial["hours"] = round(free_hours, 1)

                session["hours"] = round(session["hours"] - free_hours, 1)
                assigned.append(partial)
                free_hours = 0
                break

            cursor += 1

        calendar.append(
            {
                "date": current_day["date"],
                "available_hours": current_day["hours"],
                "used_hours": round(current_day["hours"] - free_hours, 1),
                "sessions": assigned,
            }
        )

    return calendar, remaining


def build_study_plan(raw_topics, start_day, end_day, weekday_hours, weekend_hours):
    topics = normalize_topics(raw_topics)
    today = start_day

    ordered_topics = sorted(
        topics,
        key=lambda topic: (-score_topic(topic, today), topic["deadline"], topic["name"]),
    )

    sessions = rank_sessions(ordered_topics, today)

    capacity = []
    for day in daterange(start_day, end_day):
        hours = weekend_hours if day.weekday() in (4, 5) else weekday_hours
        capacity.append({"date": day, "hours": hours})

    plan, unassigned = allocate_sessions(sessions, capacity)
    return plan, unassigned


def render_plan(plan):
    lines = []

    for day in plan:
        lines.append(f"{day['date'].isoformat()}  [{day['used_hours']}/{day['available_hours']}h]")
        if not day["sessions"]:
            lines.append("  No study sessions assigned.")
            lines.append("")
            continue

        for session in day["sessions"]:
            lines.append(
                f"  - {session['subject']}: {session['session_label']} "
                f"({session['hours']}h, due {session['deadline'].isoformat()})"
            )
        lines.append("")

    return "\n".join(lines).rstrip()


def summarize_unassigned(unassigned):
    if not unassigned:
        return "All sessions were scheduled."

    total_hours = round(sum(item["hours"] for item in unassigned), 1)
    lines = [f"Unassigned sessions: {len(unassigned)} ({total_hours}h)"]

    for item in unassigned:
        lines.append(
            f"- {item['subject']} / {item['session_label']} / "
            f"{item['hours']}h / due {item['deadline'].isoformat()}"
        )

    return "\n".join(lines)


topics_input = [
    {
        "name": "Bayes theorem exercises",
        "subject": "Probability",
        "difficulty": 4,
        "estimated_hours": 5.5,
        "deadline": date(2026, 4, 12),
        "priority": "high",
        "requires_review": True,
    },
    {
        "name": "Shortest paths and MST",
        "subject": "Algorithms",
        "difficulty": 5,
        "estimated_hours": 6,
        "deadline": date(2026, 4, 10),
        "priority": "high",
        "requires_review": True,
    },
    {
        "name": "Matrix diagonalization",
        "subject": "Algebra",
        "difficulty": 3,
        "estimated_hours": 3.5,
        "deadline": date(2026, 4, 15),
        "priority": "medium",
        "requires_review": False,
    },
    {
        "name": "Feature scaling and leakage",
        "subject": "Data Science",
        "difficulty": 2,
        "estimated_hours": 2.5,
        "deadline": date(2026, 4, 11),
        "priority": "medium",
        "requires_review": True,
    },
    {
        "name": "Improper integrals",
        "subject": "Calculus",
        "difficulty": 4,
        "estimated_hours": 4,
        "deadline": date(2026, 4, 13),
        "priority": "high",
        "requires_review": False,
    },
]

study_plan, leftover_sessions = build_study_plan(
    raw_topics=topics_input,
    start_day=date(2026, 4, 7),
    end_day=date(2026, 4, 13),
    weekday_hours=2.5,
    weekend_hours=4.0,
)

plan_text = render_plan(study_plan)
leftover_text = summarize_unassigned(leftover_sessions)