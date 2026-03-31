# 🎨 Customization Guide - Advanced Auction System

## Overview

This guide shows you how to customize every aspect of your auction system without coding knowledge.

---

## 1️⃣ Customize Auction Items

### Edit Auction Items

**File:** `logic.py`  
**Line:** Around line 20

**Find this section:**
```python
self.items = [
    {"name": "Vintage Watch", "base_price": 200},
    {"name": "Gold Necklace", "base_price": 200},
    {"name": "Antique Vase", "base_price": 200},
    {"name": "Diamond Ring", "base_price": 200},
    {"name": "Rare Painting", "base_price": 200}
]
```

**Example: Change to Electronics Auction**
```python
self.items = [
    {"name": "iPhone 15 Pro", "base_price": 500},
    {"name": "Sony Headphones", "base_price": 150},
    {"name": "iPad Air", "base_price": 400},
    {"name": "Apple Watch", "base_price": 250},
    {"name": "MacBook Pro", "base_price": 800}
]
```

**Example: Car Auction**
```python
self.items = [
    {"name": "2020 Honda Civic", "base_price": 10000},
    {"name": "2018 Toyota Camry", "base_price": 12000},
    {"name": "2019 Ford F-150", "base_price": 15000}
]
```

---

## 2️⃣ Customize Game Rules

### Starting Balance

**File:** `logic.py`  
**Line:** In `register_client` method

**Current:**
```python
self.balances[user] = 1000
```

**Examples:**
```python
self.balances[user] = 5000      # High-stakes auction
self.balances[user] = 100       # Quick auction
self.balances[user] = 10000     # Luxury items
```

### Auction Timer Duration

**File:** `logic.py`  
**Lines:** Around 30-31

**Current:**
```python
self.time_limit = 20
self.remaining_time = 20
```

**Examples:**
```python
self.time_limit = 10    # Fast-paced (10 seconds per item)
self.time_limit = 60    # Slow-paced (1 minute per item)
self.time_limit = 5     # Speed auction (5 seconds)
```

### Startup Countdown

**File:** `models.py` (or `logic.py` if using new structure)  
**Line:** In `timer_loop` function

**Current:**
```python
for remaining in range(120, 0, -1):  # 120 seconds = 2 minutes
```

**Examples:**
```python
for remaining in range(300, 0, -1):   # 5 minute countdown
for remaining in range(60, 0, -1):    # 1 minute countdown
for remaining in range(10, 0, -1):    # 10 second start
```

### Minimum Bid Increment

**File:** `logic.py`  
**In `place_bid` method**

**Current:** (Any amount higher than current price)
```python
if price <= self.current_price:
    return {"success": False, "message": f"Bid must be higher than ${self.current_price}"}
```

**To enforce minimum increase (e.g., $10 increment):**
```python
min_increment = 10  # Minimum bid increase

if price < self.current_price + min_increment:
    return {
        "success": False,
        "message": f"Bids must increase by at least ${min_increment}. Next bid: ${self.current_price + min_increment}"
    }
```

---

## 3️⃣ Customize User Interface

### Change Colors

**File:** `static/style.css`  
**Section:** `:root` variables (lines 8-18)

**Current colors:**
```css
:root {
    --primary-color: #2563eb;      /* Blue */
    --success-color: #10b981;      /* Green */
    --danger-color: #ef4444;       /* Red */
    --warning-color: #f59e0b;      /* Orange */
    --info-color: #3b82f6;         /* Light Blue */
    --dark-bg: #1f2937;            /* Dark Gray */
    --light-bg: #f9fafb;           /* Light Gray */
    --border-color: #e5e7eb;       /* Border Gray */
    --text-color: #111827;         /* Dark Text */
}
```

**Example: Dark Theme**
```css
:root {
    --primary-color: #00ff88;      /* Neon Green */
    --success-color: #00ff88;
    --danger-color: #ff0055;       /* Neon Pink */
    --warning-color: #ffaa00;      /* Orange */
    --info-color: #00ccff;         /* Cyan */
    --dark-bg: #0a0e27;            /* Very Dark */
    --light-bg: #1a1f3a;           /* Dark Blue */
    --border-color: #2d3a5c;
    --text-color: #e0e6ff;         /* Light Text */
}
```

**Example: Professional Blue**
```css
:root {
    --primary-color: #003366;      /* Navy */
    --success-color: #006633;      /* Dark Green */
    --danger-color: #cc0000;       /* Dark Red */
    --warning-color: #ff6600;      /* Orange */
    --info-color: #0066cc;         /* Blue */
    --dark-bg: #f5f5f5;
    --light-bg: #ffffff;
    --border-color: #cccccc;
    --text-color: #333333;
}
```

### Change Logo/Title

**File:** `templates/index.html`  
**Line:** Around 30

**Current:**
```html
<h1>🎯 Advanced Auction System</h1>
```

**Examples:**
```html
<h1>💎 Luxury Auction House</h1>
<h1>🚗 Auto Auction Live</h1>
<h1>📱 Tech Gadget Auction</h1>
<h1>🏺 Antiques & Collectibles</h1>
```

### Change Font

**File:** `static/style.css`  
**Line:** Around 21

**Current:**
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
```

**Examples:**
```css
/* Elegant/Luxury */
font-family: 'Georgia', 'Times New Roman', serif;

/* Modern/Tech */
font-family: 'Courier New', monospace;

/* Playful */
font-family: 'Comic Sans MS', 'Comic Sans', cursive;

/* Professional */
font-family: 'Arial', 'Helvetica', sans-serif;
```

### Change Button Styles

**File:** `static/style.css`  
**Lines:** Around 180-220

**Current:**
```css
.btn-primary {
    background: var(--primary-color);
    color: white;
}
```

**To make buttons rounded:**
```css
.btn {
    padding: 12px 30px;
    border: none;
    border-radius: 50px;  /* Fully rounded */
    /* ... rest of styling ... */
}
```

---

## 4️⃣ Customize Server Settings

### Change Server Port

**File:** `web_server.py`  
**Last line**

**Current:**
```python
socketio.run(app, host='0.0.0.0', port=5000, debug=False)
```

**Examples:**
```python
socketio.run(app, host='0.0.0.0', port=8000, debug=False)   # Port 8000
socketio.run(app, host='0.0.0.0', port=3000, debug=False)   # Port 3000
socketio.run(app, host='0.0.0.0', port=80, debug=False)     # Port 80 (needs sudo)
```

Then access at: `http://localhost:8000` (if changed to 8000)

### Limit to Localhost Only

**File:** `web_server.py`  
**Last line**

**Current:** (accessible from anywhere)
```python
socketio.run(app, host='0.0.0.0', port=5000, debug=False)
```

**Localhost only:**
```python
socketio.run(app, host='127.0.0.1', port=5000, debug=False)
```

### Enable Debug Mode (Development Only!)

**File:** `web_server.py`  
**Last line**

**Current:**
```python
socketio.run(app, host='0.0.0.0', port=5000, debug=False)
```

**For development (shows errors):**
```python
socketio.run(app, host='0.0.0.0', port=5000, debug=True)
```

---

## 5️⃣ Customize Auction Messages

### Welcome Message

**File:** `logic.py`  
**In `welcome_message` method**

**Current:**
```python
def welcome_message(self, user):
    return f"""
Welcome {user}!

Auction Rules:

1) Initial Balance: $1000
2) Base price: $200
3) Higher bids only
4) Timer resets to 20 sec on every bid
5) If no bid in 20 sec → item sold
6) All balances are virtual currency
"""
```

**Custom example:**
```python
def welcome_message(self, user):
    return f"""
🎉 Welcome to Luxury Auctions, {user}!

🏆 Tournament Rules:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Your Starting Balance: $5,000
✓ Items Starting Price: $500
✓ Bid Step: Increase only
✓ Time Per Item: 20 seconds
✓ Auto-win: Highest bid when timer ends
✓ Have Fun Bidding!

Good luck and happy bidding! 💎
"""
```

---

## 6️⃣ Advanced Customization

### Add Username Validation

**File:** `web_server.py`  
**In `handle_register` function**

**Current:**
```python
if len(username) > 20:
    emit('error', {'message': 'Username too long'})
    return
```

**To prevent special characters:**
```python
import re

if not re.match("^[a-zA-Z0-9_]*$", username):
    emit('error', {'message': 'Username can only contain letters, numbers, and underscore'})
    return
```

### Add Maximum Users Limit

**File:** `web_server.py`  
**In `handle_register` function**

```python
MAX_USERS = 10

if len(clients_info) >= MAX_USERS:
    emit('error', {'message': f'Auction full! Maximum {MAX_USERS} users'})
    return
```

### Add Chat Feature

**File:** `web_server.py`  
**Add new event:**

```python
@socketio.on('chat_message')
def handle_chat(data):
    with clients_lock:
        if request.sid not in clients_info:
            return
        username = clients_info[request.sid]
    
    message = data.get('message', '').strip()[:100]
    broadcast_update(f"💬 {username}: {message}", "info")
```

**File:** `static/script.js`  
**Add to HTML listeners:**

```javascript
// Add send chat button click handler
chatBtn.addEventListener('click', () => {
    const msg = chatInput.value;
    if (msg) {
        socket.emit('chat_message', { message: msg });
        chatInput.value = '';
    }
});
```

---

## 7️⃣ Styling Examples

### Gradient Background

**File:** `static/style.css`  
**Line:** Around 19

**Current:**
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

**Other examples:**
```css
/* Sunset */
background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);

/* Ocean */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Forest */
background: linear-gradient(135deg, #134e5e 0%, #71b280 100%);

/* Midnight */
background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);

/* Purple Vibes */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

---

## 📝 Configuration Checklist

Before launching your auction:

- [ ] Updated auction items list
- [ ] Set appropriate starting balance
- [ ] Configured timer duration
- [ ] Customized colors/theme
- [ ] Updated title and messages
- [ ] Set correct server port
- [ ] Tested from external machine
- [ ] Verified all buttons work
- [ ] Checked console for errors

---

## 💡 Pro Tips

1. **Test locally first** - changes to port number
2. **Backup originals** - save before major edits
3. **Use color picker** - find perfect color at `colorpicker.com`
4. **Mobile friendly** - CSS is responsive, test on phones
5. **Fast refresh** - Ctrl+Shift+Delete → Clear cache + Reload

---

## 🚀 Ready to Deploy?

Once customized:

1. Test thoroughly
2. Get IP address: `hostname -I` (Linux) or `ipconfig` (Windows)
3. Share IP with friends: `http://<YOUR_IP>:5000`
4. Run `python web_server.py`
5. Enjoy your custom auction!

---

**Happy customizing! 🎨**
