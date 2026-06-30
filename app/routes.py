from flask import Blueprint, jsonify, request

from app.chat import generate_response
from app.memory import clear_conversation, get_messages
from app.models import get_available_models, is_valid_model

main = Blueprint("main", __name__)


@main.get("/health")
def health():
    return jsonify({"status": "ok"})


@main.get("/models")
def get_models():
    return jsonify({
        "models": get_available_models()
    })


@main.get("/config-check")
def config_check():
    from flask import current_app

    return jsonify({
        "watsonx_apikey_loaded": bool(current_app.config.get("WATSONX_APIKEY")),
        "watsonx_project_id_loaded": bool(current_app.config.get("WATSONX_PROJECT_ID")),
        "watsonx_url_loaded": bool(current_app.config.get("WATSONX_URL")),
    })


@main.post("/chat")
def chat():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    conversation_id = data.get("conversation_id", "default")
    model = data.get("model")
    message = data.get("message")

    if not model:
        return jsonify({"error": "Missing required field: model"}), 400

    if not message:
        return jsonify({"error": "Missing required field: message"}), 400

    if not is_valid_model(model):
        return jsonify({
            "error": f"Unsupported model: {model}",
            "available_models": [m["key"] for m in get_available_models()]
        }), 400

    answer = generate_response(
        model=model,
        message=message,
        conversation_id=conversation_id
    )

    return jsonify({
        "conversation_id": conversation_id,
        "model": model,
        "message": message,
        "answer": answer
    })


@main.get("/chat-test")
def chat_test():
    conversation_id = request.args.get("conversation_id", "default")
    model = request.args.get("model")
    message = request.args.get("message")

    if not model:
        return jsonify({"error": "Missing query parameter: model"}), 400

    if not message:
        return jsonify({"error": "Missing query parameter: message"}), 400

    if not is_valid_model(model):
        return jsonify({
            "error": f"Unsupported model: {model}",
            "available_models": [m["key"] for m in get_available_models()]
        }), 400

    answer = generate_response(
        model=model,
        message=message,
        conversation_id=conversation_id
    )

    return jsonify({
        "conversation_id": conversation_id,
        "model": model,
        "message": message,
        "answer": answer
    })


@main.get("/conversations/<conversation_id>")
def get_conversation(conversation_id):
    return jsonify({
        "conversation_id": conversation_id,
        "messages": get_messages(conversation_id)
    })


@main.delete("/conversations/<conversation_id>")
def delete_conversation(conversation_id):
    clear_conversation(conversation_id)

    return jsonify({
        "conversation_id": conversation_id,
        "status": "cleared"
    })