from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
import threading
import time
import json
from datetime import datetime
from logic import AuctionManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'
socketio = SocketIO(app, cors_allowed_origins="*")

# Auction manager
auction = AuctionManager()
clients_info = {}  # Store client info {sid: username}
clients_lock = threading.Lock()

# Triangle: timer state control
timer_thread = None
countdown_active = False
countdown_value = 0
auction_started = False


def start_auction_timer():
    """Start the auction timer with WebSocket broadcasts"""
    global socketio, auction, timer_thread, auction_started
    
    # Ensure auction is marked started
    auction_started = True
    if not auction.auction_running:
        auction.start_auction()

    socketio.emit('auction_started', {
        'message': '🎯 AUCTION STARTED! Bidding is now open!'
    })

    socketio.emit('message_update', {
        'message': '🎯 AUCTION STARTED! Bidding is now open!',
        'type': 'system',
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })

    broadcast_auction_state()
    print(f"start_auction_timer: auction_running={auction.auction_running}, time_remaining={auction.remaining_time}")

    # Main auction loop
    while auction.auction_running:
        try:
            time.sleep(1)

            auction.decrease_timer()
            remaining = auction.get_time()
            print(f"timer tick: remaining={remaining}")

            # Broadcast timer to ALL clients (auction is running)
            socketio.emit('auction_state', {
                'current_item': auction.items[auction.current_index] if auction.current_index < len(auction.items) else None,
                'current_price': auction.current_price,
                'highest_bidder': auction.highest_bidder,
                'time_remaining': remaining,
                'status': 'running',
                'countdown_active': False,
                'countdown_remaining': 0,
                'active_bidders': len(clients_info)
            })  # Broadcast to all
            
            # Item sold when timer reaches 0
            if remaining == 0:
                print("\n✓ Item sold!")
                
                # Close item and get winner
                auction.close_current_item()
                winner = auction.highest_bidder or "Nobody"
                
                socketio.emit('message_update', {
                    'message': f'🔨 Item SOLD to {winner}!',
                    'type': 'system',
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                })
                
                # Move to next item
                auction.move_to_next_item()
                
                # Send updated history to all clients
                socketio.emit('history', {'history': auction.history})
                
                if auction.auction_running:
                    time.sleep(1)  # Pause before next item
                    socketio.emit('message_update', {
                        'message': f'⏭️ Next Item: {auction.items[auction.current_index]["name"]} - Starting at ${auction.items[auction.current_index]["base_price"]}',
                        'type': 'system',
                        'timestamp': datetime.now().strftime('%H:%M:%S')
                    })
                    
                    # Broadcast new item state
                    broadcast_auction_state()
                else:
                    socketio.emit('message_update', {
                        'message': '🎊 AUCTION FINISHED! Thank you for participating!',
                        'type': 'system',
                        'timestamp': datetime.now().strftime('%H:%M:%S')
                    })
        except Exception as e:
            print(f"Error in auction timer loop: {e}")
            break

    # timer thread ends when auction ends so restart is possible with fresh register
    timer_thread = None


@app.route('/')
def index():
    """Serve the main auction page"""
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    """Client connected"""
    print(f"Client connected: {request.sid}")
    emit('connection_response', {'data': 'Connected to auction server'})


@socketio.on('disconnect')
def handle_disconnect():
    """Client disconnected"""
    with clients_lock:
        if request.sid in clients_info:
            username = clients_info[request.sid]
            del clients_info[request.sid]
            print(f"Client disconnected: {username}")
            broadcast_update(f"{username} disconnected", "info")


@socketio.on('register')
def handle_register(data):
    """Register user"""
    global timer_thread, auction_started

    username = data.get('username', '').strip()
    
    if not username:
        emit('error', {'message': 'Username cannot be empty'})
        return
    
    if len(username) > 20:
        emit('error', {'message': 'Username too long'})
        return
    
    with clients_lock:
        if request.sid in clients_info:
            emit('error', {'message': 'Already registered'})
            return
        
        # Check if username already exists
        if username in [u for u in clients_info.values()]:
            emit('error', {'message': 'Username already taken'})
            return
        
        clients_info[request.sid] = username
        auction.register_client(username)
    
    # Send welcome message
    welcome = auction.welcome_message(username)
    emit('welcome', {
        'message': welcome,
        'balance': auction.balances[username]
    })
    
    # Broadcast to all clients
    broadcast_update(f"{username} joined the auction", "info")

    print(f"register: {username}, auction_running={auction.auction_running}, timer_thread={timer_thread}")

    # If auction not yet started and no timer running, start it immediately
    if not auction.auction_running and timer_thread is None:
        print(f"✓ First user joined: {username}, starting auction immediately...")
        timer_thread = threading.Thread(target=start_auction_timer, daemon=True)
        timer_thread.start()

    # Push current state and status to this user
    broadcast_auction_state()
    if auction_started:
        emit('auction_started', {
            'message': 'Auction already started'
        })


@socketio.on('place_bid')
def handle_bid(data):
    """Handle bid placement"""
    try:
        bid_amount = int(data.get('bid_amount', 0))
    except (ValueError, TypeError):
        emit('error', {'message': 'Invalid bid amount'})
        return
    
    with clients_lock:
        if request.sid not in clients_info:
            emit('error', {'message': 'Not registered'})
            return
        
        username = clients_info[request.sid]
    
    try:
        result = auction.place_bid(username, bid_amount)
        if result['success']:
            # Broadcast message to all
            socketio.emit('message_update', {
                'message': f"{username} bid ${bid_amount}",
                'type': 'bid',
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
            
            # Broadcast updated auction state to all
            broadcast_auction_state()
            
            # Broadcast updated history to all
            socketio.emit('history', {'history': auction.history})
            
            # Send success to this user
            emit('bid_success', {'message': f'Bid of ${bid_amount} placed!', 'balance': result.get('balance')})
        else:
            emit('error', {'message': result.get('message', 'Bid failed')})
    except Exception as e:
        print(f"Error placing bid: {e}")
        emit('error', {'message': str(e)})


@socketio.on('get_history')
def handle_get_history():
    """Get auction history"""
    emit('history', {'history': auction.history})


@socketio.on('get_balance')
def handle_get_balance():
    """Get current balance"""
    with clients_lock:
        if request.sid not in clients_info:
            emit('error', {'message': 'Not registered'})
            return
        
        username = clients_info[request.sid]
        balance = auction.balances.get(username, 0)
        emit('balance_update', {'balance': balance})


def broadcast_update(message, message_type="info"):
    """Broadcast message to all connected clients"""
    socketio.emit('message_update', {
        'message': message,
        'type': message_type,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })


def broadcast_auction_state():
    """Broadcast current auction state to all clients"""
    try:
        socketio.emit('auction_state', {
            'current_item': auction.items[auction.current_index] if auction.current_index < len(auction.items) else None,
            'current_price': auction.current_price,
            'highest_bidder': auction.highest_bidder,
            'time_remaining': auction.remaining_time,
            'status': 'running' if auction.auction_running else 'finished',
            'countdown_active': False,
            'countdown_remaining': 0,
            'active_bidders': len(clients_info)
        })
    except Exception as e:
        print(f"Error broadcasting auction state: {e}")


def broadcast_auction_state():
    """Broadcast current auction state to all clients"""
    current_item = None
    if auction.current_index < len(auction.items):
        current_item = auction.items[auction.current_index]
    auction_status = 'running' if auction.auction_running else 'pending'
    
    time_remaining = auction.remaining_time if auction.auction_running else 0
    current_price = auction.current_price if auction.auction_running else 0
    highest_bidder = auction.highest_bidder if auction.auction_running else 'None'

    socketio.emit('auction_state', {
        'current_item': current_item,
        'current_price': current_price,
        'highest_bidder': highest_bidder,
        'time_remaining': time_remaining,
        'status': auction_status,
        'countdown_active': countdown_active,
        'countdown_remaining': countdown_value,
        'active_bidders': len(clients_info)
    })


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print("Starting Advanced Auction Server...")
    print(f"Server accessible at http://0.0.0.0:{port}")
    # When on hosting services (Railway/Heroku), allow_unsafe_werkzeug is not used by socketio 5.x
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
