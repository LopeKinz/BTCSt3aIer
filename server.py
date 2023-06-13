#work in progress
from flask import Flask, jsonify, request

app = Flask(__name__)

online_users = set()

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

@app.route("/balance/<address>")
def get_balance(address):
    try:
        url = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance"
        response = requests.get(url)
        data = response.json()
        
        if "error" in data:
            return jsonify({"error": data["error"]}), 404
        else:
            balance = data["balance"] / 10**8
            return jsonify({"balance": balance})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch balance"}), 500

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
