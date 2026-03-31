import threading
import time


class AuctionManager:

    def __init__(self):

        self.lock = threading.Lock()

        self.items = [
            {"name": "Vintage Watch", "base_price": 200},
            {"name": "Gold Necklace", "base_price": 200},
            {"name": "Antique Vase", "base_price": 200},
            {"name": "Diamond Ring", "base_price": 200},
            {"name": "Rare Painting", "base_price": 200}
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

1) Initial Balance: $1000
2) Base price: $200
3) Higher bids only
4) Timer resets to 20 sec on every bid
5) If no bid in 20 sec → item sold
6) All balances are virtual currency
"""

    # -------------------------

    def get_current_item(self):

        item = self.items[self.current_index]

        return (
            f"\nCURRENT ITEM: {item['name']}\n"
            f"Base price: ${item['base_price']}\n"
            f"Current price: ${self.current_price}\n"
            f"Highest bidder: {self.highest_bidder}"
        )

    # -------------------------

    def place_bid(self, user, price):

        with self.lock:

            if not self.auction_running:

                return {
                    "success": False,
                    "message": "Auction not started yet"
                }

            if not isinstance(price, int) or price < 1:

                return {
                    "success": False,
                    "message": "Bid must be a positive integer"
                }

            if price <= self.current_price:

                return {
                    "success": False,
                    "message": f"Bid must be higher than ${self.current_price}"
                }

            if user not in self.balances:

                return {
                    "success": False,
                    "message": "User not registered"
                }

            if self.balances[user] < price:

                return {
                    "success": False,
                    "message": f"Insufficient balance. You have ${self.balances[user]}"
                }

            # refund previous bidder
            if self.highest_bidder and self.highest_bidder != user:

                prev = self.highest_bidder
                self.balances[prev] += self.current_price

            # deduct new bidder balance
            self.balances[user] -= price

            self.current_price = price
            self.highest_bidder = user

            # reset timer
            self.remaining_time = self.time_limit

            timestamp = time.strftime("%H:%M:%S")

            message = f"Bid placed by {user} for ${price}"

            self.history.append({
                "timestamp": timestamp,
                "user": user,
                "price": price,
                "name": self.items[self.current_index]["name"]
            })

            print(message)

            return {
                "success": True,
                "message": message,
                "balance": self.balances[user]
            }

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

        # Add complete history entry with winner
        if self.history and len(self.history) > 0:
            # Update last history entry with winner
            self.history[-1]["winner"] = winner

        message = (
            "\nITEM SOLD\n"
            f"Winner: {winner}\n"
            f"Final price: ${self.current_price}\n"
        )

        print(message)

        return message

    # -------------------------

    def move_to_next_item(self):

        self.current_index += 1

        if self.current_index >= len(self.items):

            self.auction_running = False

            return "\n====AUCTION FINISHED=====\n******Thank You******"

        self.current_price = self.items[self.current_index]["base_price"]
        self.highest_bidder = None
        self.remaining_time = self.time_limit

        item = self.items[self.current_index]

        return (
            f"\nNEXT ITEM: {item['name']}\n"
            f"Base price: ${item['base_price']}\n"
        )

    # -------------------------

    def get_history(self):

        if not self.history:

            return []

        return self.history