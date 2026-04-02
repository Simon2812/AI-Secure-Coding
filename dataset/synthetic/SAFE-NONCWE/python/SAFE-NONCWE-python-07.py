from collections import defaultdict
from typing import Iterable, Dict, Generator, Tuple


def evaluate_attempts_stream(attempts: Iterable[Dict]) -> Generator[Tuple[str, Dict], None, None]:
    user_state = {}

    for attempt in attempts:
        user_id = attempt["user_id"]

        if user_id not in user_state:
            user_state[user_id] = {
                "points": 0,
                "max": 0,
                "answers": 0,
                "correct": 0,
                "skills": defaultdict(lambda: [0, 0, 0, 0]),  
                # [points, max, correct, count]
            }

        state = user_state[user_id]

        for answer in attempt["answers"]:
            pts = int(answer["points_awarded"])
            max_pts = int(answer["max_points"])
            correct = 1 if answer["is_correct"] else 0
            skill = answer["skill"]

            state["points"] += pts
            state["max"] += max_pts
            state["answers"] += 1
            state["correct"] += correct

            skill_data = state["skills"][skill]
            skill_data[0] += pts
            skill_data[1] += max_pts
            skill_data[2] += correct
            skill_data[3] += 1

        yield user_id, _snapshot(state)


def _snapshot(state: Dict) -> Dict:
    accuracy = _ratio(state["correct"], state["answers"])
    score = _ratio(state["points"], state["max"])

    skills = []
    for name, data in state["skills"].items():
        skills.append(
            {
                "skill": name,
                "accuracy": round(_ratio(data[2], data[3]) * 100, 1),
                "score": round(_ratio(data[0], data[1]) * 100, 1),
            }
        )

    skills.sort(key=lambda s: (s["accuracy"], s["score"]))

    return {
        "accuracy": round(accuracy * 100, 1),
        "score": round(score * 100, 1),
        "skills": tuple(skills),
        "spread": _spread_index(skills),
    }


def merge_user_snapshots(stream: Iterable[Tuple[str, Dict]]) -> Dict[str, Dict]:
    latest = {}

    for user_id, snapshot in stream:
        latest[user_id] = snapshot

    return latest


def rank_users(snapshots: Dict[str, Dict]) -> Tuple[str, ...]:
    return tuple(
        user
        for user, _ in sorted(
            snapshots.items(),
            key=lambda item: (-item[1]["score"], item[0]),
        )
    )


def weakest_skill(snapshot: Dict) -> str:
    if not snapshot["skills"]:
        return ""
    return snapshot["skills"][0]["skill"]


def strongest_skill(snapshot: Dict) -> str:
    if not snapshot["skills"]:
        return ""
    return snapshot["skills"][-1]["skill"]


def _spread_index(skills) -> float:
    if not skills:
        return 0.0

    values = [s["score"] for s in skills]
    avg = sum(values) / len(values)
    deviation = sum(abs(v - avg) for v in values) / len(values)

    return round(100 - deviation, 2)


def _ratio(a: int, b: int) -> float:
    return (a / b) if b else 0.0