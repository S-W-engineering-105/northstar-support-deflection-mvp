let sessionId = "session_" + Math.random().toString(36).substring(2, 10);
const messagesDiv = document.getElementById("chat-messages");
const input = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");
const quickReplyBtns = document.querySelectorAll(".quick-reply-btn");
const clearChatBtn = document.getElementById("clear-chat-btn");

function formatTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function addMessage(text, sender) {
    const wrapper = document.createElement("div");
    wrapper.classList.add("message-wrapper", sender === "user" ? "user" : "bot");

    const msgDiv = document.createElement("div");
    msgDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");
    msgDiv.textContent = text;

    const timeDiv = document.createElement("div");
    timeDiv.classList.add("timestamp");
    timeDiv.textContent = formatTime();

    wrapper.appendChild(msgDiv);
    wrapper.appendChild(timeDiv);
    messagesDiv.appendChild(wrapper);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function showTypingIndicator() {
    const wrapper = document.createElement("div");
    wrapper.classList.add("message-wrapper", "bot");
    wrapper.id = "typing-wrapper";

    const typing = document.createElement("div");
    typing.classList.add("typing-indicator");
    typing.innerHTML = "<span></span><span></span><span></span>";

    wrapper.appendChild(typing);
    messagesDiv.appendChild(wrapper);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function removeTypingIndicator() {
    const el = document.getElementById("typing-wrapper");
    if (el) el.remove();
}

async function sendMessage(overrideText) {
    const text = (overrideText !== undefined ? overrideText : input.value).trim();
    if (!text) return;

    addMessage(text, "user");
    input.value = "";
    sendBtn.disabled = true;

    showTypingIndicator();

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: sessionId, message: text })
        });
        const data = await response.json();

        await new Promise(resolve => setTimeout(resolve, 400));

        removeTypingIndicator();
        addMessage(data.reply, "bot");
    } catch (err) {
        removeTypingIndicator();
        addMessage("Sorry, something went wrong. Please try again.", "bot");
    }
}

sendBtn.addEventListener("click", () => sendMessage());
input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});

input.addEventListener("input", () => {
    sendBtn.disabled = input.value.trim().length === 0;
});

quickReplyBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        sendMessage(btn.dataset.msg);
    });
});

clearChatBtn.addEventListener("click", () => {
    messagesDiv.innerHTML = "";
    sessionId = "session_" + Math.random().toString(36).substring(2, 10);
    addMessage("Hi! I'm Northstar's support assistant. I can help you check your order status or product availability. How can I help?", "bot");
});

// Greet the customer on load
addMessage("Hi! I'm Northstar's support assistant. I can help you check your order status or product availability. How can I help?", "bot");