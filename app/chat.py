from app.llm import get_llm
from app.memory import add_message, get_recent_messages
from app.models import get_model_config


SYSTEM_PROMPT = "You are a helpful AI assistant. Answer clearly and practically."


def format_history(messages: list[dict]) -> str:
    if not messages:
        return "No previous conversation."

    formatted_messages = []

    for message in messages:
        role = message["role"]
        content = message["content"]

        if role == "user":
            formatted_messages.append(f"User: {content}")
        elif role == "assistant":
            formatted_messages.append(f"Assistant: {content}")

    return "\n".join(formatted_messages)


def build_prompt(model_key: str, user_message: str, conversation_id: str) -> str:
    model_config = get_model_config(model_key)
    prompt_style = model_config["prompt_style"]

    recent_messages = get_recent_messages(conversation_id, limit=6)
    history_text = format_history(recent_messages)

    if prompt_style == "llama":
        return build_llama_prompt(user_message, history_text)

    if prompt_style == "granite":
        return build_granite_prompt(user_message, history_text)

    if prompt_style == "mistral":
        return build_mistral_prompt(user_message, history_text)

    return user_message


def build_llama_prompt(user_message: str, history_text: str) -> str:
    return f"""
{SYSTEM_PROMPT}

Previous conversation:
{history_text}

Current user message:
{user_message}

Assistant:
""".strip()


def build_granite_prompt(user_message: str, history_text: str) -> str:
    return f"""
{SYSTEM_PROMPT}

Previous conversation:
{history_text}

Current user message:
{user_message}

Assistant:
""".strip()


def build_mistral_prompt(user_message: str, history_text: str) -> str:
    return f"""
{SYSTEM_PROMPT}

Previous conversation:
{history_text}

Current user message:
{user_message}

Assistant:
""".strip()


def generate_response(model: str, message: str, conversation_id: str) -> str:
    prompt = build_prompt(
        model_key=model,
        user_message=message,
        conversation_id=conversation_id
    )

    llm = get_llm(model)

    add_message(conversation_id, "user", message)

    try:
        answer = llm.invoke(prompt)
    except Exception as e:
        return f"Model request failed: {str(e)}"

    add_message(conversation_id, "assistant", answer)

    return answer