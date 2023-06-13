import requests
import random
import pycoin
from blockstream import blockstream_client
def get_online_users():
    try:
        url = "http://localhost:5000/online_users"
        response = requests.get(url, headers={"X-User": "main.py"})
        
        if response.status_code == 200:
            users = response.json()["users"]
            return(len(users))
        else:
            return "Error"
    except requests.exceptions.RequestException as e:
        return "Error"

def generate_random_address():
    secret_exponent = random.randint(1, pycoin.ecdsa.secp256k1.generator.order())
    wif = pycoin.key.Key(secret_exponent=secret_exponent).wif()
    return wif_to_address(wif)

def wif_to_address(wif):
    key = pycoin.key.Key.from_text(wif)
    return key.address()

def find_wallet_balance():
    blockstream = blockstream_client.Client()

    num_addresses = int(input("Enter the number of addresses to generate and check: "))
    filename = input("Enter the filename to save the addresses with balance: ")

    addresses_with_balance = []

    for _ in range(num_addresses):
        address = generate_random_address()
        balance = blockstream.get_address(address)["chain_stats"]["funded_txo_sum"]

        if balance > 0:
            addresses_with_balance.append(address)

    with open(filename, "w") as file:
        for address in addresses_with_balance:
            file.write(address + "\n")

    print(f"{len(addresses_with_balance)} addresses with balance found. Saved to {filename}.")



def main():
    print("Bitcoin Wallet Finder")
    print(f"---Online:-{get_online_users()}-------")
    print("Enter 'help' for a list of commands.")

    while True:
        command = input("> ")

        if command == "help":
            print("Commands:")
            print("- find wallet <address>")
            print("- exit")
        elif command.startswith("find wallet"):
            _, _, address = command.split()
            find_wallet_balance(address)
        elif command == "exit":
            break
        else:
            print("Invalid command. Enter 'help' for a list of commands.")

if __name__ == "__main__":
    main()


#gets edited but does the job rn
