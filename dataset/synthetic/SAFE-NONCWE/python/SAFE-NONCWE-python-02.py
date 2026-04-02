from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from statistics import mean


class ReorderPlanner:
    def __init__(self, service_level_buffer=0.15, review_period_days=7):
        self.service_level_buffer = Decimal(str(service_level_buffer))
        self.review_period_days = int(review_period_days)

    def build_plan(self, items, inbound_shipments):
        inbound_by_sku = self._group_inbound(inbound_shipments)
        result = []

        for item in items:
            sku = item["sku"]
            demand_profile = self._summarize_demand(item["daily_demand"])
            incoming = inbound_by_sku.get(sku, [])

            available_now = int(item["on_hand"]) - int(item.get("reserved", 0))
            inbound_soon = self._units_arriving_within(incoming, item["supplier_lead_days"])
            projected_available = available_now + inbound_soon

            reorder_point = self._reorder_point(
                avg_daily=demand_profile["average"],
                variability=demand_profile["variability"],
                lead_days=item["supplier_lead_days"],
            )

            target_level = self._target_stock_level(
                avg_daily=demand_profile["average"],
                variability=demand_profile["variability"],
                lead_days=item["supplier_lead_days"],
            )

            shortage = max(0, target_level - projected_available)
            suggested_order = self._round_to_pack(shortage, item["pack_size"])

            urgency = self._urgency_label(
                projected_available=projected_available,
                reorder_point=reorder_point,
                days_cover=self._days_of_cover(projected_available, demand_profile["average"]),
            )

            result.append(
                {
                    "sku": sku,
                    "name": item["name"],
                    "category": item["category"],
                    "supplier": item["supplier"],
                    "available_now": available_now,
                    "inbound_within_lead_time": inbound_soon,
                    "projected_available": projected_available,
                    "average_daily_demand": self._quantize(demand_profile["average"]),
                    "demand_variability": self._quantize(demand_profile["variability"]),
                    "reorder_point": reorder_point,
                    "target_level": target_level,
                    "suggested_order_units": suggested_order,
                    "suggested_order_packs": suggested_order // item["pack_size"] if item["pack_size"] else 0,
                    "urgency": urgency,
                    "notes": self._notes(item, projected_available, reorder_point, incoming),
                }
            )

        return sorted(
            result,
            key=lambda row: (
                self._urgency_rank(row["urgency"]),
                -row["suggested_order_units"],
                row["sku"],
            ),
        )

    def category_summary(self, plan_rows):
        grouped = defaultdict(lambda: {"items": 0, "units_to_order": 0, "critical": 0})

        for row in plan_rows:
            bucket = grouped[row["category"]]
            bucket["items"] += 1
            bucket["units_to_order"] += row["suggested_order_units"]
            if row["urgency"] == "critical":
                bucket["critical"] += 1

        summary = []
        for category, values in sorted(grouped.items()):
            summary.append(
                {
                    "category": category,
                    "items": values["items"],
                    "units_to_order": values["units_to_order"],
                    "critical_items": values["critical"],
                }
            )
        return summary

    def render_text_table(self, plan_rows):
        if not plan_rows:
            return "No items to review."

        headers = [
            "SKU",
            "Name",
            "Avail",
            "ROP",
            "Target",
            "Order",
            "Urgency",
            "Supplier",
        ]

        rows = []
        for row in plan_rows:
            rows.append(
                [
                    row["sku"],
                    row["name"],
                    str(row["projected_available"]),
                    str(row["reorder_point"]),
                    str(row["target_level"]),
                    str(row["suggested_order_units"]),
                    row["urgency"],
                    row["supplier"],
                ]
            )

        widths = []
        for col_index, header in enumerate(headers):
            widths.append(
                max(len(header), max(len(line[col_index]) for line in rows))
            )

        parts = []
        parts.append(self._render_line(headers, widths))
        parts.append(self._render_separator(widths))
        for row in rows:
            parts.append(self._render_line(row, widths))
        return "\n".join(parts)

    def _group_inbound(self, inbound_shipments):
        grouped = defaultdict(list)
        for shipment in inbound_shipments:
            grouped[shipment["sku"]].append(shipment)
        return grouped

    def _summarize_demand(self, daily_demand):
        if not daily_demand:
            return {"average": Decimal("0"), "variability": Decimal("0")}

        numbers = [Decimal(str(value)) for value in daily_demand]
        avg = Decimal(str(mean([float(v) for v in numbers])))

        spread = Decimal("0")
        if len(numbers) > 1:
            high = max(numbers)
            low = min(numbers)
            spread = (high - low) / Decimal("2")

        return {
            "average": avg,
            "variability": spread,
        }

    def _reorder_point(self, avg_daily, variability, lead_days):
        baseline = avg_daily * Decimal(str(lead_days))
        buffer_units = variability * Decimal("1.5")
        service_units = baseline * self.service_level_buffer
        total = baseline + buffer_units + service_units
        return int(total.to_integral_value(rounding=ROUND_HALF_UP))

    def _target_stock_level(self, avg_daily, variability, lead_days):
        coverage_days = Decimal(str(lead_days + self.review_period_days))
        baseline = avg_daily * coverage_days
        extra = variability * Decimal("2")
        service_units = baseline * self.service_level_buffer
        total = baseline + extra + service_units
        return int(total.to_integral_value(rounding=ROUND_HALF_UP))

    def _units_arriving_within(self, inbound_shipments, lead_days):
        units = 0
        for shipment in inbound_shipments:
            if int(shipment["arrives_in_days"]) <= int(lead_days):
                units += int(shipment["units"])
        return units

    def _round_to_pack(self, units, pack_size):
        if units <= 0:
            return 0
        if pack_size <= 1:
            return int(units)

        full_packs, remainder = divmod(int(units), int(pack_size))
        if remainder:
            full_packs += 1
        return full_packs * int(pack_size)

    def _days_of_cover(self, projected_available, avg_daily):
        if avg_daily <= 0:
            return None
        value = Decimal(str(projected_available)) / avg_daily
        return value.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

    def _urgency_label(self, projected_available, reorder_point, days_cover):
        if projected_available <= 0:
            return "critical"
        if projected_available < reorder_point * 0.5:
            return "critical"
        if projected_available < reorder_point:
            return "high"
        if days_cover is not None and days_cover < Decimal("10"):
            return "medium"
        return "normal"

    def _urgency_rank(self, label):
        ranks = {
            "critical": 0,
            "high": 1,
            "medium": 2,
            "normal": 3,
        }
        return ranks.get(label, 9)

    def _notes(self, item, projected_available, reorder_point, incoming):
        messages = []

        if projected_available < reorder_point:
            messages.append("below reorder threshold")

        if not incoming:
            messages.append("no inbound supply")

        if item["supplier_lead_days"] >= 21:
            messages.append("long supplier lead time")

        if item.get("seasonal"):
            messages.append("seasonal demand pattern")

        return ", ".join(messages) if messages else "stable"

    def _quantize(self, number):
        return str(number.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))

    def _render_line(self, values, widths):
        padded = []
        for value, width in zip(values, widths):
            padded.append(value.ljust(width))
        return " | ".join(padded)

    def _render_separator(self, widths):
        return "-+-".join("-" * width for width in widths)


inventory_items = [
    {
        "sku": "BR-1001",
        "name": "Blue Roller Pen",
        "category": "stationery",
        "supplier": "North Office Supply",
        "on_hand": 180,
        "reserved": 35,
        "pack_size": 24,
        "supplier_lead_days": 8,
        "seasonal": False,
        "daily_demand": [12, 14, 10, 13, 15, 11, 12, 14, 16, 10],
    },
    {
        "sku": "NT-2104",
        "name": "A5 Lined Notebook",
        "category": "paper_goods",
        "supplier": "Metro Paper Group",
        "on_hand": 95,
        "reserved": 22,
        "pack_size": 20,
        "supplier_lead_days": 14,
        "seasonal": True,
        "daily_demand": [9, 11, 8, 13, 15, 12, 10, 14, 16, 11],
    },
    {
        "sku": "MK-4402",
        "name": "Whiteboard Marker Set",
        "category": "stationery",
        "supplier": "North Office Supply",
        "on_hand": 34,
        "reserved": 8,
        "pack_size": 10,
        "supplier_lead_days": 10,
        "seasonal": False,
        "daily_demand": [4, 5, 3, 6, 7, 4, 5, 5, 6, 4],
    },
    {
        "sku": "CH-0090",
        "name": "Desk Chair Wheels",
        "category": "maintenance",
        "supplier": "Facility Parts Hub",
        "on_hand": 12,
        "reserved": 4,
        "pack_size": 4,
        "supplier_lead_days": 28,
        "seasonal": False,
        "daily_demand": [1, 0, 2, 1, 1, 0, 1, 2, 1, 1],
    },
    {
        "sku": "CB-7781",
        "name": "Cable Organizer Box",
        "category": "electronics_accessories",
        "supplier": "CableWorks Distribution",
        "on_hand": 61,
        "reserved": 5,
        "pack_size": 12,
        "supplier_lead_days": 6,
        "seasonal": False,
        "daily_demand": [6, 7, 5, 4, 8, 6, 7, 5, 6, 7],
    },
]

inbound_shipments = [
    {"sku": "BR-1001", "units": 48, "arrives_in_days": 5},
    {"sku": "NT-2104", "units": 40, "arrives_in_days": 16},
    {"sku": "MK-4402", "units": 20, "arrives_in_days": 9},
    {"sku": "CB-7781", "units": 24, "arrives_in_days": 3},
]

planner = ReorderPlanner(service_level_buffer=0.18, review_period_days=9)
plan = planner.build_plan(inventory_items, inbound_shipments)
category_overview = planner.category_summary(plan)
report_text = planner.render_text_table(plan)