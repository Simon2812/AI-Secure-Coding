from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Optional


def money(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@dataclass
class LineItem:
    sku: str
    description: str
    quantity: int
    unit_price: Decimal
    category: str
    discount_percent: Decimal = Decimal("0")


@dataclass
class PricingRule:
    category: str
    bulk_threshold: int
    bulk_discount_percent: Decimal


class InvoiceCalculator:
    def __init__(
        self,
        vat_percent: Decimal,
        category_rules: List[PricingRule],
        global_discount_percent: Decimal = Decimal("0"),
    ):
        self.vat_percent = vat_percent
        self.category_rules = {rule.category: rule for rule in category_rules}
        self.global_discount_percent = global_discount_percent

    def calculate(self, items: List[LineItem]) -> Dict[str, object]:
        processed_lines = []
        subtotal = Decimal("0")
        total_discount = Decimal("0")

        for item in items:
            line = self._process_line(item)
            subtotal += line["gross"]
            total_discount += line["discount_value"]
            processed_lines.append(line)

        subtotal = money(subtotal)
        total_discount = money(total_discount)

        discounted_subtotal = money(subtotal - total_discount)

        global_discount_value = money(
            discounted_subtotal * self.global_discount_percent / Decimal("100")
        )

        net_after_all_discounts = money(discounted_subtotal - global_discount_value)

        vat_amount = money(net_after_all_discounts * self.vat_percent / Decimal("100"))
        total_due = money(net_after_all_discounts + vat_amount)

        return {
            "lines": processed_lines,
            "summary": {
                "subtotal": subtotal,
                "line_discounts": total_discount,
                "global_discount": global_discount_value,
                "net_before_vat": net_after_all_discounts,
                "vat_percent": self.vat_percent,
                "vat_amount": vat_amount,
                "total_due": total_due,
            },
        }

    def _process_line(self, item: LineItem) -> Dict[str, object]:
        base = Decimal(item.quantity) * item.unit_price

        category_discount = self._category_discount(item)
        item_discount = item.discount_percent

        effective_discount = max(category_discount, item_discount)

        discount_value = money(base * effective_discount / Decimal("100"))
        net = money(base - discount_value)

        return {
            "sku": item.sku,
            "description": item.description,
            "quantity": item.quantity,
            "unit_price": money(item.unit_price),
            "gross": money(base),
            "discount_percent": effective_discount,
            "discount_value": discount_value,
            "net": net,
        }

    def _category_discount(self, item: LineItem) -> Decimal:
        rule: Optional[PricingRule] = self.category_rules.get(item.category)
        if not rule:
            return Decimal("0")

        if item.quantity >= rule.bulk_threshold:
            return rule.bulk_discount_percent

        return Decimal("0")


class InvoiceRenderer:
    def render(self, invoice: Dict[str, object]) -> str:
        lines = invoice["lines"]
        summary = invoice["summary"]

        output = []
        output.append("INVOICE")
        output.append("-" * 50)

        for line in lines:
            output.append(
                f"{line['sku']} | {line['description']} | "
                f"{line['quantity']} x {line['unit_price']} = {line['gross']}"
            )
            if line["discount_value"] > 0:
                output.append(
                    f"  discount {line['discount_percent']}% -> -{line['discount_value']}"
                )
            output.append(f"  net: {line['net']}")

        output.append("-" * 50)
        output.append(f"Subtotal: {summary['subtotal']}")
        output.append(f"Line discounts: -{summary['line_discounts']}")
        output.append(f"Global discount: -{summary['global_discount']}")
        output.append(f"Net before VAT: {summary['net_before_vat']}")
        output.append(
            f"VAT ({summary['vat_percent']}%): {summary['vat_amount']}"
        )
        output.append(f"TOTAL DUE: {summary['total_due']}")

        return "\n".join(output)


items = [
    LineItem(
        sku="PR-001",
        description="Premium Paper Pack",
        quantity=12,
        unit_price=Decimal("8.50"),
        category="paper",
        discount_percent=Decimal("5"),
    ),
    LineItem(
        sku="PN-100",
        description="Gel Ink Pen",
        quantity=30,
        unit_price=Decimal("1.20"),
        category="writing",
    ),
    LineItem(
        sku="FD-900",
        description="Office Folder Set",
        quantity=5,
        unit_price=Decimal("4.75"),
        category="paper",
    ),
]

rules = [
    PricingRule(category="paper", bulk_threshold=10, bulk_discount_percent=Decimal("7")),
    PricingRule(category="writing", bulk_threshold=25, bulk_discount_percent=Decimal("10")),
]

calculator = InvoiceCalculator(
    vat_percent=Decimal("17"),
    category_rules=rules,
    global_discount_percent=Decimal("3"),
)

invoice_data = calculator.calculate(items)
renderer = InvoiceRenderer()
invoice_text = renderer.render(invoice_data)