# Advanced Online Auction System

A modern, real-time auction platform with a web-based UI and server that supports external connections.

## Features

✨ **Modern Features:**
- 🌐 Web-based UI with responsive design
- 🔄 Real-time bidding with WebSocket communication
- 💰 Virtual balance management
- 📊 Live auction feed and history tracking
- 🎯 Multiple items auction support
- ⏱️ Real-time countdown timer
- 👥 Multi-user support with external connectivity

## System Architecture

```
- web_server.py: Flask + SocketIO server (accessible externally on port 5000)
- logic.py: Auction management and bidding logic
- static/: CSS and JavaScript frontend
- templates/: HTML interface
```

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Web Server

```bash
python web_server.py
```

The server will start at `http://0.0.0.0:5000` and be accessible from anywhere.

## Access the Auction

### From Same Machine:
```
http://localhost:5000
```

### From External Machine:
```
http://<SERVER_IP>:5000
```

Example (Server at 192.168.1.100):
```
http://192.168.1.100:5000
```

## How to Use

1. **Join the Auction**
   - Enter your username (max 20 characters)
   - Click "Join Auction"
   - Receive $1000 virtual currency

2. **Place Bids**
   - Enter bid amount higher than current price
   - Click "Place Bid" or press Enter
   - Timer resets to 20 seconds on each bid

3. **Win Items**
   - Highest bidder when timer ends wins
   - Automatically moves to next item
   - View your balance and auction history

## Auction Rules

- **Initial Balance:** $1000 per user
- **Base Price:** $200 per item
- **Bid Requirement:** Must exceed current price
- **Timer:** 20 seconds, resets on each bid
- **Auto-Sale:** Item sells when timer reaches 0
- **Refunds:** Previous bidder refunded if outbid
- **Items:** 5 items in auction

## Available Items

1. 🕐 Vintage Watch - $200
2. 💍 Gold Necklace - $200
3. 🏺 Antique Vase - $200
4. 💎 Diamond Ring - $200
5. 🎨 Rare Painting - $200

## Technology Stack

- **Backend:** Flask, Flask-SocketIO, Python
- **Frontend:** HTML5, CSS3, JavaScript
- **Communication:** WebSocket (real-time)
- **Threading:** Multi-threaded auction timer

## Troubleshooting

### Connection Issues?
- Check firewall allows port 5000
- Verify correct server IP address
- Ensure server is running

### Bid Not Accepted?
- Sufficient balance required
- Bid must exceed current price
- Auction must be running

### WebSocket Connection Fails?
- Check browser console for errors
- Verify network connectivity
- Confirm server is accessible

## System Requirements

- Python 3.7+
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Network access to server machine

## Project Files

| File | Purpose |
|------|---------|
| `web_server.py` | Main Flask-SocketIO server |
| `logic.py` | Auction management & bidding logic |
| `templates/index.html` | HTML frontend |
| `static/style.css` | UI styling |
| `static/script.js` | Client-side logic |
| `requirements.txt` | Python dependencies |

## Real-time Updates

- **Auction State:** Refreshes every bid or timer change
- **Live Feed:** Shows all bids and events in real-time
- **Balance:** Updates after each transaction
- **History:** Tracks all bids with timestamps

---

**Start Your Advanced Auction Now! 🎊**

