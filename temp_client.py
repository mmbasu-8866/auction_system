import socket
import threading
import sys

PORT = 5555

auction_started = False


def receive_messages(client):

    global auction_started

    while True:

        try:

            message = client.recv(1024).decode()

            if not message:
                break

            # -------------------------
            # PRE-AUCTION COUNTDOWN
            # -------------------------

            if message.startswith("START_COUNTDOWN"):

                if not auction_started:

                    seconds = message.split()[1]

                    sys.stdout.write(
                        f"\rAuction starts in: {seconds} sec   "
                    )

                    sys.stdout.flush()

                continue

            # -------------------------
            # AUCTION STARTED
            # -------------------------

            if "AUCTION STARTED" in message:

                auction_started = True

                print("\n" + message)

                print(
                    "\nTime limit per round: 20 sec\n"
                )

                continue

            # -------------------------
            # IGNORE RUNTIME TIMER
            # -------------------------

            if message.startswith("TIMER"):

                continue

            # -------------------------
            # NORMAL MESSAGE
            # -------------------------

            print("\n" + message)

        except:

            break


def start_client():

    host = input("Enter server IP: ").strip()

    client = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        client.connect((host, PORT))

    except Exception as e:

        print("Unable to connect to server:", e)

        return

    # Receive initial server prompt

    try:

        message = client.recv(1024).decode()

        print(message)

    except:

        print("Failed to receive server prompt.")

        client.close()

        return

    # Enter name

    name = input().strip()

    client.send(name.encode())

    print("\nConnected to auction server.\n")

    thread = threading.Thread(
        target=receive_messages,
        args=(client,),
        daemon=True
    )

    thread.start()

    while True:

        try:

            command = input("> ").strip()

            if not command:
                continue

            client.send(command.encode())

            if command.lower() == "exit":
                break

        except KeyboardInterrupt:

            break

    client.close()

    print("Client closed.")


if __name__ == "__main__":

    start_client()