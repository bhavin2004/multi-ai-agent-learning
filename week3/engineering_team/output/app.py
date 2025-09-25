
import gradio as gr
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
        return self.get_portfolio_value(get_share_price) - initial_deposit

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

# Gradio Interface Components
def create_account(username, password, email):
    account = UserAccount(user_id=len(accounts) + 1, username=username, password=password, email=email)
    accounts.append(account)
    return f"Account created for {username}."

def deposit_funds(user_id, amount):
    account = accounts[user_id - 1]
    account.deposit(amount)
    return f"New balance: {account.balance}"

def withdraw_funds(user_id, amount):
    account = accounts[user_id - 1]
    account.withdraw(amount)
    return f"New balance: {account.balance}"

def buy_shares(user_id, symbol, quantity):
    account = accounts[user_id - 1]
    account.buy_shares(symbol, quantity, get_share_price)
    return f"Bought {quantity} shares of {symbol}. Your holdings: {account.holdings}"

def sell_shares(user_id, symbol, quantity):
    account = accounts[user_id - 1]
    account.sell_shares(symbol, quantity, get_share_price)
    return f"Sold {quantity} shares of {symbol}. Your holdings: {account.holdings}"

def view_portfolio(user_id):
    account = accounts[user_id - 1]
    return f"Current holdings: {account.get_holdings()}. Total portfolio value: {account.get_portfolio_value(get_share_price)}"

def view_transactions(user_id):
    account = accounts[user_id - 1]
    transaction_history = account.get_transaction_history()
    return json.dumps(transaction_history, indent=4)

# Global account storage
accounts = []

# Gradio Interface layout
with gr.Blocks() as app:
    gr.Markdown("## Trading Simulation Platform - Account Management")
    
    with gr.Tab("Create Account"):
        username = gr.Textbox(label="Username")
        password = gr.Textbox(label="Password", type="password")
        email = gr.Textbox(label="Email")
        create_btn = gr.Button("Create Account")
        create_output = gr.Markdown("")
        create_btn.click(create_account, inputs=[username, password, email], outputs=create_output)

    with gr.Tab("Deposit Funds"):
        user_id_d = gr.Number(label="User ID")
        amount_d = gr.Number(label="Amount to Deposit")
        deposit_btn = gr.Button("Deposit Funds")
        deposit_output = gr.Markdown("")
        deposit_btn.click(deposit_funds, inputs=[user_id_d, amount_d], outputs=deposit_output)

    with gr.Tab("Withdraw Funds"):
        user_id_w = gr.Number(label="User ID")
        amount_w = gr.Number(label="Amount to Withdraw")
        withdraw_btn = gr.Button("Withdraw Funds")
        withdraw_output = gr.Markdown("")
        withdraw_btn.click(withdraw_funds, inputs=[user_id_w, amount_w], outputs=withdraw_output)

    with gr.Tab("Buy Shares"):
        user_id_b = gr.Number(label="User ID")
        symbol_b = gr.Textbox(label="Stock Symbol")
        quantity_b = gr.Number(label="Quantity")
        buy_btn = gr.Button("Buy Shares")
        buy_output = gr.Markdown("")
        buy_btn.click(buy_shares, inputs=[user_id_b, symbol_b, quantity_b], outputs=buy_output)

    with gr.Tab("Sell Shares"):
        user_id_s = gr.Number(label="User ID")
        symbol_s = gr.Textbox(label="Stock Symbol")
        quantity_s = gr.Number(label="Quantity")
        sell_btn = gr.Button("Sell Shares")
        sell_output = gr.Markdown("")
        sell_btn.click(sell_shares, inputs=[user_id_s, symbol_s, quantity_s], outputs=sell_output)

    with gr.Tab("View Portfolio"):
        user_id_portfolio = gr.Number(label="User ID")
        portfolio_btn = gr.Button("View Portfolio")
        portfolio_output = gr.Markdown("")
        portfolio_btn.click(view_portfolio, inputs=[user_id_portfolio], outputs=portfolio_output)

    with gr.Tab("View Transactions"):
        user_id_trans = gr.Number(label="User ID")
        transactions_btn = gr.Button("View Transactions")
        transactions_output = gr.Markdown("")
        transactions_btn.click(view_transactions, inputs=[user_id_trans], outputs=transactions_output)

app.launch()
