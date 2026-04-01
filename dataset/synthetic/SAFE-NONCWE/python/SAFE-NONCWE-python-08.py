from datetime import datetime, timedelta


class AttendanceBook:
    def __init__(self):
        self._schedule = {}
        self._records = {}
        self._students = set()

    def register_session(self, course_id, session_id, start_at, end_at):
        self._schedule[(course_id, session_id)] = (start_at, end_at)

    def mark_presence(self, student_id, course_id, session_id, timestamp):
        key = (student_id, course_id, session_id)
        self._students.add(student_id)

        entry = self._records.get(key)
        if entry is None:
            self._records[key] = {
                "first_seen": timestamp,
                "last_seen": timestamp,
                "events": 1,
            }
        else:
            if timestamp < entry["first_seen"]:
                entry["first_seen"] = timestamp
            if timestamp > entry["last_seen"]:
                entry["last_seen"] = timestamp
            entry["events"] += 1

    def evaluate(self):
        report = {}

        for (student_id, course_id, session_id), record in self._records.items():
            schedule_key = (course_id, session_id)
            if schedule_key not in self._schedule:
                continue

            start_at, end_at = self._schedule[schedule_key]
            duration = int((end_at - start_at).total_seconds() // 60)

            attended_minutes = self._compute_overlap(
                record["first_seen"], record["last_seen"], start_at, end_at
            )

            presence_ratio = attended_minutes / duration if duration else 0

            status = self._status_label(presence_ratio)

            student_bucket = report.setdefault(student_id, [])
            student_bucket.append(
                (
                    course_id,
                    session_id,
                    attended_minutes,
                    duration,
                    round(presence_ratio * 100, 1),
                    status,
                )
            )

        return report

    def student_summary(self, report, student_id):
        sessions = report.get(student_id, [])
        total_minutes = 0
        total_duration = 0
        missed = 0

        for entry in sessions:
            attended, duration = entry[2], entry[3]
            total_minutes += attended
            total_duration += duration
            if entry[5] == "absent":
                missed += 1

        ratio = (total_minutes / total_duration) if total_duration else 0

        return {
            "student": student_id,
            "attendance_percent": round(ratio * 100, 1),
            "sessions": len(sessions),
            "absent_sessions": missed,
        }

    def anomalies(self):
        issues = []

        for (student_id, course_id, session_id), record in self._records.items():
            if record["events"] == 1:
                issues.append(
                    (student_id, course_id, session_id, "single ping detected")
                )

            if record["last_seen"] - record["first_seen"] < timedelta(minutes=2):
                issues.append(
                    (student_id, course_id, session_id, "very short presence window")
                )

        return issues

    def _compute_overlap(self, a_start, a_end, b_start, b_end):
        latest_start = max(a_start, b_start)
        earliest_end = min(a_end, b_end)

        if latest_start >= earliest_end:
            return 0

        return int((earliest_end - latest_start).total_seconds() // 60)

    def _status_label(self, ratio):
        if ratio >= 0.75:
            return "present"
        if ratio >= 0.4:
            return "partial"
        return "absent"


def format_student_report(entries):
    lines = []

    for course_id, session_id, attended, duration, percent, status in entries:
        lines.append(
            f"{course_id}/{session_id}: {attended}/{duration} min "
            f"({percent}%) -> {status}"
        )

    return "\n".join(lines)


def merge_reports(base_report, extra_report):
    merged = dict(base_report)

    for student, sessions in extra_report.items():
        if student not in merged:
            merged[student] = list(sessions)
        else:
            merged[student].extend(sessions)

    return merged