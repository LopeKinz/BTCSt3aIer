import requests
import random
from bitcoinlib.keys import HDKey
import time

API_THRESHOLD = 0.8
API_STATUS_URL = "http://localhost:5000/status"

def get_api_status():
    try:
        response = requests.get(API_STATUS_URL)
        if response.status_code == 200:
            api_usage = response.json()["api_usage"]
            return api_usage
        else:
            return "Error"
    except requests.exceptions.RequestException as e:
        return "Error"

def get_online_users(token):
    # ...

    try:
        url = "http://localhost:5000/online_users"
        headers = {"X-User": "main.py", "Authorization": token}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            users = response.json()["users"]
            return users
        else:
            return "Error"
    except requests.exceptions.RequestException as e:
        return "Error"
    

def generate_random_address():
    key = HDKey()
    address = key.address()
    return address

def find_wallet_balance(token):
    num_addresses = int(input("Enter the number of addresses to generate and check: "))
    filename = input("Enter the filename to save the addresses with balance: ")

    addresses_with_balance = []

    for _ in range(num_addresses):
        address = generate_random_address()
        headers = {"Authorization": token}
        url = f"http://localhost:5000/balance/{address}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            balance = data.get("balance")
            print(f"Checked {address} and has 0 Balance!")
            if balance and balance > 0:
                addresses_with_balance.append(address)

    with open(filename, "w") as file:
        for address in addresses_with_balance:
            file.write(address + "\n")

    print(f"{len(addresses_with_balance)} addresses with balance found. Saved to {filename}.")

def validate_token(token):
    headers = {"Authorization": token}
    url = "http://localhost:5000/validate_token"
    response = requests.post(url, json={"token": token}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        valid = data.get("valid")
        return valid
    else:
        return False

def main_menu(token):
    print("Bitcoin Wallet Finder")
    while True:
        online_users = get_online_users(token)
        print(f"---Online: {online_users} users---")

        if online_users is not None:
            print("Enter 'help' for a list of commands.")

            command = input("> ")

            if command == "help":
                print("Commands:")
                print("- find wallet <address>")
                print("- exit")
            elif command.startswith("find wallet"):
                find_wallet_balance(token)
            elif command == "exit":
                break
            else:
                print("Invalid command. Enter 'help' for a list of commands.")

        time.sleep(1)

def main():
    token = input("Enter your token: ")
    if not validate_token(token):
        print("Invalid token. Exiting...")
        exit()
    main_menu(token)

if __name__ == "__main__":
    main()

