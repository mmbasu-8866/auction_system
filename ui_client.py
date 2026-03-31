import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

PORT = 5555

class AuctionUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Auction Client")

        # Text area
        self.chat_area = scrolledtext.ScrolledText(root, height=20, width=60)
        self.chat_area.pack()

        # Entry
        self.entry = tk.Entry(root, width=50)
        self.entry.pack(side=tk.LEFT, padx=5)

        # Send button
        self.send_btn = tk.Button(root, text="Send", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT)

        # Connect button
        self.connect_btn = tk.Button(root, text="Connect", command=self.connect)
        self.connect_btn.pack()

        self.client = None

    def connect(self):
        host = "127.0.0.1"   # change if needed

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, PORT))

        # Ask name
        name = "User"  # you can add input box later
        self.client.send(name.encode())

        threading.Thread(target=self.receive_messages, daemon=True).start()

    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(1024).decode()
                self.chat_area.insert(tk.END, message + "\n")
            except:
                break

    def send_message(self):
        msg = self.entry.get()
        self.client.send(msg.encode())
        self.entry.delete(0, tk.END)

root = tk.Tk()
app = AuctionUI(root)
root.mainloop()