from dataclasses import dataclass
from datetime import datetime, timedelta, time
from typing import List, Dict, Tuple


@dataclass(frozen=True)
class Meeting:
    room: str
    title: str
    organizer: str
    start_at: datetime
    end_at: datetime
    attendees: int

    def duration_minutes(self) -> int:
        return int((self.end_at - self.start_at).total_seconds() // 60)


@dataclass(frozen=True)
class RoomStats:
    room: str
    total_minutes: int
    meeting_count: int
    utilization_percent: float
    peak_hour: str
    average_meeting_size: float


class UtilizationAnalyzer:
    def __init__(self, day_start: time, day_end: time):
        self.day_start = day_start
        self.day_end = day_end

    def analyze(self, meetings: List[Meeting]) -> Dict[str, object]:
        grouped = self._group_by_room(meetings)

        room_stats: List[RoomStats] = []
        gaps: Dict[str, List[Tuple[datetime, datetime]]] = {}

        for room, items in grouped.items():
            sorted_items = sorted(items, key=lambda m: m.start_at)

            total_minutes = sum(m.duration_minutes() for m in sorted_items)
            working_minutes = self._working_minutes_for_day(sorted_items)

            utilization = (
                (total_minutes / working_minutes) * 100 if working_minutes > 0 else 0
            )

            peak_hour = self._peak_hour(sorted_items)
            avg_size = (
                sum(m.attendees for m in sorted_items) / len(sorted_items)
                if sorted_items
                else 0
            )

            room_stats.append(
                RoomStats(
                    room=room,
                    total_minutes=total_minutes,
                    meeting_count=len(sorted_items),
                    utilization_percent=round(utilization, 1),
                    peak_hour=peak_hour,
                    average_meeting_size=round(avg_size, 1),
                )
            )

            gaps[room] = self._find_gaps(sorted_items)

        summary = self._summary(room_stats)

        return {
            "rooms": sorted(room_stats, key=lambda r: -r.utilization_percent),
            "gaps": gaps,
            "summary": summary,
        }

    def _group_by_room(self, meetings: List[Meeting]) -> Dict[str, List[Meeting]]:
        grouped: Dict[str, List[Meeting]] = {}
        for m in meetings:
            grouped.setdefault(m.room, []).append(m)
        return grouped

    def _working_minutes_for_day(self, meetings: List[Meeting]) -> int:
        if not meetings:
            return 0

        day = meetings[0].start_at.date()
        start_dt = datetime.combine(day, self.day_start)
        end_dt = datetime.combine(day, self.day_end)
        return int((end_dt - start_dt).total_seconds() // 60)

    def _peak_hour(self, meetings: List[Meeting]) -> str:
        hourly = {hour: 0 for hour in range(24)}

        for m in meetings:
            current = m.start_at
            while current < m.end_at:
                hourly[current.hour] += 1
                current += timedelta(minutes=30)

        peak = max(hourly.items(), key=lambda x: x[1])[0]
        return f"{peak:02d}:00"

    def _find_gaps(
        self, meetings: List[Meeting]
    ) -> List[Tuple[datetime, datetime]]:
        if not meetings:
            return []

        gaps = []
        sorted_items = sorted(meetings, key=lambda m: m.start_at)

        day = sorted_items[0].start_at.date()
        current_time = datetime.combine(day, self.day_start)

        for m in sorted_items:
            if m.start_at > current_time:
                gaps.append((current_time, m.start_at))
            current_time = max(current_time, m.end_at)

        end_of_day = datetime.combine(day, self.day_end)
        if current_time < end_of_day:
            gaps.append((current_time, end_of_day))

        return gaps

    def _summary(self, stats: List[RoomStats]) -> Dict[str, object]:
        if not stats:
            return {"rooms": 0}

        busiest = max(stats, key=lambda r: r.utilization_percent)
        least_used = min(stats, key=lambda r: r.utilization_percent)

        return {
            "rooms": len(stats),
            "average_utilization": round(
                sum(r.utilization_percent for r in stats) / len(stats), 1
            ),
            "busiest_room": busiest.room,
            "least_used_room": least_used.room,
        }


def create_meeting(
    room: str,
    title: str,
    organizer: str,
    start: str,
    end: str,
    attendees: int,
) -> Meeting:
    start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M")

    if end_dt <= start_dt:
        raise ValueError("Meeting end must be after start")

    return Meeting(
        room=room,
        title=title,
        organizer=organizer,
        start_at=start_dt,
        end_at=end_dt,
        attendees=attendees,
    )


meetings_data = [
    create_meeting("Room A", "Planning", "Dana", "2026-04-10 09:00", "2026-04-10 10:30", 6),
    create_meeting("Room A", "Sync", "Eli", "2026-04-10 11:00", "2026-04-10 12:00", 4),
    create_meeting("Room A", "Review", "Noa", "2026-04-10 14:00", "2026-04-10 15:30", 5),

    create_meeting("Room B", "Standup", "Lior", "2026-04-10 09:30", "2026-04-10 10:00", 8),
    create_meeting("Room B", "Workshop", "Maya", "2026-04-10 10:30", "2026-04-10 13:00", 12),
    create_meeting("Room B", "1:1", "Roi", "2026-04-10 15:00", "2026-04-10 15:30", 2),

    create_meeting("Room C", "Training", "Yael", "2026-04-10 08:30", "2026-04-10 11:30", 15),
]

analyzer = UtilizationAnalyzer(day_start=time(8, 0), day_end=time(18, 0))
analysis_result = analyzer.analyze(meetings_data)