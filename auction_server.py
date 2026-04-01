import os
import socket
import threading

from auction_client import handle_client
from models import start_timer
from logic import AuctionManager

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "5555"))

clients = []
clients_lock = threading.Lock()

auction = AuctionManager()


def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def start_server():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))
    server.listen(10)

    local_ip = get_local_ip()
    print("Auction Server Started")
    print("Listening on:")
    print(f"  - 0.0.0.0:{PORT}  (all interfaces)")
    print(f"  - {local_ip}:{PORT}  (use this from other Wi-Fi devices)")
    print("Waiting for clients...")

    start_timer(
        auction,
        clients,
        clients_lock
    )

    while True:

        conn, addr = server.accept()

        print("Connected from:", addr)

        conn.send(
            "Enter your name: ".encode()
        )

        name = conn.recv(1024).decode().strip()

        thread = threading.Thread(
            target=handle_client,
            args=(
                conn,
                addr,
                name,
                clients,
                clients_lock,
                auction
            ),
            daemon=True
        )

        thread.start()


if __name__ == "__main__":

    start_server()

    #10.50.190.45