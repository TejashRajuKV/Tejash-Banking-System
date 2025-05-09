# -*- coding: utf-8 -*-
"""playbankingsystem.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wXyJbjCB9F03ZUYs04qGbKeYbR87sEzg
"""

import getpass
import os
import hashlib
from datetime import datetime
import pytz


TIMEZONE = 'Asia/Kolkata'
ACCOUNTS_FILE = "accounts.txt"
TRANSACTIONS_FILE = "transactions.txt"



def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_greeting():
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    hour = now.hour
    print(f"[DEBUG] Current time: {now.strftime('%Y-%m-%d %H:%M:%S')} | Hour: {hour}")

    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 16:
        return "Good afternoon"
    elif 16 <= hour < 21:
        return "Good evening"
    else:
        return "Good night"

def load_accounts():
    accounts = {}
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(",")
                if len(parts) == 4:
                    account_number, name, password, balance = parts
                    accounts[account_number] = {
                        "name": name,
                        "password": password,
                        "balance": float(balance)
                    }
    return accounts

def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as f:
        for acc_num, data in accounts.items():
            f.write(f"{acc_num},{data['name']},{data['password']},{data['balance']}\n")

def log_transaction(account_number, action, amount):
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    with open(TRANSACTIONS_FILE, "a") as f:
        f.write(f"{account_number},{action},{amount},{now}\n")



def create_account():
    accounts = load_accounts()

    name = input("Enter your name: ")
    account_number = input("Choose an account number: ")

    if account_number in accounts:
        print(" Account already exists.")
        return

    password = hash_password(getpass.getpass("Choose a password: "))

    try:
        balance = float(input("Enter initial deposit: "))
        if balance < 0:
            raise ValueError
    except ValueError:
        print("Please enter a valid non-negative number.")
        return

    accounts[account_number] = {
        "name": name,
        "password": password,
        "balance": balance
    }

    save_accounts(accounts)
    print(" Account created successfully!\n")

def login():
    accounts = load_accounts()

    account_number = input("Enter account number: ")
    password = getpass.getpass("Enter password: ")

    user = accounts.get(account_number)

    if user and user["password"] == hash_password(password):
        greeting = get_greeting()
        print(f"{greeting}, {user['name']}!\n")
        user_menu(account_number, accounts)
    else:
        print(" Invalid account number or password.\n")



def user_menu(account_number, accounts):
    while True:
        print("\n1. View Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Logout")

        choice = input("Choose an option: ")

        if choice == "1":
            print(f" Current balance: ${accounts[account_number]['balance']}")

        elif choice == "2":
            try:
                amount = float(input("Enter amount to deposit: "))
                if amount <= 0:
                    print(" Amount must be greater than zero.")
                    continue
            except ValueError:
                print(" Please enter a valid number.")
                continue

            accounts[account_number]['balance'] += amount
            save_accounts(accounts)
            log_transaction(account_number, "Deposit", amount)
            print(f" Deposit successful! Current balance: {accounts[account_number]['balance']}")
            print("(Transaction logged in transactions.txt)")

        elif choice == "3":
            try:
                amount = float(input("Enter amount to withdraw: "))
                if amount <= 0:
                    print(" Amount must be greater than zero.")
                    continue
                if amount > accounts[account_number]['balance']:
                    print(" Insufficient balance.")
                    continue
            except ValueError:
                print(" Please enter a valid number.")
                continue

            accounts[account_number]['balance'] -= amount
            save_accounts(accounts)
            log_transaction(account_number, "Withdrawal", amount)
            print(f" Withdrawal successful! Current balance: {accounts[account_number]['balance']}")
            print("(Transaction logged in transactions.txt)")

        elif choice == "4":
            print(" Logged out.\n")
            break
        else:
            print(" Invalid option. Try again.")


def main():
    greeting = get_greeting()
    print(f"\n{greeting}! Welcome to the Banking System!")

    while True:
        print("\n=== Banking System ===")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")

        option = input("Choose an option: ")

        if option == "1":
            create_account()
        elif option == "2":
            login()
        elif option == "3":
            print(" Thank you! Goodbye.")
            break
        else:
            print(" Invalid choice. Try again.")

if __name__ == "__main__":
    main()