from flask import Flask, jsonify, request
import requests
import random
import string
import time
import logging
from functools import wraps
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Globale Variablen
online_users = 0
api_request_count = 0
last_reset_time = datetime.now()
user_sessions = {}  # Token -> letzte Aktivität

# Aktualisierte und funktionsfähige Bitcoin API Endpunkte
btc_balance_apis = [
    {
        "url": "https://blockchain.info/q/addressbalance/{}",
        "response_key": None,  # Direkte Antwort in Satoshi
        "divisor": 100000000
    },
    {
        "url": "https://blockstream.info/api/address/{}/coins",
        "response_key": "address.chain_stats.funded_txo_sum",
        "divisor": 100000000
    },
    {
        "url": "https://api.blockcypher.com/v1/btc/main/addrs/{}/balance",
        "response_key": "balance",
        "divisor": 100000000
    },
    {
        "url": "https://api.blockchair.com/bitcoin/dashboards/address/{}",
        "response_key": "data.{}.address.balance",
        "divisor": 100000000
    },
    {
        "url": "https://chain.api.btc.com/v3/address/{}",
        "response_key": "data.balance",
        "divisor": 100000000
    },
    {
        "url": "https://mempool.space/api/address/{}",
        "response_key": "chain_stats.funded_txo_sum",
        "divisor": 100000000
    }
]

current_api_index = 0

class TokenManager:
    def __init__(self):
        self.tokens_file = 'tokens.txt'
        self.tokens = self.load_tokens()
        if not self.tokens:
            self.generate_initial_tokens()
    
    def generate_token(self, length: int = 32) -> str:
        """Generiert einen sicheren Token"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def generate_initial_tokens(self):
        """Generiert initiale Tokens"""
        logger.info("Generiere initiale Tokens...")
        for _ in range(10):
            token = self.generate_token()
            self.tokens.add(token)
        self.save_tokens()
    
    def save_tokens(self):
        """Speichert Tokens in Datei"""
        try:
            with open(self.tokens_file, 'w') as f:
                for token in self.tokens:
                    f.write(token + '\n')
            logger.info(f"{len(self.tokens)} Tokens gespeichert")
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Tokens: {e}")
    
    def load_tokens(self) -> set:
        """Lädt Tokens aus Datei"""
        try:
            if os.path.exists(self.tokens_file):
                with open(self.tokens_file, 'r') as f:
                    tokens = {line.strip() for line in f if line.strip()}
                logger.info(f"{len(tokens)} Tokens geladen")
                return tokens
        except Exception as e:
            logger.error(f"Fehler beim Laden der Tokens: {e}")
        return set()
    
    def is_valid(self, token: str) -> bool:
        """Überprüft ob Token gültig ist"""
        return token in self.tokens
    
    def add_token(self, token: str):
        """Fügt neuen Token hinzu"""
        self.tokens.add(token)
        self.save_tokens()

# Token Manager initialisieren
token_manager = TokenManager()

def clean_bearer_token(token: str) -> str:
    """Entfernt 'Bearer ' Präfix falls vorhanden"""
    if token and token.startswith('Bearer '):
        return token[7:]
    return token or ""

def token_required(f):
    """Decorator für Token-Validierung"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        token = clean_bearer_token(auth_header)
        
        if not token or not token_manager.is_valid(token):
            logger.warning(f"Ungültiger Token-Versuch: {token[:10]}...")
            return jsonify({"error": "Ungültiges oder fehlendes Token"}), 401
        
        # Benutzer-Session aktualisieren
        update_user_session(token)
        return f(*args, **kwargs)
    return decorated_function

def api_usage_check(f):
    """Decorator für API-Nutzungsüberwachung"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        global api_request_count, last_reset_time
        
        # Stündliche Zurücksetzung der API-Zähler
        now = datetime.now()
        if now - last_reset_time > timedelta(hours=1):
            api_request_count = 0
            last_reset_time = now
            logger.info("API-Zähler zurückgesetzt")
        
        api_usage = api_request_count / 1000  # Limit auf 1000 Anfragen pro Stunde
        
        if api_usage > 0.9:
            logger.warning(f"API-Limit fast erreicht: {api_usage:.2%}")
            return jsonify({"error": "API-Nutzungslimit fast erreicht. Bitte später versuchen."}), 429
        
        api_request_count += 1
        return f(*args, **kwargs)
    return decorated_function

def update_user_session(token: str):
    """Aktualisiert die Benutzer-Session"""
    global user_sessions
    user_sessions[token] = datetime.now()

def cleanup_old_sessions():
    """Entfernt alte Sessions"""
    global user_sessions, online_users
    cutoff_time = datetime.now() - timedelta(minutes=5)
    old_tokens = [token for token, last_seen in user_sessions.items() if last_seen < cutoff_time]
    
    for token in old_tokens:
        del user_sessions[token]
    
    online_users = len(user_sessions)

def get_btc_balance(address: str) -> Optional[float]:
    """Holt Bitcoin-Guthaben von verschiedenen APIs"""
    global current_api_index
    
    for attempt in range(len(btc_balance_apis)):
        api_config = btc_balance_apis[current_api_index]
        
        try:
            url = api_config["url"].format(address)
            logger.debug(f"Versuche API {current_api_index}: {url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                if api_config["response_key"] is None:
                    # Direkte Antwort (wie blockchain.info)
                    try:
                        balance_satoshi = int(response.text.strip())
                        balance_btc = balance_satoshi / api_config["divisor"]
                        logger.debug(f"Erfolgreich von API {current_api_index}: {balance_btc} BTC")
                        return balance_btc
                    except ValueError:
                        logger.warning(f"Ungültige Antwort von API {current_api_index}")
                else:
                    # JSON-Antwort
                    try:
                        data = response.json()
                        
                        # Navigiere durch verschachtelte Keys
                        key_path = api_config["response_key"]
                        if "{}" in key_path:
                            key_path = key_path.format(address)
                        
                        balance_satoshi = data
                        for key in key_path.split('.'):
                            if key in balance_satoshi:
                                balance_satoshi = balance_satoshi[key]
                            else:
                                raise KeyError(f"Key '{key}' nicht gefunden")
                        
                        balance_btc = float(balance_satoshi) / api_config["divisor"]
                        logger.debug(f"Erfolgreich von API {current_api_index}: {balance_btc} BTC")
                        return balance_btc
                    except (KeyError, ValueError, TypeError) as e:
                        logger.warning(f"Fehler beim Parsen der Antwort von API {current_api_index}: {e}")
            else:
                logger.warning(f"API {current_api_index} antwortete mit Status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"Anfrage-Fehler bei API {current_api_index}: {e}")
        
        # Zur nächsten API wechseln
        current_api_index = (current_api_index + 1) % len(btc_balance_apis)
        time.sleep(0.5)  # Kurze Pause zwischen API-Versuchen
    
    logger.error(f"Alle APIs fehlgeschlagen für Adresse: {address}")
    return None

# API Endpunkte

@app.route("/status")
def api_status():
    """API-Status Endpunkt"""
    cleanup_old_sessions()
    
    api_usage = api_request_count / 1000  # Basierend auf 1000 Anfragen pro Stunde
    
    status_info = {
        "api_usage": min(api_usage, 1.0),  # Maximal 1.0
        "online_users": online_users,
        "current_api": current_api_index,
        "total_apis": len(btc_balance_apis),
        "requests_this_hour": api_request_count,
        "timestamp": datetime.now().isoformat()
    }
    
    return jsonify(status_info)

@app.route("/validate_token", methods=["POST"])
def validate_token():
    """Token-Validierung Endpunkt"""
    try:
        auth_header = request.headers.get("Authorization", "")
        token = clean_bearer_token(auth_header)
        
        # Auch aus JSON Body prüfen als Fallback
        json_data = request.get_json() or {}
        if not token:
            token = json_data.get("token", "")
        
        is_valid = token_manager.is_valid(token)
        
        if is_valid:
            update_user_session(token)
            logger.info(f"Token erfolgreich validiert: {token[:10]}...")
        else:
            logger.warning(f"Token-Validierung fehlgeschlagen: {token[:10]}...")
        
        return jsonify({"valid": is_valid})
    
    except Exception as e:
        logger.error(f"Fehler bei Token-Validierung: {e}")
        return jsonify({"valid": False}), 500

@app.route("/generate_token", methods=["POST"])
def generate_token_endpoint():
    """Token-Generierung Endpunkt"""
    try:
        token = token_manager.generate_token()
        token_manager.add_token(token)
        
        logger.info(f"Neuer Token generiert: {token[:10]}...")
        return jsonify({"token": token})
    
    except Exception as e:
        logger.error(f"Fehler bei Token-Generierung: {e}")
        return jsonify({"error": "Token-Generierung fehlgeschlagen"}), 500

@app.route("/balance/<address>")
@token_required
@api_usage_check
def balance_route(address: str):
    """Bitcoin-Guthaben Endpunkt"""
    try:
        # Einfache Adressvalidierung
        if not address or len(address) < 26 or len(address) > 62:
            return jsonify({"error": "Ungültige Bitcoin-Adresse"}), 400
        
        logger.info(f"Guthaben-Anfrage für Adresse: {address}")
        
        balance = get_btc_balance(address)
        
        if balance is not None:
            return jsonify({
                "address": address,
                "balance": balance,
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "error": "Guthaben konnte nicht abgerufen werden",
                "address": address
            }), 503
    
    except Exception as e:
        logger.error(f"Fehler beim Abrufen des Guthabens für {address}: {e}")
        return jsonify({"error": "Interner Server-Fehler"}), 500

@app.route("/online_users", methods=["GET"])
@token_required
def get_online_users():
    """Online-Benutzer abrufen"""
    cleanup_old_sessions()
    return jsonify({"users": online_users})

@app.route("/online_users", methods=["POST"])
@token_required  
def add_online_user():
    """Benutzer als online markieren"""
    try:
        auth_header = request.headers.get("Authorization", "")
        token = clean_bearer_token(auth_header)
        
        update_user_session(token)
        cleanup_old_sessions()
        
        return jsonify({
            "message": "Benutzer als online markiert",
            "users": online_users
        })
    
    except Exception as e:
        logger.error(f"Fehler beim Hinzufügen des Online-Benutzers: {e}")
        return jsonify({"error": "Interner Server-Fehler"}), 500

@app.route("/health")
def health_check():
    """Gesundheitscheck Endpunkt"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpunkt nicht gefunden"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Interner Server-Fehler"}), 500

if __name__ == "__main__":
    logger.info("Bitcoin Wallet Finder Server wird gestartet...")
    logger.info(f"Server läuft mit {len(btc_balance_apis)} Bitcoin APIs")
    logger.info(f"{len(token_manager.tokens)} Tokens verfügbar")
    
    # Entwicklungsmodus mit Debug
    app.run(debug=True, host='127.0.0.1', port=5000)
