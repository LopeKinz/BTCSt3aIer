import requests

def get_online_users():
    try:
        url = "http://localhost:5000/online_users"
        response = requests.get(url, headers={"X-User": "main.py"})
        
        if response.status_code == 200:
            users = response.json()["users"]
            print("Currently online users:")
            for user in users:
                print(user)
        else:
            print("Error: Failed to fetch online users.")
    except requests.exceptions.RequestException as e:
        print("Error: Failed to fetch online users.")

def find_wallet_balance(address):
    try:
        url = f"http://localhost:5000/balance/{address}"
        response = requests.get(url, headers={"X-User": "main.py"})

        if response.status_code == 200:
            balance = response.json()["balance"]
            print(f"The balance of {address} is {balance} BTC")
        else:
            print("Error: Failed to fetch the balance.")
    except requests.exceptions.RequestException as e:
        print("Error: Failed to fetch the balance.")

def main():
    print("Bitcoin Wallet Finder")
    print("---------------------")

    while True:
        print("\nMenu:")
        print("1. Find wallet balance")
        print("2. Get online users")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            address = input("Enter the Bitcoin address: ")
            find_wallet_balance(address)
        elif choice == "2":
            get_online_users()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


#gets edited but does the job rn
