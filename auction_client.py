def broadcast(message, clients, clients_lock):

    with clients_lock:

        for client in clients[:]:

            try:
                client.send((message + "\n").encode())

            except:
                clients.remove(client)


def handle_client(
    conn,
    addr,
    name,
    clients,
    clients_lock,
    auction
):

    print(f"{name} connected from {addr}")

    auction.register_client(name)

    with clients_lock:

        clients.append(conn)

    # SEND WELCOME MESSAGE

    conn.send(
        auction.welcome_message(name).encode()
    )

    try:

        while True:

            menu = (
                "\nCommands:\n"
                "bid <amount>\n"
                "history\n"
                "exit\n"
            )

            conn.send(menu.encode())

            data = conn.recv(1024).decode()

            if not data:
                break

            cmd = data.strip().split()

            if not cmd:
                continue

            if cmd[0] == "bid":

                if len(cmd) != 2:

                    conn.send(
                        "Usage: bid <amount>\n".encode()
                    )

                    continue

                try:

                    price = int(cmd[1])

                except:

                    conn.send(
                        "Invalid amount\n".encode()
                    )

                    continue

                result = auction.place_bid(
                    name,
                    price
                )

                broadcast(
                    result,
                    clients,
                    clients_lock
                )

            elif cmd[0] == "history":

                message = auction.get_history()

                conn.send(message.encode())

            elif cmd[0] == "exit":

                break

            else:

                conn.send(
                    "Invalid command\n".encode()
                )

    finally:

        with clients_lock:

            if conn in clients:

                clients.remove(conn)

        conn.close()

        broadcast(
            f"{name} left the auction",
            clients,
            clients_lock
        )

        print(name, "disconnected")