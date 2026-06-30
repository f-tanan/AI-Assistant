from flask import Blueprint, jsonify, request
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


@main.post("/chat")
def chat():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

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

    return jsonify({
        "model": model,
        "message": message,
        "answer": f"Temporary response from {model}: you said '{message}'"
    })