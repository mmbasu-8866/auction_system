// Connect to the server via WebSocket
const socket = io();

// UI Elements
const loginPanel = document.getElementById('login-panel');
const auctionPanel = document.getElementById('auction-panel');
const usernameInput = document.getElementById('username-input');
const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');
const bidInput = document.getElementById('bid-input');
const bidBtn = document.getElementById('bid-btn');
const messagesContainer = document.getElementById('messages');
const connectionStatus = document.getElementById('connection-status');
const userInfo = document.getElementById('user-info');

let currentUsername = null;
let isLoggedIn = false;
let auctionRunning = false;

// Connection Events
socket.on('connect', () => {
    setConnectionStatus(true);
    console.log('Connected to server');
});

socket.on('disconnect', () => {
    setConnectionStatus(false);
    console.log('Disconnected from server');
    if (isLoggedIn) {
        showToast('Disconnected from server', 'danger');
        resetUI();
    }
});

socket.on('connection_response', (data) => {
    console.log('Server response:', data);
});

// Authentication
socket.on('welcome', (data) => {
    isLoggedIn = true;
    loginPanel.classList.remove('active');
    auctionPanel.classList.add('active');
    userInfo.textContent = `Logged in as: ${currentUsername}`;
    
    addMessage('Welcome! You have joined the auction.', 'info');
    updateBalance(data.balance);
    
    // Clear input
    usernameInput.value = '';
});

socket.on('error', (data) => {
    showToast(data.message, 'danger');
});

// Auction Updates
socket.on('auction_state', (data) => {
    const itemDisplay = document.getElementById('item-display');

    if (data.status === 'pending') {
        itemDisplay.innerHTML = `
            <p class="item-name">Waiting for auction to start...</p>
            <p class="item-price">$0</p>
        `;
    } else if (data.current_item) {
        itemDisplay.innerHTML = `
            <p class="item-name">${data.current_item.name}</p>
            <p class="item-price">$${data.current_price}</p>
        `;
    }

    document.getElementById('current-price').textContent = `$${data.current_price}`;
    document.getElementById('highest-bidder').textContent = data.highest_bidder || 'None';
    document.getElementById('time-remaining').textContent = `${data.time_remaining}s`;
    document.getElementById('active-bidders').textContent = data.active_bidders;

    // If auction is running, enable bidding
    if (data.status === 'running') {
        auctionRunning = true;
        bidBtn.disabled = false;
    } else {
        auctionRunning = false;
        bidBtn.disabled = true;
    }
});

socket.on('auction_started', (data) => {
    auctionRunning = true;
    bidBtn.disabled = false;
    addMessage(data.message || 'Auction started', 'info');
});

socket.on('message_update', (data) => {
    addMessage(data.message, data.type);
});

socket.on('balance_update', (data) => {
    updateBalance(data.balance);
});

socket.on('history', (data) => {
    updateHistory(data.history);
});

// Event Listeners
loginBtn.addEventListener('click', () => {
    const username = usernameInput.value.trim();
    if (!username) {
        showToast('Please enter a username', 'warning');
        return;
    }
    currentUsername = username;
    socket.emit('register', { username });

    // Disable bids until server confirms auction status
    auctionRunning = false;
    bidBtn.disabled = true;
});

// Allow Enter key for login
usernameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        loginBtn.click();
    }
});

bidBtn.addEventListener('click', () => {
    if (!auctionRunning) {
        showToast('Auction has not started yet. Please wait...', 'warning');
        return;
    }

    const bidAmount = parseInt(bidInput.value);
    if (!bidAmount || bidAmount < 1) {
        showToast('Please enter a valid bid amount', 'warning');
        return;
    }
    socket.emit('place_bid', { bid_amount: bidAmount });
    bidInput.value = '';
});

// Allow Enter key for bidding
bidInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        bidBtn.click();
    }
});

logoutBtn.addEventListener('click', () => {
    resetUI();
    socket.disconnect();
    setTimeout(() => socket.connect(), 500);
});

// Helper Functions
function setConnectionStatus(connected) {
    const status = connectionStatus;
    if (connected) {
        status.textContent = 'Connected';
        status.classList.remove('disconnected');
        status.classList.add('connected');
    } else {
        status.textContent = 'Disconnected';
        status.classList.remove('connected');
        status.classList.add('disconnected');
    }
}

function addMessage(message, type) {
    const messageEl = document.createElement('div');
    messageEl.className = `message ${type}`;
    
    const timestamp = new Date().toLocaleTimeString();
    messageEl.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span>${message}</span>
            <span class="message-timestamp">${timestamp}</span>
        </div>
    `;
    
    messagesContainer.appendChild(messageEl);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function updateBalance(balance) {
    document.getElementById('balance').textContent = `$${balance}`;
}

function updateHistory(history) {
    const historyContainer = document.getElementById('history');
    
    if (!history || history.length === 0) {
        historyContainer.innerHTML = '<p class="empty-message">No history yet</p>';
        return;
    }
    
    historyContainer.innerHTML = history.map((item, index) => `
        <div class="history-item">
            <div>
                <p class="history-label">Time</p>
                <p class="history-value">${item.timestamp || 'N/A'}</p>
            </div>
            <div>
                <p class="history-label">Item</p>
                <p class="history-value">${item.name || 'N/A'}</p>
            </div>
            <div>
                <p class="history-label">Bidder</p>
                <p class="history-value">${item.user || 'N/A'}</p>
            </div>
            <div>
                <p class="history-label">Price</p>
                <p class="history-value">$${item.price || 0}</p>
            </div>
            <div>
                <p class="history-label">Winner</p>
                <p class="history-value">${item.winner ? '✓ ' + item.winner : 'Pending'}</p>
            </div>
        </div>
    `).join('');
}

function resetUI() {
    isLoggedIn = false;
    currentUsername = null;
    loginPanel.classList.add('active');
    auctionPanel.classList.remove('active');
    userInfo.textContent = 'Not logged in';
    messagesContainer.innerHTML = '<p class="system-message">Waiting for auction to start...</p>';
    document.getElementById('history').innerHTML = '<p class="empty-message">No history yet</p>';
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `error-message`;
    if (type === 'warning') toast.className = 'message system';
    if (type === 'danger') toast.className = 'message bid';
    
    toast.textContent = message;
    
    // Insert at top of messages if in auction panel
    if (isLoggedIn) {
        messagesContainer.insertBefore(toast, messagesContainer.firstChild);
    }
}

// Periodic updates
setInterval(() => {
    if (isLoggedIn) {
        socket.emit('get_balance');
        socket.emit('get_history');
    }
}, 5000);

// Initial setup
document.addEventListener('DOMContentLoaded', () => {
    console.log('Auction client ready');
});
