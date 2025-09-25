
import json
from datetime import datetime

class UserAccount:
    """Represents a user account with balance, holdings, and transaction history."""
    def __init__(self, user_id, username, password, email, balance=0.0):
        self.user_id = user_id
        self.username = username
        self.password = password  # In real-world, hash the password
        self.email = email
        self.balance = balance
        self.holdings = {}
        self.transactions = []

    def deposit(self, amount):
        """Deposits funds into the account."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self.transactions.append({
            'transaction_type': 'deposit',
            'amount': amount,
            'timestamp': datetime.now().isoformat()
        })

    def withdraw(self, amount):
        """Withdraws funds from the account."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self.balance < amount:
            raise ValueError("Insufficient funds.")
        self.balance -= amount
        self.transactions.append({
            'transaction_type': 'withdrawal',
            'amount': amount,
            'timestamp': datetime.now().isoformat()
        })

    def buy_shares(self, symbol, quantity, get_share_price):
        """Buys shares of a given symbol."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        share_price = get_share_price(symbol)
        cost = share_price * quantity
        if self.balance < cost:
            raise ValueError("Insufficient funds to buy shares.")

        self.balance -= cost
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        self.transactions.append({
            'transaction_type': 'buy',
            'symbol': symbol,
            'quantity': quantity,
            'price': share_price,
            'timestamp': datetime.now().isoformat()
        })

    def sell_shares(self, symbol, quantity, get_share_price):
        """Sells shares of a given symbol."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        if symbol not in self.holdings or self.holdings[symbol] < quantity:
            raise ValueError("Insufficient shares to sell.")

        share_price = get_share_price(symbol)
        proceeds = share_price * quantity
        self.balance += proceeds
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]
        self.transactions.append({
            'transaction_type': 'sell',
            'symbol': symbol,
            'quantity': quantity,
            'price': share_price,
            'timestamp': datetime.now().isoformat()
        })

    def get_portfolio_value(self, get_share_price):
        """Calculates the total value of the portfolio."""
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def get_profit_loss(self, initial_deposit):
        """Calculates the profit or loss from the initial deposit."""
        return self.get_portfolio_value(get_share_price) - initial_deposit if hasattr(self, 'get_portfolio_value') else 0 #handle case of no portfolio value yet

    def get_holdings(self):
        """Returns the current holdings."""
        return self.holdings

    def get_transaction_history(self):
        """Returns the transaction history."""
        return self.transactions

    def to_dict(self):
        """Serializes the object to a dictionary."""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'balance': self.balance,
            'holdings': self.holdings,
            'transactions': self.transactions
        }

    @classmethod
    def from_dict(cls, data):
        """Deserializes the object from a dictionary."""
        account = cls(
            user_id=data['user_id'],
            username=data['username'],
            password=data['password'],
            email=data['email'],
            balance=data['balance']
        )
        account.holdings = data['holdings']
        account.transactions = data['transactions']
        return account


class Transaction:
    """Represents a transaction.
    Note: It's included for completeness, but transactions are also stored inside UserAccount for now."""
    def __init__(self, transaction_id, user_id, share_symbol, quantity, transaction_type, timestamp=None):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.share_symbol = share_symbol
        self.quantity = quantity
        self.transaction_type = transaction_type  # 'buy' or 'sell'
        self.timestamp = timestamp or datetime.now().isoformat()

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'user_id': self.user_id,
            'share_symbol': self.share_symbol,
            'quantity': self.quantity,
            'transaction_type': self.transaction_type,
            'timestamp': self.timestamp
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            transaction_id=data['transaction_id'],
            user_id=data['user_id'],
            share_symbol=data['share_symbol'],
            quantity=data['quantity'],
            transaction_type=data['transaction_type'],
            timestamp=data['timestamp']
        )

def get_share_price(symbol):
    """Returns a fixed share price for testing purposes."""
    if symbol == 'AAPL':
        return 150.0
    elif symbol == 'TSLA':
        return 600.0
    elif symbol == 'GOOGL':
        return 2500.0
    else:
        return 100.0


if __name__ == '__main__':
    # Example Usage
    account1 = UserAccount(user_id=1, username='john_doe', password='password123', email='john@example.com', balance=1000.0)

    # Deposit
    account1.deposit(500.0)
    print(f"Balance after deposit: {account1.balance}")

    # Buy shares
    account1.buy_shares('AAPL', 5, get_share_price)
    print(f"Balance after buying 5 AAPL shares: {account1.balance}")
    print(f"Holdings: {account1.holdings}")

    # Sell shares
    account1.sell_shares('AAPL', 2, get_share_price)
    print(f"Balance after selling 2 AAPL shares: {account1.balance}")
    print(f"Holdings: {account1.holdings}")

    # Portfolio Value
    portfolio_value = account1.get_portfolio_value(get_share_price)
    print(f"Portfolio value: {portfolio_value}")

    # Profit/Loss
    profit_loss = account1.get_profit_loss(1000.0) # Initial deposit of 1000
    print(f"Profit/Loss: {profit_loss}")

    # Transaction History
    print(f"Transaction history: {account1.get_transaction_history()}")

    # Serialize to JSON
    account_dict = account1.to_dict()
    account_json = json.dumps(account_dict, indent=4)
    print(f"Serialized account: {account_json}")

    # Deserialize from JSON
    account2 = UserAccount.from_dict(json.loads(account_json))
    print(f"Deserialized account balance: {account2.balance}")
