const conversationId = "browser-chat";

const modelSelect = document.getElementById("modelSelect");
const chatBox = document.getElementById("chatBox");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const clearButton = document.getElementById("clearButton");

async function loadModels() {
    const response = await fetch("/models");
    const data = await response.json();

    modelSelect.innerHTML = "";

    data.models.forEach(model => {
        const option = document.createElement("option");
        option.value = model.key;
        option.textContent = `${model.display_name} (${model.key})`;
        modelSelect.appendChild(option);
    });
}

function addMessage(role, content) {
    const messageDiv = document.createElement("div");

    if (role === "user") {
        messageDiv.className = "message user-message";
        messageDiv.textContent = `You:\n${content}`;
    } else if (role === "assistant") {
        messageDiv.className = "message assistant-message";
        messageDiv.textContent = `Assistant:\n${content}`;
    } else {
        messageDiv.className = "message error-message";
        messageDiv.textContent = content;
    }

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const model = modelSelect.value;
    const message = messageInput.value.trim();

    if (!model) {
        addMessage("error", "Please select a model.");
        return;
    }

    if (!message) {
        addMessage("error", "Please enter a message.");
        return;
    }

    addMessage("user", message);
    messageInput.value = "";

    sendButton.disabled = true;
    sendButton.textContent = "Sending...";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                conversation_id: conversationId,
                model: model,
                message: message
            })
        });

        const contentType = response.headers.get("content-type");

        let data;

        if (contentType && contentType.includes("application/json")) {
            data = await response.json();
        } else {
            const text = await response.text();
            addMessage("error", `Server returned non-JSON response:\n${text.slice(0, 500)}`);
            return;
        }

        if (!response.ok) {
            addMessage("error", data.error || data.answer || "Request failed.");
            return;
        }

        addMessage("assistant", data.answer);
    } catch (error) {
        addMessage("error", `Error: ${error.message}`);
    } finally {
        sendButton.disabled = false;
        sendButton.textContent = "Send";
    }
}

async function clearChat() {
    chatBox.innerHTML = "";

    try {
        await fetch(`/conversations/${conversationId}`, {
            method: "DELETE"
        });

        addMessage("assistant", "Chat cleared.");
    } catch (error) {
        addMessage("error", `Error clearing chat: ${error.message}`);
    }
}

sendButton.addEventListener("click", sendMessage);

clearButton.addEventListener("click", clearChat);

messageInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

loadModels();