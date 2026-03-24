import threading
import time
import sys


# ----------------------------------------
# Broadcast helper
# ----------------------------------------

def broadcast(message, clients, clients_lock):

    with clients_lock:

        for client in clients[:]:

            try:

                client.send(
                    (message + "\n").encode()
                )

            except:

                clients.remove(client)


# ----------------------------------------
# Timer loop
# ----------------------------------------

def timer_loop(auction, clients, clients_lock):

    print("\nServer started.")
    print("Preparing auction...\n")

    # -----------------------------
    # START BUFFER — 60 sec
    # -----------------------------

    for remaining in range(120, 0, -1):

        message = f"START_COUNTDOWN {remaining}"

        print(
            f"\rAuction starts in: {remaining} sec",
            end="",
            flush=True
        )

        broadcast(
            message,
            clients,
            clients_lock
        )

        time.sleep(1)

    print("\n")

    # -----------------------------
    # START AUCTION
    # -----------------------------

    auction.start_auction()

    start_message = (
        "\n==============================\n"
        "      AUCTION STARTED\n"
        "==============================\n"
    )

    print(start_message)

    broadcast(
        start_message,
        clients,
        clients_lock
    )

    first_item = auction.get_current_item()

    print(first_item)

    broadcast(
        first_item,
        clients,
        clients_lock
    )

    # Broadcast initial timer

    broadcast(
        f"TIMER {auction.get_time()}",
        clients,
        clients_lock
    )

    # -----------------------------
    # MAIN AUCTION LOOP
    # -----------------------------

    while True:

        time.sleep(1)

        if not auction.auction_running:

            continue

        auction.decrease_timer()

        remaining = auction.get_time()

        # Update server timer line

        print(
            f"\rTime remaining: {remaining} sec",
            end="",
            flush=True
        )

        # Broadcast timer to clients

        broadcast(
            f"TIMER {remaining}",
            clients,
            clients_lock
        )

        # -------------------------
        # ITEM SOLD
        # -------------------------

        if remaining == 0:

            print("\n")

            winner_message = (
                auction.close_current_item()
            )

            broadcast(
                winner_message,
                clients,
                clients_lock
            )

            next_item = (
                auction.move_to_next_item()
            )

            print(next_item)

            broadcast(
                next_item,
                clients,
                clients_lock
            )

            # Broadcast new timer

            broadcast(
                f"TIMER {auction.get_time()}",
                clients,
                clients_lock
            )


# ----------------------------------------
# Start timer thread
# ----------------------------------------

def start_timer(auction, clients, clients_lock):

    thread = threading.Thread(
        target=timer_loop,
        args=(
            auction,
            clients,
            clients_lock
        ),
        daemon=True
    )

    thread.start()

    print("Timer thread started.")