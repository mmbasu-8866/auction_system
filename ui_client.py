import threading
import tkinter as tk
from tkinter import scrolledtext

import socketio

SERVER_URL = "http://localhost:5000"

sio = socketio.Client()
app = None


class AuctionUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Auction Client")

        # Username area
        self.user_frame = tk.Frame(root)
        self.user_frame.pack(pady=5)
        tk.Label(self.user_frame, text="Username:").pack(side=tk.LEFT)
        self.username_entry = tk.Entry(self.user_frame, width=16)
        self.username_entry.pack(side=tk.LEFT, padx=4)
        self.register_btn = tk.Button(self.user_frame, text="Register", command=self.register)
        self.register_btn.pack(side=tk.LEFT)

        # Bid area
        self.bid_frame = tk.Frame(root)
        self.bid_frame.pack(pady=5)
        tk.Label(self.bid_frame, text="Bid amount:").pack(side=tk.LEFT)
        self.bid_entry = tk.Entry(self.bid_frame, width=10)
        self.bid_entry.pack(side=tk.LEFT, padx=4)
        self.bid_btn = tk.Button(self.bid_frame, text="Bid", command=self.place_bid)
        self.bid_btn.pack(side=tk.LEFT)

        # Chat/history area
        self.chat_area = scrolledtext.ScrolledText(root, height=16, width=70)
        self.chat_area.pack(padx=5, pady=5)
        self.chat_area.configure(state=tk.DISABLED)

        # Connect controls
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=5)
        self.connect_btn = tk.Button(self.control_frame, text="Connect", command=self.connect)
        self.connect_btn.pack(side=tk.LEFT, padx=2)
        self.disconnect_btn = tk.Button(self.control_frame, text="Disconnect", command=self.disconnect)
        self.disconnect_btn.pack(side=tk.LEFT, padx=2)

        self.username = None

    def append_log(self, text):
        self.chat_area.configure(state=tk.NORMAL)
        self.chat_area.insert(tk.END, text + "\n")
        self.chat_area.see(tk.END)
        self.chat_area.configure(state=tk.DISABLED)

    def connect(self):
        try:
            if not sio.connected:
                sio.connect(SERVER_URL)
                self.append_log("Connected to server (Socket.IO)")
        except Exception as ex:
            self.append_log(f"Error connecting: {ex}")

    def disconnect(self):
        if sio.connected:
            sio.disconnect()
            self.append_log("Disconnected from server")

    def register(self):
        name = self.username_entry.get().strip()
        if not name:
            self.append_log("Username cannot be empty")
            return
        self.username = name
        if sio.connected:
            sio.emit('register', {'username': self.username})

    def place_bid(self):
        if not self.username:
            self.append_log("Register before bidding")
            return
        if not sio.connected:
            self.append_log("Not connected")
            return
        try:
            bid_amount = int(self.bid_entry.get())
        except ValueError:
            self.append_log("Enter a valid integer bid")
            return
        sio.emit('place_bid', {'bid_amount': bid_amount})


@sio.event
def connect():
    if app:
        app.append_log("Socket.IO connected")


@sio.event
def disconnect():
    if app:
        app.append_log("Socket.IO disconnected")


@sio.on('welcome')
def on_welcome(data):
    if app:
        app.append_log(f"WELCOME: {data.get('message', '').strip()}")


@sio.on('message_update')
def on_message_update(data):
    if app:
        app.append_log(f"{data.get('timestamp', '')} | {data.get('type', '')}: {data.get('message', '')}")


@sio.on('auction_state')
def on_auction_state(data):
    if app:
        item = data.get('current_item')
        if item:
            app.append_log(f"Auction [{data.get('status')}] Item={item.get('name')} Price={data.get('current_price')} Time={data.get('time_remaining')} Highest={data.get('highest_bidder')}")


@sio.on('error')
def on_error(data):
    if app:
        app.append_log(f"ERROR: {data.get('message')}")


if __name__ == '__main__':
    root = tk.Tk()
    app = AuctionUI(root)
    root.mainloop()