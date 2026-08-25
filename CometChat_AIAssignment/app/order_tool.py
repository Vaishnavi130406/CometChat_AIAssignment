import json
import re
from pathlib import Path
from typing import Optional, Dict, Any


class OrderTool:
    """Safe customer-facing order lookup tool."""

    def __init__(self, orders_path: str = "data/orders.json"):
        self.orders_path = Path(orders_path)
        self.snapshot_at = None
        self.orders = self._load_orders()

    def _load_orders(self):
        """Load the mock order dataset."""
        with self.orders_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        self.snapshot_at = data.get("snapshot_at")

        return data.get("orders", [])

    def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """
        Look up an order by ID.

        Harmless differences such as lowercase letters,
        surrounding whitespace, and ordinary punctuation are normalized.

        A substantially different order ID is never guessed.
        """

        normalized_id = self._normalize_order_id(order_id)

        if not normalized_id:
            return None

        for order in self.orders:
            if order.get("order_id") == normalized_id:
                return self._sanitize_order(order)

        return None

    @staticmethod
    def _normalize_order_id(order_id: str) -> Optional[str]:
        """Normalize harmless formatting differences."""

        if not order_id:
            return None

        normalized = order_id.strip().upper()

        # Remove ordinary punctuation and whitespace while preserving
        # the meaningful characters of the order ID.
        normalized = re.sub(r"[\s\-_/.:,]+", "", normalized)

        # Convert ORD1007 -> ORD-1007 for harmless formatting.
        match = re.fullmatch(r"ORD(\d{4})", normalized)

        if match:
            normalized = f"ORD-{match.group(1)}"

        # Already in canonical form.
        if re.fullmatch(r"ORD-\d{4}", normalized):
            return normalized

        return None

    def _sanitize_order(self, order: Dict[str, Any]) -> Dict[str, Any]:
        """
        Return only customer-safe information.

        Internal/customer-private data is deliberately excluded.
        """

        safe_order = {
            "order_id": order.get("order_id"),
            "membership_tier": order.get("membership_tier"),
            "placed_at": order.get("placed_at"),
            "status": order.get("status"),
            "status_updated_at": order.get("status_updated_at"),
            "shipped_at": order.get("shipped_at"),
            "delivered_at": order.get("delivered_at"),
            "carrier": order.get("carrier"),
            "tracking_number": order.get("tracking_number"),
            "estimated_delivery": order.get("estimated_delivery"),
            "customer_safe_message": order.get("customer_safe_message"),
        }

        # Only expose the allowed item fields.
        safe_order["items"] = []

        for item in order.get("items", []):
            safe_order["items"].append({
                "name": item.get("name"),
                "quantity": item.get("quantity"),
                "final_sale": item.get("final_sale"),
            })

        return safe_order