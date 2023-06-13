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
    "https://api.blockcypher.com/v2/btc/main/addrs/{}/balance",
    "https://blockchair.com/bitcoin/api/address/{}",
    "https://www.blockonomics.co/api/balance?addr={}",
    "https://blockexplorer.com/api/addr/{}/utxo",
    "https://chainz.cryptoid.info/btc/api.dws?q=getbalance&a={}",
    "https://o1testnet1.minepi.com/blockchain/pi/{}",
    "https://live.blockcypher.com/btc/address/{}/",
    "https://api.bitaps.com/btc/v1/blockchain/address/{}",
    "https://api.gemini.com/v1/balances/{}/",
    "https://api.indodax.com/v2/btc_address/{}/balance",
    "https://api.luno.com/api/1/balance",
    "https://api.novadax.com/v1/account/getBalance/{}/BTC",
    "https://api.paymium.com/api/v1/users/{}/bitcoin_accounts/0/balance",
    "https://api.zebpay.com/api/v1/user/balance/{}/btc"
]


api_index = 0

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
    global api_index

    for i in range(len(btc_balance_apis)):
        try:
            url = btc_balance_apis[api_index].format(address)
            response = requests.get(url)
            data = response.json()

            if "error" in data:
                api_index = (api_index + 1) % len(btc_balance_apis)
                continue
            else:
                balance = data["balance"] / 10**8
                return jsonify({"balance": balance})
        except requests.exceptions.RequestException:
            api_index = (api_index + 1) % len(btc_balance_apis)
            continue

    return jsonify({"error": "Failed to fetch balance"}), 500

@app.route("/balance/<address>")
def balance_route(address):
    return get_balance(address)

@app.route("/version")
def version():
    return "1.0"

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
