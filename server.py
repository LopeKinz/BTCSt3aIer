from flask import Flask, jsonify, request
import redis

app = Flask(__name__)
db = redis.Redis()
import requests
import random
import string



users = 0

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

# Function to generate a random token (unchanged)
def generate_token(length=16):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

# Function to save tokens to a file (unchanged)
def save_tokens(tokens):
    with open('tokens.txt', 'w') as f:
        for token in tokens:
            f.write(token + '\n')

# Function to load tokens from a file (unchanged)
def load_tokens():
    try:
        with open('tokens.txt', 'r') as f:
            tokens = [line.strip() for line in f]
            return set(tokens)
    except FileNotFoundError:
        return set()

tokens = load_tokens()
tokens.update(generate_token() for _ in range(10))
save_tokens(tokens)

# Token validation decorator (unchanged)
def token_required(f):
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if token and token in tokens:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Invalid token"}), 401
    return decorated_function

# API usage check decorator (new)
def api_usage_check(f):
    def decorated_function(*args, **kwargs):
        api_usage = api_index / len(btc_balance_apis)
        if api_usage > 0.8:
            return jsonify({"error": "API usage limit exceeded"}), 429
        else:
            return f(*args, **kwargs)
    return decorated_function


# API status endpoint (new)
@app.route("/status")
def api_status():
    api_usage = api_index / len(btc_balance_apis)
    return jsonify({"api_usage": api_usage})

# Token validation endpoint (unchanged)
@app.route("/validate_token", methods=["POST"])
def validate_token():
    token = request.json.get("token")
    if token and token in tokens:
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False}), 401

# Token generation endpoint (unchanged)
@app.route("/generate_token", methods=["POST"])
def generate_token_endpoint():
    token = generate_token()
    tokens.add(token)
    save_tokens(tokens)
    return jsonify({"token": token})

# Balance route with API usage check (updated)
@app.route("/balance/<address>")
@token_required
@api_usage_check
def balance_route(address):
    global api_index

    retries = 3
    backoff = 1

    while retries > 0:
        try:
            url = btc_balance_apis[api_index].format(address)
            response = requests.get(url)
            data = response.json()

            if "error" in data:
                api_index = (api_index + 1) % len(btc_balance_apis)
                retries -= 1
                if retries > 0:
                    time.sleep(backoff)
                    backoff *= 2
                continue
            else:
                balance = data["balance"] / 10**8
                return jsonify({"balance": balance})

        except requests.exceptions.RequestException:
            api_index = (api_index + 1) % len(btc_balance_apis)
            retries -= 1
            if retries > 0:
                time.sleep(backoff)
                backoff *= 2
            continue

    return jsonify({"error": "Failed to fetch balance"}), 500

# Online users management endpoints (updated)
@app.teardown_request
def remove_user_online(exception=None):
    db.decr("online_users")

@app.route("/online_users", methods=["GET"])
def get_online_users():
    users = db.get("online_users") or 0
    return jsonify({"users": int(users)})

@app.route("/online_users", methods=["POST"])
def add_online_user():
    user = request.json.get("user")
    if user:
        db.incr("online_users")
        print({"message": f"{user} added to online users"})
        return jsonify({"message": f"{user} added to online users"})
    else:
        return jsonify({"error": "User not provided"}), 400
    return jsonify({"users": int(users)})


if __name__ == "__main__":
    app.run()
