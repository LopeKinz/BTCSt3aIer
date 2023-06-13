from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

online_users = set()

btc_balance_apis = [
    "https://api.blockcypher.com/v1/btc/main/addrs/{}/balance",
    "https://api.smartbit.com.au/v1/blockchain/address/{}/balance",
    "https://chain.api.btc.com/v3/address/{}",
    "https://api.blockchair.com/bitcoin/dashboards/address/{}",
    "https://api.blockexplorer.com/v1/address/{}/balance",
    "https://api.blockstream.space/api/address/{}/coins",
    "https://blockchain.info/q/addressbalance/{}",
    "https://api.walletexplorer.com/api/1/address?address={}",
    "https://api.blockchain.com/v3/address/{}/balance",
    "https://api.toshi.io/api/v0/bitcoin/addresses/{}",
    "https://bitcoin.toshi.io/api/v0/addresses/{}/balance",
    "https://blockexplorer.com/api/addr/{}/balance",
    "https://btc.bitaps.com/{}/balance",
    "https://api.btc21.org/address/{}",
    "https://www.bitstamp.net/api/v2/balance/{}/",
    "https://chain.so/api/v2/address/BTC/{}",
    "https://api.cryptoapis.io/v1/bc/btc/mainnet/address/{}/balance",
    "https://api.whatsonchain.com/v1/bsv/main/address/{}/balance",
    "https://rest.bitcoin.com/v2/address/details/{}",
    "https://api.blockcypher.com/v2/btc/main/addrs/{}/balance"
]

current_api_index = 0

@app.before_request
def check_user_online():
    user = request.headers.get("X-User")
    if user:
        online_users.add(user)

@app.teardown_request
def remove_user_online(exception=None):
    user = request.headers.get("X-User")
    if user and user in online_users:
        online_users.remove(user)

def get_balance(address):
    global current_api_index

    try:
        url = btc_balance_apis[current_api_index].format(address)
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            if current_api_index < len(btc_balance_apis) - 1:
                # Switch to the next API if available
                current_api_index += 1
                return get_balance(address)
            else:
                return jsonify({"error": data["error"]}), 404
        else:
            balance = data["balance"] / 10**8
            return jsonify({"balance": balance})
    except requests.exceptions.RequestException as e:
        if current_api_index < len(btc_balance_apis) - 1:
            # Switch to the next API if available
            current_api_index += 1
            return get_balance(address)
        else:
            return jsonify({"error": "Failed to fetch balance"}), 500

@app.route("/balance/<address>")
def balance_route(address):
    return get_balance(address)

@app.route("/version")
def version():
    return 1.0

@app.route("/online_users", methods=["GET", "POST"])
def manage_online_users():
    if request.method == "GET":
        return jsonify({"users": list(online_users)})
    elif request.method == "POST":
        user = request.json.get("user")
        if user:
            online_users.add(user)
            return jsonify({"message": f"{user} added to online users"})
        else:
            return jsonify({"error": "User not provided"}), 400

if __name__ == "__main__":
    app.run()
