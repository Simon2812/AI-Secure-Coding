from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple


@dataclass(frozen=True)
class Event:
    at: datetime
    kind: str  # "created", "assigned", "first_response", "status_change", "resolved"
    actor: str
    meta: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    customer: str
    priority: str  # "low", "medium", "high", "urgent"
    channel: str   # "email", "chat", "phone"
    events: Tuple[Event, ...]


@dataclass(frozen=True)
class TicketMetrics:
    ticket_id: str
    priority: str
    first_response_minutes: Optional[int]
    resolution_minutes: Optional[int]
    first_response_breached: bool
    resolution_breached: bool
    final_status: str
    owner: Optional[str]


class BusinessHours:
    def __init__(self, start_hour: int = 9, end_hour: int = 18, working_days: Tuple[int, ...] = (0, 1, 2, 3, 4)):
        self.start_hour = start_hour
        self.end_hour = end_hour
        self.working_days = set(working_days)

    def is_working_time(self, dt: datetime) -> bool:
        return dt.weekday() in self.working_days and self.start_hour <= dt.hour < self.end_hour

    def next_working_time(self, dt: datetime) -> datetime:
        cursor = dt
        while True:
            if cursor.weekday() not in self.working_days:
                cursor = (cursor + timedelta(days=1)).replace(hour=self.start_hour, minute=0, second=0, microsecond=0)
                continue
            if cursor.hour < self.start_hour:
                return cursor.replace(hour=self.start_hour, minute=0, second=0, microsecond=0)
            if cursor.hour >= self.end_hour:
                cursor = (cursor + timedelta(days=1)).replace(hour=self.start_hour, minute=0, second=0, microsecond=0)
                continue
            return cursor

    def working_minutes_between(self, start: datetime, end: datetime) -> int:
        if end <= start:
            return 0

        cursor = self.next_working_time(start)
        total = 0

        while cursor < end:
            if self.is_working_time(cursor):
                next_point = min(
                    end,
                    cursor.replace(hour=self.end_hour, minute=0, second=0, microsecond=0),
                )
                total += int((next_point - cursor).total_seconds() // 60)
                cursor = next_point
            else:
                cursor = self.next_working_time(cursor + timedelta(minutes=1))

        return total


class SlaPolicy:
    def __init__(self):
        # minutes
        self.first_response_targets = {
            "low": 8 * 60,
            "medium": 4 * 60,
            "high": 2 * 60,
            "urgent": 30,
        }
        self.resolution_targets = {
            "low": 5 * 24 * 60,
            "medium": 3 * 24 * 60,
            "high": 24 * 60,
            "urgent": 8 * 60,
        }

    def first_response_target(self, priority: str) -> int:
        return self.first_response_targets.get(priority, 4 * 60)

    def resolution_target(self, priority: str) -> int:
        return self.resolution_targets.get(priority, 3 * 24 * 60)


class SlaTracker:
    def __init__(self, calendar: BusinessHours, policy: SlaPolicy):
        self.calendar = calendar
        self.policy = policy

    def analyze(self, tickets: List[Ticket]) -> Dict[str, object]:
        per_ticket: List[TicketMetrics] = []
        by_priority = {}

        for ticket in tickets:
            metrics = self._analyze_ticket(ticket)
            per_ticket.append(metrics)

            bucket = by_priority.setdefault(
                ticket.priority,
                {
                    "count": 0,
                    "first_response_breaches": 0,
                    "resolution_breaches": 0,
                },
            )

            bucket["count"] += 1
            if metrics.first_response_breached:
                bucket["first_response_breaches"] += 1
            if metrics.resolution_breached:
                bucket["resolution_breaches"] += 1

        summary = {
            "tickets": len(per_ticket),
            "by_priority": by_priority,
            "breach_rate_first_response": self._rate(
                sum(1 for m in per_ticket if m.first_response_breached),
                len(per_ticket),
            ),
            "breach_rate_resolution": self._rate(
                sum(1 for m in per_ticket if m.resolution_breached),
                len(per_ticket),
            ),
        }

        return {"tickets": per_ticket, "summary": summary}

    def _analyze_ticket(self, ticket: Ticket) -> TicketMetrics:
        events = sorted(ticket.events, key=lambda e: e.at)

        created = self._first(events, "created")
        first_response = self._first(events, "first_response")
        resolved = self._last(events, "resolved")

        owner = self._current_owner(events)
        final_status = self._final_status(events)

        first_response_minutes = None
        resolution_minutes = None

        if created and first_response:
            first_response_minutes = self.calendar.working_minutes_between(
                created.at, first_response.at
            )

        if created and resolved:
            resolution_minutes = self.calendar.working_minutes_between(
                created.at, resolved.at
            )

        fr_target = self.policy.first_response_target(ticket.priority)
        res_target = self.policy.resolution_target(ticket.priority)

        return TicketMetrics(
            ticket_id=ticket.ticket_id,
            priority=ticket.priority,
            first_response_minutes=first_response_minutes,
            resolution_minutes=resolution_minutes,
            first_response_breached=(
                first_response_minutes is not None and first_response_minutes > fr_target
            ),
            resolution_breached=(
                resolution_minutes is not None and resolution_minutes > res_target
            ),
            final_status=final_status,
            owner=owner,
        )

    def _first(self, events: List[Event], kind: str) -> Optional[Event]:
        for e in events:
            if e.kind == kind:
                return e
        return None

    def _last(self, events: List[Event], kind: str) -> Optional[Event]:
        for e in reversed(events):
            if e.kind == kind:
                return e
        return None

    def _current_owner(self, events: List[Event]) -> Optional[str]:
        owner = None
        for e in events:
            if e.kind == "assigned":
                owner = e.meta.get("to")
        return owner

    def _final_status(self, events: List[Event]) -> str:
        status = "open"
        for e in events:
            if e.kind == "status_change":
                status = e.meta.get("status", status)
        return status

    def _rate(self, part: int, total: int) -> float:
        if total == 0:
            return 0.0
        return round((part / total) * 100, 1)


def make_event(ts: str, kind: str, actor: str, **meta) -> Event:
    return Event(
        at=datetime.strptime(ts, "%Y-%m-%d %H:%M"),
        kind=kind,
        actor=actor,
        meta={k: str(v) for k, v in meta.items()},
    )


tickets_data = [
    Ticket(
        ticket_id="T-1001",
        customer="Acme Ltd",
        priority="high",
        channel="email",
        events=(
            make_event("2026-04-08 08:40", "created", "system"),
            make_event("2026-04-08 09:10", "assigned", "dispatcher", to="Dana"),
            make_event("2026-04-08 10:05", "first_response", "Dana"),
            make_event("2026-04-08 15:30", "status_change", "Dana", status="in_progress"),
            make_event("2026-04-09 11:15", "resolved", "Dana"),
        ),
    ),
    Ticket(
        ticket_id="T-1002",
        customer="Beta Corp",
        priority="urgent",
        channel="chat",
        events=(
            make_event("2026-04-08 17:50", "created", "system"),
            make_event("2026-04-09 09:05", "assigned", "dispatcher", to="Roi"),
            make_event("2026-04-09 09:40", "first_response", "Roi"),
            make_event("2026-04-09 12:20", "resolved", "Roi"),
        ),
    ),
    Ticket(
        ticket_id="T-1003",
        customer="Gamma Inc",
        priority="medium",
        channel="phone",
        events=(
            make_event("2026-04-07 14:10", "created", "system"),
            make_event("2026-04-07 15:00", "assigned", "dispatcher", to="Noa"),
            make_event("2026-04-08 11:30", "first_response", "Noa"),
            make_event("2026-04-10 10:00", "resolved", "Noa"),
        ),
    ),
]

calendar = BusinessHours(start_hour=9, end_hour=18)
policy = SlaPolicy()
tracker = SlaTracker(calendar, policy)

sla_report = tracker.analyze(tickets_data)