import os
from dotenv import load_dotenv
import requests
from pprint import PrettyPrinter

load_dotenv()
API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.freecurrencyapi.com/v1/latest"  
printer = PrettyPrinter()

def get_exchange_rates(base_currency="USD"):
    """Fetch latest exchange rates with respect to a base currency"""
    url = f"{BASE_URL}?apikey={API_KEY}&base_currency={base_currency.upper()}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['data']
    except requests.exceptions.RequestException as e:
        print("❌ Error fetching data:", e)
        return None

def list_supported_currencies():
    """Prints all supported currencies with their full names"""
    url = f"https://api.freecurrencyapi.com/v1/currencies?apikey={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()['data']
        print("✅ Supported Currencies:\n")
        for code in sorted(data):
            name = data[code]['name']
            print(f"{code} - {name}")
    except requests.exceptions.RequestException as e:
        print("❌ Error fetching supported currencies:", e)


def convert_currency(from_curr, to_curr, amount):
    """Convert amount from one currency to another"""
    rates = get_exchange_rates(from_curr)
    if rates and to_curr.upper() in rates:
        rate = rates[to_curr.upper()]
        converted_amount = round(amount * rate, 2)
        print(f"💱 {amount} {from_curr.upper()} = {converted_amount} {to_curr.upper()}")
    else:
        print("⚠️ Currency not supported or data fetch error.")

def main():
    print("💰 Welcome to Currency Converter 💰\n")

    while True:
        print("\nSelect an option:")
        print("1. List supported currencies")
        print("2. Convert currency")
        print("3. Exit")
        choice = input("Your choice: ")

        if choice == "1":
            list_supported_currencies()

        elif choice == "2":
            from_currency = input("From Currency (e.g., USD): ").strip().upper()
            to_currency = input("To Currency (e.g., INR): ").strip().upper()
            try:
                amount = float(input(f"Amount in {from_currency}: "))
                convert_currency(from_currency, to_currency, amount)
            except ValueError:
                print("❌ Please enter a valid number for amount.")

        elif choice == "3":
            print("👋 Exiting Currency Converter. Have a great day!")
            break

        else:
            print("⚠️ Invalid option. Please select again.")

if __name__ == "__main__":
    main()
