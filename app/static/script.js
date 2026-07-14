// ── Send a message when the form is submitted ──────────────────────────────
async function sendMessage(event) {
    event.preventDefault();

    const inputField = document.getElementById('user-input');
    const msg = inputField.value.trim();
    if (!msg) return;

    inputField.value = '';
    appendMessage(msg, 'user');

    const typingId = showTypingIndicator();

    try {
        const formData = new FormData();
        formData.append('msg', msg);

        const response = await fetch('/chat', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        removeMessage(typingId);
        appendMessage(data.answer, 'bot');

    } catch (error) {
        console.error("Chat error:", error);
        removeMessage(typingId);
        appendMessage("Sorry, something went wrong. Please try again.", 'bot');
    }
}

// ── Add a message bubble to the chat box ───────────────────────────────────
function appendMessage(text, sender) {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);

    const icon = sender === 'user' ? 'fa-user' : 'fa-robot';

    msgDiv.innerHTML = `
        <div class="avatar"><i class="fa-solid ${icon}"></i></div>
        <div class="bubble">${escapeHTML(text)}</div>
    `;

    chatBox.appendChild(msgDiv);
    scrollToBottom();
}

// ── Show animated typing dots while waiting for the bot ────────────────────
function showTypingIndicator() {
    const chatBox = document.getElementById('chat-box');
    const msgDiv = document.createElement('div');
    const id = 'typing-' + Date.now();
    msgDiv.id = id;
    msgDiv.classList.add('message', 'bot');

    msgDiv.innerHTML = `
        <div class="avatar"><i class="fa-solid fa-robot"></i></div>
        <div class="bubble">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>
    `;

    chatBox.appendChild(msgDiv);
    scrollToBottom();
    return id;
}

// ── Remove a message by its ID ──────────────────────────────────────────────
function removeMessage(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

// ── Scroll chat to the latest message ──────────────────────────────────────
function scrollToBottom() {
    const chatBox = document.getElementById('chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
}

// ── Prevent XSS by escaping HTML special characters ────────────────────────
function escapeHTML(str) {
    return str.replace(/[&<>'"]/g,
        tag => ({
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            "'": '&#39;',
            '"': '&quot;'
        }[tag] || tag)
    );
}
