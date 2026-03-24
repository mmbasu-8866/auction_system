import threading
import time


class AuctionManager:

    def __init__(self):

        self.lock = threading.Lock()

        self.items = [
            {"name": "Item 1", "base_price": 200},
            {"name": "Item 2", "base_price": 200},
            {"name": "Item 3", "base_price": 200},
            {"name": "Item 4", "base_price": 200},
            {"name": "Item 5", "base_price": 200}
        ]

        self.current_index = 0
        self.current_price = 200
        self.highest_bidder = None

        self.time_limit = 20
        self.remaining_time = 20

        self.auction_running = False

        self.history = []
        self.balances = {}

    # -------------------------

    def register_client(self, user):

        with self.lock:

            if user not in self.balances:

                self.balances[user] = 1000

    # -------------------------

    def welcome_message(self, user):

        return f"""
Welcome {user}!

Auction Rules:

1) Initial Balance: 1000
2) Base price: 200
3) Bid must be multiple of 10
4) Timer resets to 20 sec on every bid
5) If no bid in 20 sec → item sold
6) Command format: bid 210
"""

    # -------------------------

    def get_current_item(self):

        item = self.items[self.current_index]

        return (
            f"\nCURRENT ITEM: {item['name']}\n"
            f"Base price: 200\n"
            f"Current price: {self.current_price}\n"
            f"Highest bidder: {self.highest_bidder}"
        )

    # -------------------------

    def place_bid(self, user, price):

        with self.lock:

            if not self.auction_running:

                return "Auction not started yet"

            if price % 10 != 0:

                return "Bid must be multiple of 10"

            if price <= self.current_price:

                return (
                    f"Bid must be higher than "
                    f"{self.current_price}"
                )

            if self.balances[user] < price:

                return "Insufficient balance"

            # refund previous bidder
            if self.highest_bidder:

                prev = self.highest_bidder
                self.balances[prev] += self.current_price

            # deduct new bidder balance
            self.balances[user] -= price

            self.current_price = price
            self.highest_bidder = user

            # reset timer
            self.remaining_time = self.time_limit

            timestamp = time.strftime("%H:%M:%S")

            message = (
                "\nNEW BID RECEIVED\n\n"
                f"Bidder: {user}\n"
                f"Bid Amount: {price}\n"
                f"Remaining Balance: {self.balances[user]}\n\n"
                f"Current Highest Bidder: {self.highest_bidder}\n"
                f"Current Price: {self.current_price}\n"
            )

            self.history.append(
                f"[{timestamp}] {user} bid {price}"
            )

            print(message)

            return message

    # -------------------------

    def decrease_timer(self):

        with self.lock:

            if self.remaining_time > 0:

                self.remaining_time -= 1

    def get_time(self):

        return self.remaining_time

    # -------------------------

    def start_auction(self):

        with self.lock:

            self.auction_running = True
            self.remaining_time = self.time_limit

    # -------------------------

    def close_current_item(self):

        if self.highest_bidder:

            winner = self.highest_bidder

        else:

            winner = "No bids"

        message = (
            "\nITEM SOLD\n"
            f"Winner: {winner}\n"
            f"Final price: {self.current_price}\n"
        )

        print(message)

        return message

    # -------------------------

    def move_to_next_item(self):

        self.current_index += 1

        if self.current_index >= len(self.items):

            self.auction_running = False

            return "\n====AUCTION FINISHED=====\n******Thank You******"

        self.current_price = 200
        self.highest_bidder = None
        self.remaining_time = self.time_limit

        item = self.items[self.current_index]

        return (

            f"                          "
            f"========New Item======    "
                                    
            f"\nNEXT ITEM: {item['name']}\n"
            f"Base price: 200\n"
        )

    # -------------------------

    def get_history(self):

        if not self.history:

            return "No bids yet"

        return "\n".join(self.history)