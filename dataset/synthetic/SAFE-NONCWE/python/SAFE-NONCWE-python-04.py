from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass(frozen=True)
class Shift:
    employee_id: str
    employee_name: str
    team: str
    start_at: datetime
    end_at: datetime
    role: str

    def duration_minutes(self) -> int:
        return int((self.end_at - self.start_at).total_seconds() // 60)


@dataclass(frozen=True)
class Conflict:
    employee_id: str
    employee_name: str
    category: str
    details: str
    related: Tuple[Shift, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class DailyLoad:
    employee_id: str
    employee_name: str
    total_minutes: int
    shift_count: int


class ScheduleAudit:
    def __init__(
        self,
        min_rest_hours: int = 10,
        max_daily_minutes: int = 12 * 60,
        max_consecutive_days: int = 6,
    ) -> None:
        self.min_rest = timedelta(hours=min_rest_hours)
        self.max_daily_minutes = max_daily_minutes
        self.max_consecutive_days = max_consecutive_days

    def analyze(self, shifts: Iterable[Shift]) -> Dict[str, object]:
        ordered = sorted(
            list(shifts),
            key=lambda item: (item.employee_id, item.start_at, item.end_at),
        )

        grouped = self._group_by_employee(ordered)

        conflicts: List[Conflict] = []
        daily_load: List[DailyLoad] = []

        for employee_shifts in grouped.values():
            conflicts.extend(self._find_overlaps(employee_shifts))
            conflicts.extend(self._find_short_rest(employee_shifts))
            conflicts.extend(self._find_long_days(employee_shifts))
            conflicts.extend(self._find_excessive_streaks(employee_shifts))
            daily_load.extend(self._build_daily_load(employee_shifts))

        summary = self._build_summary(conflicts, daily_load)
        return {
            "summary": summary,
            "conflicts": conflicts,
            "daily_load": daily_load,
        }

    def _group_by_employee(self, shifts: List[Shift]) -> Dict[str, List[Shift]]:
        grouped: Dict[str, List[Shift]] = {}
        for item in shifts:
            grouped.setdefault(item.employee_id, []).append(item)
        return grouped

    def _find_overlaps(self, shifts: List[Shift]) -> List[Conflict]:
        conflicts: List[Conflict] = []

        for index in range(len(shifts) - 1):
            current = shifts[index]
            following = shifts[index + 1]

            if following.start_at < current.end_at:
                details = (
                    f"Overlapping shifts: "
                    f"{current.start_at:%Y-%m-%d %H:%M}–{current.end_at:%H:%M} "
                    f"and {following.start_at:%Y-%m-%d %H:%M}–{following.end_at:%H:%M}"
                )
                conflicts.append(
                    Conflict(
                        employee_id=current.employee_id,
                        employee_name=current.employee_name,
                        category="overlap",
                        details=details,
                        related=(current, following),
                    )
                )

        return conflicts

    def _find_short_rest(self, shifts: List[Shift]) -> List[Conflict]:
        conflicts: List[Conflict] = []

        for index in range(len(shifts) - 1):
            current = shifts[index]
            following = shifts[index + 1]

            if following.start_at < current.end_at:
                continue

            gap = following.start_at - current.end_at
            if gap < self.min_rest:
                details = (
                    f"Insufficient rest between shifts: "
                    f"{gap.total_seconds() / 3600:.1f} hours, "
                    f"minimum required is {self.min_rest.total_seconds() / 3600:.1f}."
                )
                conflicts.append(
                    Conflict(
                        employee_id=current.employee_id,
                        employee_name=current.employee_name,
                        category="short_rest",
                        details=details,
                        related=(current, following),
                    )
                )

        return conflicts

    def _find_long_days(self, shifts: List[Shift]) -> List[Conflict]:
        minutes_by_day: Dict[datetime.date, List[Shift]] = {}

        for item in shifts:
            day = item.start_at.date()
            minutes_by_day.setdefault(day, []).append(item)

        conflicts: List[Conflict] = []

        for day, entries in minutes_by_day.items():
            total_minutes = sum(shift.duration_minutes() for shift in entries)
            if total_minutes > self.max_daily_minutes:
                details = (
                    f"Scheduled for {total_minutes // 60}h {total_minutes % 60:02d}m "
                    f"on {day.isoformat()}, exceeding the allowed "
                    f"{self.max_daily_minutes // 60}h {self.max_daily_minutes % 60:02d}m."
                )
                conflicts.append(
                    Conflict(
                        employee_id=entries[0].employee_id,
                        employee_name=entries[0].employee_name,
                        category="long_day",
                        details=details,
                        related=tuple(sorted(entries, key=lambda s: s.start_at)),
                    )
                )

        return conflicts

    def _find_excessive_streaks(self, shifts: List[Shift]) -> List[Conflict]:
        worked_days = sorted({item.start_at.date() for item in shifts})
        if not worked_days:
            return []

        streak_start = worked_days[0]
        previous_day = worked_days[0]
        current_streak = [worked_days[0]]

        streaks: List[List[datetime.date]] = []

        for current_day in worked_days[1:]:
            if current_day == previous_day + timedelta(days=1):
                current_streak.append(current_day)
            else:
                streaks.append(current_streak)
                current_streak = [current_day]
            previous_day = current_day

        streaks.append(current_streak)

        conflicts: List[Conflict] = []
        shifts_by_day: Dict[datetime.date, List[Shift]] = {}
        for item in shifts:
            shifts_by_day.setdefault(item.start_at.date(), []).append(item)

        for streak in streaks:
            if len(streak) > self.max_consecutive_days:
                related_shifts: List[Shift] = []
                for day in streak:
                    related_shifts.extend(shifts_by_day.get(day, []))

                first_shift = related_shifts[0]
                details = (
                    f"Worked {len(streak)} consecutive days from "
                    f"{streak[0].isoformat()} to {streak[-1].isoformat()}."
                )
                conflicts.append(
                    Conflict(
                        employee_id=first_shift.employee_id,
                        employee_name=first_shift.employee_name,
                        category="consecutive_days",
                        details=details,
                        related=tuple(sorted(related_shifts, key=lambda s: s.start_at)),
                    )
                )

        return conflicts

    def _build_daily_load(self, shifts: List[Shift]) -> List[DailyLoad]:
        grouped: Dict[datetime.date, List[Shift]] = {}
        for item in shifts:
            grouped.setdefault(item.start_at.date(), []).append(item)

        result: List[DailyLoad] = []
        for day in sorted(grouped):
            entries = grouped[day]
            result.append(
                DailyLoad(
                    employee_id=entries[0].employee_id,
                    employee_name=entries[0].employee_name,
                    total_minutes=sum(shift.duration_minutes() for shift in entries),
                    shift_count=len(entries),
                )
            )
        return result

    def _build_summary(
        self,
        conflicts: List[Conflict],
        daily_load: List[DailyLoad],
    ) -> Dict[str, object]:
        by_category: Dict[str, int] = {}
        for item in conflicts:
            by_category[item.category] = by_category.get(item.category, 0) + 1

        heaviest_day: Optional[DailyLoad] = None
        for item in daily_load:
            if heaviest_day is None or item.total_minutes > heaviest_day.total_minutes:
                heaviest_day = item

        return {
            "conflict_count": len(conflicts),
            "by_category": dict(sorted(by_category.items())),
            "employees_checked": len({item.employee_id for item in daily_load}),
            "heaviest_day": heaviest_day,
        }


def make_shift(
    employee_id: str,
    employee_name: str,
    team: str,
    start_at: str,
    end_at: str,
    role: str,
) -> Shift:
    start_value = datetime.strptime(start_at, "%Y-%m-%d %H:%M")
    end_value = datetime.strptime(end_at, "%Y-%m-%d %H:%M")
    if end_value <= start_value:
        raise ValueError(f"Shift end must be after start for {employee_name}.")
    return Shift(
        employee_id=employee_id,
        employee_name=employee_name,
        team=team,
        start_at=start_value,
        end_at=end_value,
        role=role,
    )


def render_conflict_report(conflicts: Iterable[Conflict]) -> str:
    rows: List[str] = []
    for item in conflicts:
        rows.append(f"[{item.category}] {item.employee_name} ({item.employee_id})")
        rows.append(f"  {item.details}")
        if item.related:
            for shift in item.related:
                rows.append(
                    "  - "
                    f"{shift.start_at:%Y-%m-%d %H:%M} to {shift.end_at:%H:%M} "
                    f"| {shift.team} | {shift.role}"
                )
    return "\n".join(rows)


def sample_week() -> List[Shift]:
    return [
        make_shift("E-104", "Maya Cohen", "Support", "2026-04-06 08:00", "2026-04-06 16:00", "Agent"),
        make_shift("E-104", "Maya Cohen", "Support", "2026-04-06 15:00", "2026-04-06 20:00", "Escalation"),
        make_shift("E-104", "Maya Cohen", "Support", "2026-04-07 05:30", "2026-04-07 12:00", "Agent"),
        make_shift("E-104", "Maya Cohen", "Support", "2026-04-08 08:00", "2026-04-08 18:30", "Agent"),
        make_shift("E-104", "Maya Cohen", "Support", "2026-04-09 08:00", "2026-04-09 18:30", "Agent"),
        make_shift("E-104", "Maya Cohen", "Support", "2026-04-10 08:00", "2026-04-10 18:30", "Agent"),
        make_shift("E-104", "Maya Cohen", "Support", "2026-04-11 08:00", "2026-04-11 18:30", "Agent"),
        make_shift("E-104", "Maya Cohen", "Support", "2026-04-12 08:00", "2026-04-12 18:30", "Agent"),
        make_shift("E-104", "Maya Cohen", "Support", "2026-04-13 08:00", "2026-04-13 18:30", "Agent"),
        make_shift("E-205", "Daniel Levi", "Fulfillment", "2026-04-06 09:00", "2026-04-06 17:00", "Picker"),
        make_shift("E-205", "Daniel Levi", "Fulfillment", "2026-04-07 09:00", "2026-04-07 17:00", "Picker"),
        make_shift("E-205", "Daniel Levi", "Fulfillment", "2026-04-08 09:00", "2026-04-08 17:00", "Picker"),
        make_shift("E-311", "Rina Azulay", "Front Desk", "2026-04-06 07:00", "2026-04-06 13:00", "Reception"),
        make_shift("E-311", "Rina Azulay", "Front Desk", "2026-04-06 14:00", "2026-04-06 20:00", "Reception"),
    ]