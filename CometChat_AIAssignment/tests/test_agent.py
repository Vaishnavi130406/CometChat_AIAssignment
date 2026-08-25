import re
from typing import Dict, Any

from app.retriever import KnowledgeRetriever
from app.order_tool import OrderTool
from app.conversation import ConversationMemory


class SupportAgent:
    """
    Customer support agent for Aster & Row.

    The agent can:
    - Answer knowledge-base questions
    - Look up orders
    - Maintain conversation history
    - Avoid exposing internal order information
    - Hand off exception cases
    """

    def __init__(self):
        self.retriever = KnowledgeRetriever()
        self.order_tool = OrderTool()
        self.memory = ConversationMemory()

    def respond(self, user_message: str) -> Dict[str, Any]:
        """
        Process a customer message and return a structured response.
        """

        # Store user message
        self.memory.add_message(
            "user",
            user_message
        )

        # --------------------------------------------------
        # 1. Check whether this is an order question
        # --------------------------------------------------

        order_id = self._extract_order_id(user_message)

        if order_id:
            result = self._handle_order_question(order_id)

            self.memory.add_message(
                "assistant",
                result["answer"]
            )

            return result

        # --------------------------------------------------
        # 2. Otherwise search the knowledge base
        # --------------------------------------------------

        retrieved = self.retriever.search(
            user_message,
            top_k=3
        )

        if retrieved:
            result = self._answer_from_knowledge(
                user_message,
                retrieved
            )
        else:
            result = {
                "answer": (
                    "I don't have enough information in the "
                    "Aster & Row knowledge base to answer that "
                    "question accurately."
                ),
                "sources": [],
                "handoff": False,
            }

        # Store assistant response
        self.memory.add_message(
            "assistant",
            result["answer"]
        )

        return result

    # ======================================================
    # ORDER HANDLING
    # ======================================================

    def _extract_order_id(self, message: str):
        """
        Extract an order ID such as ORD-1007.
        """

        match = re.search(
            r"\bORD[-\s]?\d{4}\b",
            message,
            re.IGNORECASE
        )

        if not match:
            return None

        raw_order_id = match.group(0)

        # Normalize harmless formatting differences
        order_id = re.sub(
            r"[\s]",
            "",
            raw_order_id.upper()
        )

        order_id = order_id.replace(
            "ORD",
            "ORD-"
        )

        # Avoid ORD--1007
        order_id = order_id.replace(
            "ORD--",
            "ORD-"
        )

        return order_id

    def _handle_order_question(
        self,
        order_id: str
    ) -> Dict[str, Any]:
        """
        Handle an order lookup.

        Only customer-safe fields are used.
        Internal fields are never returned.
        """

        order = self.order_tool.get_order(order_id)

        # --------------------------------------------------
        # Order not found
        # --------------------------------------------------

        if order is None:
            return {
                "answer": (
                    f"I couldn't find an order matching "
                    f"{order_id}. Please check the order ID "
                    f"and try again."
                ),
                "sources": [],
                "handoff": False,
            }

        status = order.get("status")

        safe_message = order.get(
            "customer_safe_message",
            f"The order status is {status}."
        )

        # --------------------------------------------------
        # Cancelled
        # --------------------------------------------------

        if status == "cancelled":
            answer = (
                f"Order {order['order_id']}: "
                f"{safe_message}"
            )

            return {
                "answer": answer,
                "sources": ["orders.json"],
                "handoff": False,
            }

        # --------------------------------------------------
        # Returned
        # --------------------------------------------------

        if status == "returned":
            answer = (
                f"Order {order['order_id']}: "
                f"{safe_message}"
            )

            return {
                "answer": answer,
                "sources": ["orders.json"],
                "handoff": False,
            }

        # --------------------------------------------------
        # Exception
        # --------------------------------------------------

        if status == "exception":
            answer = (
                f"Order {order['order_id']}: "
                f"{safe_message} "
                f"Please contact customer support for "
                f"assistance."
            )

            return {
                "answer": answer,
                "sources": ["orders.json"],
                "handoff": True,
            }

        # --------------------------------------------------
        # Shipped
        # --------------------------------------------------

        if status == "shipped":
            answer = (
                f"Order {order['order_id']}: "
                f"{safe_message}"
            )

            return {
                "answer": answer,
                "sources": ["orders.json"],
                "handoff": False,
            }

        # --------------------------------------------------
        # Delivered
        # --------------------------------------------------

        if status == "delivered":
            answer = (
                f"Order {order['order_id']}: "
                f"{safe_message}"
            )

            return {
                "answer": answer,
                "sources": ["orders.json"],
                "handoff": False,
            }

        # --------------------------------------------------
        # Pending / processing / delayed
        # --------------------------------------------------

        answer = (
            f"Order {order['order_id']}: "
            f"{safe_message}"
        )

        return {
            "answer": answer,
            "sources": ["orders.json"],
            "handoff": False,
        }

    # ======================================================
    # KNOWLEDGE BASE
    # ======================================================

    def _answer_from_knowledge(
        self,
        user_message: str,
        retrieved
    ) -> Dict[str, Any]:
        """
        Generate a grounded answer from retrieved documents.

        This version intentionally does not call an external
        LLM, allowing the project to run without API credits.
        """

        top_document = retrieved[0]

        content = top_document["content"]
        source = top_document["source"]

        answer = self._extract_answer(
            user_message,
            content
        )

        if not answer:
            answer = (
                "I found relevant information in the "
                "Aster & Row knowledge base, but I don't "
                "have enough information to give a precise "
                "answer."
            )

        return {
            "answer": answer,
            "sources": [source],
            "handoff": False,
        }

    def _extract_answer(
        self,
        question: str,
        content: str
    ) -> str:
        """
        Extract useful customer-facing information from
        a retrieved Markdown section.
        """

        lines = [
            line.strip()
            for line in content.splitlines()
            if line.strip()
        ]

        # Remove Markdown heading markers
        clean_lines = []

        for line in lines:
            line = re.sub(
                r"^#{1,6}\s*",
                "",
                line
            )

            if line:
                clean_lines.append(line)

        # Look for bullet/list content first
        useful_lines = []

        for line in clean_lines:
            if line.startswith("-"):
                useful_lines.append(
                    line.lstrip("- ").strip()
                )

        if useful_lines:
            return " ".join(useful_lines[:4])

        # Otherwise use the first few descriptive lines
        descriptive_lines = []

        for line in clean_lines:
            lower = line.lower()

            if lower.startswith(
                (
                    "source:",
                    "document:",
                    "last updated:",
                    "owner:",
                    "status:",
                )
            ):
                continue

            descriptive_lines.append(line)

        if descriptive_lines:
            return " ".join(
                descriptive_lines[:3]
            )

        return ""