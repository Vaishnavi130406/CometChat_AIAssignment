from app.conversation import ConversationMemory


def test_messages_are_stored():
    memory = ConversationMemory()

    memory.add_user_message("Where is ORD-1007?")
    memory.add_assistant_message("Your order has shipped.")

    messages = memory.get_messages()

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"


def test_conversation_order_is_preserved():
    memory = ConversationMemory()

    memory.add_user_message("Do you ship internationally?")
    memory.add_assistant_message("Yes.")
    memory.add_user_message("What about Canada?")

    messages = memory.get_messages()

    assert messages[0]["content"] == "Do you ship internationally?"
    assert messages[2]["content"] == "What about Canada?"


def test_history_is_limited():
    memory = ConversationMemory(max_messages=2)

    memory.add_user_message("Message 1")
    memory.add_assistant_message("Message 2")
    memory.add_user_message("Message 3")

    messages = memory.get_messages()

    assert len(messages) == 2
    assert messages[0]["content"] == "Message 2"
    assert messages[1]["content"] == "Message 3"


def test_clear_removes_history():
    memory = ConversationMemory()

    memory.add_user_message("Hello")
    memory.clear()

    assert memory.get_messages() == []