function toggleChat() {
    const chatContainer = document.getElementById('chat-container');
    if (chatContainer.style.display === 'none' || chatContainer.style.display === '') {
        chatContainer.style.display = 'flex';
    } else {
        chatContainer.style.display = 'none';
    }
}

// Function to check for Enter key press
function checkEnter(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    // Initially hide the chatbot
    const chatContainer = document.getElementById('chat-container');
    chatContainer.style.display = 'none';

    // Load any previous messages if needed
    loadMessages();
});

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value;
    if (message.trim() === '') return;

    // Display user message
    displayMessage('You', message);
    userInput.value = '';

    // Send message to Rasa server
    const response = await fetch('http://localhost:5005/webhooks/rest/webhook', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    });
    const data = await response.json();

    // Display bot responses
    data.forEach((item) => {
        if (item.text) {
            displayMessage('Bot', item.text);
        }
    });

    // Scroll to the bottom of the messages
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function displayMessage(sender, text) {
    const chatMessages = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatMessages.appendChild(messageElement);
}

function loadMessages() {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML = ''; // Clear existing messages
    const messages = JSON.parse(sessionStorage.getItem('chatMessages')) || [];
    messages.forEach(({ sender, message }) => {
        displayMessage(sender, message);
    });
}