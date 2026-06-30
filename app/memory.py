# Simple in-memory conversation store.
# Key: conversation_id
# Value: list of messages

CONVERSATIONS = {}


def get_messages(conversation_id: str) -> list[dict]:
    return CONVERSATIONS.get(conversation_id, [])


def add_message(conversation_id: str, role: str, content: str) -> None:
    if conversation_id not in CONVERSATIONS:
        CONVERSATIONS[conversation_id] = []

    CONVERSATIONS[conversation_id].append({
        "role": role,
        "content": content
    })


def get_recent_messages(conversation_id: str, limit: int = 6) -> list[dict]:
    messages = get_messages(conversation_id)
    return messages[-limit:]


def clear_conversation(conversation_id: str) -> None:
    CONVERSATIONS.pop(conversation_id, None)