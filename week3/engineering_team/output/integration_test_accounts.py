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
        return self.get_portfolio_value(get_share_price) - initial_deposit if hasattr(self, 'get_portfolio_value') else 0

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


# Integration Tests

import pytest

class TestUserAccount:
    @pytest.fixture
    def account(self):
        return UserAccount(user_id=1, username='john_doe', password='password123', email='john@example.com', balance=1000.0)

    def test_deposit_success(self, account):
        account.deposit(500.0)
        assert account.balance == 1500.0

    def test_deposit_negative(self, account):
        with pytest.raises(ValueError) as exc:
            account.deposit(-100)
        assert str(exc.value) == "Deposit amount must be positive."

    def test_withdraw_success(self, account):
        account.withdraw(200.0)
        assert account.balance == 800.0

    def test_withdraw_insufficient(self, account):
        with pytest.raises(ValueError) as exc:
            account.withdraw(1500)
        assert str(exc.value) == "Insufficient funds."

    def test_buy_shares_success(self, account):
        account.buy_shares('AAPL', 5, get_share_price)
        assert account.holdings['AAPL'] == 5
        assert account.balance == 750.0

    def test_buy_shares_insufficient_funds(self, account):
        with pytest.raises(ValueError) as exc:
            account.buy_shares('AAPL', 10, get_share_price)
        assert str(exc.value) == "Insufficient funds to buy shares."

    def test_sell_shares_success(self, account):
        account.buy_shares('AAPL', 5, get_share_price)
        account.sell_shares('AAPL', 2, get_share_price)
        assert account.holdings['AAPL'] == 3
        assert account.balance == 750.0 + (2 * 150.0)

    def test_sell_shares_insufficient(self, account):
        with pytest.raises(ValueError) as exc:
            account.sell_shares('AAPL', 1, get_share_price)
        assert str(exc.value) == "Insufficient shares to sell."

    def test_get_portfolio_value(self, account):
        account.buy_shares('AAPL', 5, get_share_price)
        assert account.get_portfolio_value(get_share_price) == 750.0 + (5 * 150.0)

    def test_get_profit_loss(self, account):
        initial_deposit = 1000.0
        account.buy_shares('AAPL', 5, get_share_price)
        assert account.get_profit_loss(initial_deposit) == (750.0 + (5 * 150.0)) - initial_deposit

    def test_get_holdings(self, account):
        account.buy_shares('GOOGL', 2, get_share_price)
        assert account.get_holdings() == {'GOOGL': 2}

    def test_get_transaction_history(self, account):
        account.deposit(100.0)
        assert len(account.get_transaction_history()) == 1
        assert account.get_transaction_history()[0]['transaction_type'] == 'deposit'

if __name__ == '__main__':
    pytest.main()  # For running the tests