import threading
import time


class Auction:
    """Manages bidding for a single auction item"""
    
    def __init__(self, base_price):
        self.current_bid = base_price
        self.highest_bidder = None
    
    def place_bid(self, user, amount):
        """Place a bid. Returns tuple (success, message)"""
        if amount <= self.current_bid:
            return False, f"Bid must be higher than ${self.current_bid}"
        
        # Refund previous bidder if exists
        previous_bidder = self.highest_bidder
        
        self.current_bid = amount
        self.highest_bidder = user
        
        return True, previous_bidder
    
    def end_auction(self):
        """End auction and return winner and final price"""
        return self.highest_bidder, self.current_bid
    
    def get_current_bid(self):
        return self.current_bid
    
    def get_highest_bidder(self):
        return self.highest_bidder


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
        self.auction = Auction(self.items[0]["base_price"])

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
            f"Current price: ${self.auction.get_current_bid()}\n"
            f"Highest bidder: {self.auction.get_highest_bidder()}"
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

            # Double-check auction object exists and is healthy
            if not self.auction:
                return {
                    "success": False,
                    "message": "Auction state error - try again"
                }

            # Use Auction class to validate bid amount
            success, result = self.auction.place_bid(user, price)
            
            if not success:
                return {
                    "success": False,
                    "message": result
                }

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

        winner, final_price = self.auction.end_auction()

        if not winner:

            winner = "No bids"

        else:
            # Deduct balance only from winner when auction closes
            with self.lock:
                if winner in self.balances:
                    self.balances[winner] -= final_price

        # Add complete history entry with winner
        if self.history and len(self.history) > 0:
            # Update last history entry with winner
            self.history[-1]["winner"] = winner
            self.history[-1]["final_price"] = final_price

        message = (
            "\nITEM SOLD\n"
            f"Winner: {winner}\n"
            f"Final price: ${final_price}\n"
        )

        print(message)

        return {"winner": winner, "final_price": final_price, "message": message}

    # -------------------------

    def move_to_next_item(self):

        with self.lock:
            self.current_index += 1

            if self.current_index >= len(self.items):

                self.auction_running = False

                return "\n====AUCTION FINISHED=====\n******Thank You******"

            # Create new Auction instance for the next item
            self.auction = Auction(self.items[self.current_index]["base_price"])
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