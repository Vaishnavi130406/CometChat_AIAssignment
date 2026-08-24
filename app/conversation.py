from typing import List, Dict, Optional
import re


class ConversationMemory:
    """Stores relevant conversation context for the current session."""

    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self.messages: List[Dict[str, str]] = []
        self.last_order_id: Optional[str] = None

    def add_user_message(self, content: str):
        """Add a user message and remember an order ID if present."""

        self.messages.append({
            "role": "user",
            "content": content
        })

        order_id = self.extract_order_id(content)

        if order_id:
            self.last_order_id = order_id

        self._trim_history()

    def add_assistant_message(self, content: str):
        """Add an assistant message."""
        self.messages.append({
            "role": "assistant",
            "content": content
        })

        self._trim_history()

    def get_messages(self) -> List[Dict[str, str]]:
        """Return conversation history."""
        return list(self.messages)

    def get_last_order_id(self) -> Optional[str]:
        """Return the most recently mentioned order ID."""
        return self.last_order_id

    def clear(self):
        """Clear the current conversation session."""
        self.messages.clear()
        self.last_order_id = None

    def _trim_history(self):
        """Keep only the most recent messages."""
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    @staticmethod
    def extract_order_id(content: str) -> Optional[str]:
        """Extract and normalize an order ID from text."""

        match = re.search(
            r"\bORD[\s\-_]?(\d{4})\b",
            content,
            re.IGNORECASE,
        )

        if not match:
            return None

        return f"ORD-{match.group(1)}"