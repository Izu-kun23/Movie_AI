// API Configuration
// Automatically use same origin in production, localhost in development
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:8000'
    : ''; // Empty string = same origin (production)

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const typingIndicator = document.getElementById('typingIndicator');
const suggestionButtons = document.querySelectorAll('.suggestion-btn');

// Initialize chat
let chatHistory = [];

// Event Listeners
sendBtn.addEventListener('click', handleSendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSendMessage();
    }
});

suggestionButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        const message = btn.getAttribute('data-message');
        chatInput.value = message;
        handleSendMessage();
    });
});

// Send message to AI
async function handleSendMessage() {
    const message = chatInput.value.trim();
    
    if (!message) return;
    
    // Clear input
    chatInput.value = '';
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Detect intent
        const msgType = detectIntent(message);
        
        // Send to AI chat endpoint
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                type: msgType
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Request failed');
        }
        
        const data = await response.json();
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Handle AI response
        handleAIResponse(data);
        
    } catch (error) {
        hideTypingIndicator();
        addMessage(`Sorry, I encountered an error: ${error.message}`, 'ai', 'error');
    }
}

// Detect user intent
function detectIntent(message) {
    const lowerMsg = message.toLowerCase();
    
    if (lowerMsg.match(/hello|hi|hey|greetings/i)) {
        return 'greeting';
    } else if (lowerMsg.match(/search|find|look for/i)) {
        return 'search';
    } else {
        return 'recommend';  // Default to recommendation
    }
}

// Handle AI response
function handleAIResponse(data) {
    if (data.type === 'greeting') {
        addMessage(data.message, 'ai');
    } else if (data.type === 'recommendations') {
        // Add intro message
        addMessage(data.message, 'ai');
        
        // Add recommendations as cards
        setTimeout(() => {
            displayRecommendations(data.recommendations, data.requested_movie);
        }, 500);
        
    } else if (data.type === 'search_results') {
        addMessage(data.message, 'ai');
        
        if (data.movies && data.movies.length > 0) {
            setTimeout(() => {
                displaySearchResults(data.movies);
            }, 500);
        }
        
    } else if (data.type === 'error') {
        addMessage(data.message, 'ai', 'error');
    }
}

// Add message to chat
function addMessage(text, sender, type = 'normal') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message--${sender}`;
    
    if (sender === 'ai') {
        messageDiv.innerHTML = `
            <div class="message__avatar">🤖</div>
            <div class="message__content">
                <p>${escapeHtml(text)}</p>
                <span class="message__time">${getCurrentTime()}</span>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="message__content">
                <p>${escapeHtml(text)}</p>
                <span class="message__time">${getCurrentTime()}</span>
            </div>
            <div class="message__avatar">👤</div>
        `;
    }
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
    
    // Typewriter effect for AI messages
    if (sender === 'ai' && type !== 'error') {
        animateTyping(messageDiv);
    }
}

// Display recommendations in chat
function displayRecommendations(recommendations, requestedMovie) {
    const container = document.createElement('div');
    container.className = 'recommendations-container';
    
    recommendations.forEach((movie, index) => {
        const card = document.createElement('div');
        card.className = 'movie-card-chat';
        card.style.animationDelay = `${index * 0.1}s`;
        
        const similarityPercent = (movie.similarity_score * 100).toFixed(1);
        const posterHtml = movie.poster 
            ? `<div class="movie-card-chat__poster">
                 <img src="${escapeHtml(movie.poster)}" alt="${escapeHtml(movie.title)}" 
                      onerror="this.style.display='none'; this.parentElement.style.display='none';">
               </div>`
            : '';
        
        card.innerHTML = `
            ${posterHtml}
            <div class="movie-card-chat__content">
                <div class="movie-card-chat__header">
                    <h3 class="movie-card-chat__title">${escapeHtml(movie.title)}</h3>
                    <span class="movie-card-chat__match">${similarityPercent}% match</span>
                </div>
                <p class="movie-card-chat__overview">${escapeHtml(movie.overview)}</p>
                <div class="movie-card-chat__explanation">
                    💡 ${escapeHtml(movie.explanation || 'Great recommendation based on your preferences!')}
                </div>
                <button class="movie-card-chat__btn" onclick="chatRecommendFor('${escapeHtml(movie.title)}')">
                    Get similar movies
                </button>
            </div>
        `;
        
        container.appendChild(card);
    });
    
    chatMessages.appendChild(container);
    scrollToBottom();
}

// Display search results
function displaySearchResults(movies) {
    const container = document.createElement('div');
    container.className = 'search-results-container';
    
    movies.forEach(movie => {
        const item = document.createElement('div');
        item.className = 'search-result-item';
        
        const posterHtml = movie.poster 
            ? `<div class="search-result-item__poster">
                 <img src="${escapeHtml(movie.poster)}" alt="${escapeHtml(movie.title)}" 
                      onerror="this.style.display='none'; this.parentElement.style.display='none';">
               </div>`
            : '';
        
        item.innerHTML = `
            ${posterHtml}
            <div class="search-result-item__content">
                <h4 class="search-result-item__title">${escapeHtml(movie.title)}</h4>
                <p class="search-result-item__overview">${escapeHtml(movie.overview)}</p>
                <button class="search-result-item__btn" onclick="chatRecommendFor('${escapeHtml(movie.title)}')">
                    Get recommendations
                </button>
            </div>
        `;
        container.appendChild(item);
    });
    
    chatMessages.appendChild(container);
    scrollToBottom();
}

// Get recommendations for a movie from chat
async function chatRecommendFor(movieTitle) {
    chatInput.value = `I like ${movieTitle}`;
    handleSendMessage();
}

// Show typing indicator
function showTypingIndicator() {
    typingIndicator.classList.remove('hidden');
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    typingIndicator.classList.add('hidden');
}

// Scroll to bottom of chat
function scrollToBottom() {
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

// Animate typing effect
function animateTyping(messageElement) {
    const textElement = messageElement.querySelector('p');
    const originalText = textElement.textContent;
    textElement.textContent = '';
    
    let index = 0;
    const typingSpeed = 20; // milliseconds per character
    
    function typeCharacter() {
        if (index < originalText.length) {
            textElement.textContent += originalText[index];
            index++;
            scrollToBottom();
            setTimeout(typeCharacter, typingSpeed + Math.random() * 20);
        }
    }
    
    typeCharacter();
}

// Get current time
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Make function available globally
window.chatRecommendFor = chatRecommendFor;
