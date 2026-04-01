#!/usr/bin/env python3
"""
Multi-Client Auction Test Script
Simulates multiple clients connecting to the auction server simultaneously
"""

import socketio
import time
import threading
import random
import sys

# Create SocketIO client instances
sio = socketio.Client()

class AuctionClient:
    def __init__(self, client_id, username):
        self.client_id = client_id
        self.username = username
        self.sio = socketio.Client()
        self.connected = False
        self.logged_in = False
        self.balance = 1000
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup WebSocket event handlers"""
        
        @self.sio.event
        def connect():
            print(f"[Client {self.client_id}] Connected to server")
            self.connected = True
            self.register()
        
        @self.sio.event
        def disconnect():
            print(f"[Client {self.client_id}] Disconnected from server")
            self.connected = False
            self.logged_in = False
        
        @self.sio.on('welcome')
        def on_welcome(data):
            print(f"[Client {self.client_id}] Welcome! Balance: ${data['balance']}")
            self.logged_in = True
            self.balance = data['balance']
        
        @self.sio.on('error')
        def on_error(data):
            print(f"[Client {self.client_id}] Error: {data['message']}")
        
        @self.sio.on('auction_started')
        def on_auction_started(data):
            print(f"[Client {self.client_id}] 🎯 {data['message']}")
        
        @self.sio.on('auction_state')
        def on_auction_state(data):
            item = data.get('current_item')
            if item:
                print(f"[Client {self.client_id}] Item: {item['name']} | "
                      f"Price: ${data['current_price']} | "
                      f"Bidder: {data['highest_bidder']} | "
                      f"Time: {data['time_remaining']}s | "
                      f"Active: {data['active_bidders']} users")
        
        @self.sio.on('message_update')
        def on_message(data):
            if data['type'] == 'bid':
                print(f"[Client {self.client_id}] 📢 {data['message']}")
        
        @self.sio.on('bid_success')
        def on_bid_success(data):
            self.balance = data.get('balance', self.balance)
            print(f"[Client {self.client_id}] ✓ Bid placed! Balance: ${self.balance}")
        
        @self.sio.on('balance_update')
        def on_balance_update(data):
            self.balance = data['balance']
            print(f"[Client {self.client_id}] Balance updated: ${self.balance}")
    
    def register(self):
        """Register with username"""
        print(f"[Client {self.client_id}] Registering as '{self.username}'...")
        self.sio.emit('register', {'username': self.username})
    
    def place_bid(self, amount):
        """Place a bid"""
        if self.logged_in:
            print(f"[Client {self.client_id}] Placing bid: ${amount}")
            self.sio.emit('place_bid', {'bid_amount': amount})
        else:
            print(f"[Client {self.client_id}] Not logged in, cannot bid")
    
    def connect(self, url):
        """Connect to auction server"""
        try:
            self.sio.connect(url, transports=['websocket', 'polling'])
            return True
        except Exception as e:
            print(f"[Client {self.client_id}] Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from server"""
        if self.connected:
            self.sio.disconnect()


def run_multi_client_test(num_clients=3, server_url='http://localhost:5000'):
    """
    Run multi-client auction test
    
    Args:
        num_clients: Number of clients to simulate
        server_url: Server URL to connect to
    """
    
    print(f"\n{'='*60}")
    print(f"🎯 MULTI-CLIENT AUCTION TEST")
    print(f"{'='*60}")
    print(f"Connecting {num_clients} clients to {server_url}\n")
    
    clients = []
    usernames = [f"Player{i+1}" for i in range(num_clients)]
    
    # Create and connect all clients
    for i in range(num_clients):
        client = AuctionClient(i+1, usernames[i])
        if client.connect(server_url):
            clients.append(client)
            time.sleep(0.5)  # Stagger connections
    
    print(f"\n✓ {len(clients)} clients connected\n")
    
    # Simulate bidding activity
    if len(clients) > 0:
        print("Starting bidding simulation in 5 seconds...\n")
        time.sleep(5)
        
        for round_num in range(3):
            print(f"\n{'─'*60}")
            print(f"Bidding Round {round_num + 1}")
            print(f"{'─'*60}")
            
            # Each client places random bids
            for client in clients:
                if client.logged_in:
                    time.sleep(random.uniform(1, 3))
                    bid_amount = random.randint(250, 900)
                    client.place_bid(bid_amount)
            
            time.sleep(5)
    
    # Keep clients connected for a while
    print(f"\n{'─'*60}")
    print("Auction in progress... Press Ctrl+C to stop")
    print(f"{'─'*60}\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down clients...")
        for client in clients:
            client.disconnect()
        print("✓ All clients disconnected")


if __name__ == '__main__':
    
    # Get number of clients from command line or use default
    num_clients = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    server_url = sys.argv[2] if len(sys.argv) > 2 else 'http://localhost:5000'
    
    try:
        run_multi_client_test(num_clients=num_clients, server_url=server_url)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
