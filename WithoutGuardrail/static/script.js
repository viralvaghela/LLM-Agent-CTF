const chatHistory = document.getElementById('chat-history');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const modelSelect = document.getElementById('model-select');
const fileUpload = document.getElementById('file-upload');

// Generate a random session ID for this window
const sessionId = Math.random().toString(36).substring(2, 15);

// Fetch available models from Ollama
async function loadModels() {
    try {
        const response = await fetch('/api/models');
        const data = await response.json();
        
        modelSelect.innerHTML = '';
        if (data.models && data.models.length > 0) {
            data.models.forEach(model => {
                const option = document.createElement('option');
                option.value = model;
                option.textContent = `Ollama: ${model}`;
                modelSelect.appendChild(option);
            });
        } else {
            const option = document.createElement('option');
            option.value = "llama3.1";
            option.textContent = "Ollama: llama3.1 (default)";
            modelSelect.appendChild(option);
        }
    } catch (error) {
        console.error("Error loading models:", error);
    }
}

// Initialize models on load
loadModels();

function appendMessage(role, content) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Simple newline to br replacement
    contentDiv.innerHTML = content.replace(/\n/g, '<br>');
    
    msgDiv.appendChild(contentDiv);
    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    
    return msgDiv;
}

function appendLoading() {
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message agent';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const indicator = document.createElement('div');
    indicator.className = 'loading-indicator';
    indicator.innerHTML = '<div class="dot"></div><div class="dot"></div><div class="dot"></div>';
    
    contentDiv.appendChild(indicator);
    msgDiv.appendChild(contentDiv);
    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    
    return msgDiv;
}

async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;
    
    // Clear input
    chatInput.value = '';
    
    // Append User Message
    appendMessage('user', text);
    
    // Append Loading
    const loadingEl = appendLoading();
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId,
                message: text,
                role: 'user',
                model: modelSelect.value
            })
        });
        
        const data = await response.json();
        
        // Remove loading
        chatHistory.removeChild(loadingEl);
        
        // Append Agent Message
        appendMessage('agent', data.response);
        
    } catch (error) {
        chatHistory.removeChild(loadingEl);
        appendMessage('system', 'Connection to server failed.');
    }
}

sendBtn.addEventListener('click', sendMessage);

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

fileUpload.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    const loadingEl = appendLoading();

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        chatHistory.removeChild(loadingEl);

        if (response.ok) {
            appendMessage('system', `File ${data.filename} uploaded successfully.`);
            // Automatically prompt the agent to read the uploaded file
            chatInput.value = `Can you process the ticket from uploads/${data.filename}?`;
            sendMessage();
        } else {
            appendMessage('system', 'File upload failed.');
        }

    } catch (error) {
        chatHistory.removeChild(loadingEl);
        appendMessage('system', 'Connection to server failed during upload.');
    }
});
