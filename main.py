import requests
import random
import time
import logging
from bitcoinlib.keys import HDKey
from typing import Optional, List
import sys
import os

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BTCWalletFinder:
    def __init__(self):
        self.api_threshold = 0.8
        self.base_url = "http://localhost:5000"
        self.session = requests.Session()
        self.session.timeout = 10
        
    def get_api_status(self) -> Optional[float]:
        """Holt den aktuellen API-Status"""
        try:
            response = self.session.get(f"{self.base_url}/status")
            response.raise_for_status()
            api_usage = response.json().get("api_usage", 0)
            return api_usage
        except requests.exceptions.RequestException as e:
            logger.error(f"Fehler beim Abrufen des API-Status: {e}")
            return None

    def get_online_users(self, token: str) -> Optional[int]:
        """Holt die Anzahl der Online-Benutzer"""
        try:
            headers = {
                "X-User": "main.py", 
                "Authorization": f"Bearer {token}"
            }
            response = self.session.get(f"{self.base_url}/online_users", headers=headers)
            response.raise_for_status()
            users = response.json().get("users", 0)
            return users
        except requests.exceptions.RequestException as e:
            logger.error(f"Fehler beim Abrufen der Online-Benutzer: {e}")
            return None

    def generate_random_address(self) -> str:
        """Generiert eine zufällige Bitcoin-Adresse"""
        try:
            key = HDKey()
            return key.address()
        except Exception as e:
            logger.error(f"Fehler beim Generieren der Adresse: {e}")
            # Fallback zu einer einfachen Methode
            return self._generate_fallback_address()
    
    def _generate_fallback_address(self) -> str:
        """Fallback-Methode zur Adressgenerierung"""
        # Einfache Bitcoin-Adressgenerierung als Fallback
        chars = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        address = "1" + ''.join(random.choice(chars) for _ in range(33))
        return address

    def check_wallet_balance(self, address: str, token: str) -> Optional[float]:
        """Überprüft das Guthaben einer Wallet-Adresse"""
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = self.session.get(f"{self.base_url}/balance/{address}", headers=headers)
            response.raise_for_status()
            
            data = response.json()
            balance = data.get("balance", 0)
            return balance
        except requests.exceptions.RequestException as e:
            logger.error(f"Fehler beim Abrufen des Guthabens für {address}: {e}")
            return None

    def find_wallet_balance(self, token: str):
        """Hauptfunktion zum Finden von Wallet-Guthaben"""
        try:
            # Input-Validierung
            while True:
                try:
                    num_addresses = int(input("Anzahl der zu generierenden und zu überprüfenden Adressen eingeben: "))
                    if num_addresses > 0:
                        break
                    else:
                        print("Bitte eine positive Zahl eingeben.")
                except ValueError:
                    print("Bitte eine gültige Zahl eingeben.")
            
            filename = input("Dateiname zum Speichern der Adressen mit Guthaben eingeben: ")
            if not filename.endswith('.txt'):
                filename += '.txt'

            addresses_with_balance = []
            checked_count = 0

            print(f"\nÜberprüfe {num_addresses} Adressen...")
            
            for i in range(num_addresses):
                address = self.generate_random_address()
                balance = self.check_wallet_balance(address, token)
                
                checked_count += 1
                
                if balance is not None:
                    if balance > 0:
                        print(f"✓ {address} hat ein Guthaben von {balance} BTC!")
                        addresses_with_balance.append((address, balance))
                    else:
                        if checked_count % 100 == 0:  # Nur alle 100 Adressen anzeigen
                            print(f"Überprüft: {checked_count}/{num_addresses} Adressen...")
                else:
                    print(f"✗ Fehler beim Überprüfen von {address}")
                
                # Kurze Pause um Rate Limiting zu vermeiden
                time.sleep(0.1)

            # Ergebnisse speichern
            self._save_results(filename, addresses_with_balance)
            
            print(f"\n🎉 {len(addresses_with_balance)} Adressen mit Guthaben gefunden!")
            print(f"Ergebnisse gespeichert in: {filename}")
            
        except KeyboardInterrupt:
            print("\n\nVorgang abgebrochen.")
        except Exception as e:
            logger.error(f"Unerwarteter Fehler: {e}")

    def _save_results(self, filename: str, addresses_with_balance: List[tuple]):
        """Speichert die Ergebnisse in eine Datei"""
        try:
            with open(filename, "w", encoding='utf-8') as file:
                file.write("Bitcoin Wallet Finder - Ergebnisse\n")
                file.write("=" * 40 + "\n\n")
                
                if addresses_with_balance:
                    for address, balance in addresses_with_balance:
                        file.write(f"Adresse: {address}\n")
                        file.write(f"Guthaben: {balance} BTC\n")
                        file.write("-" * 30 + "\n")
                else:
                    file.write("Keine Adressen mit Guthaben gefunden.\n")
                    
        except IOError as e:
            logger.error(f"Fehler beim Speichern der Datei: {e}")

    def validate_token(self, token: str) -> bool:
        """Validiert ein Token"""
        try:
            headers = {"Authorization": f"Bearer {token}"}
            data = {"token": token}
            response = self.session.post(f"{self.base_url}/validate_token", 
                                       json=data, headers=headers)
            
            if response.status_code == 200:
                return response.json().get("valid", False)
            else:
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"Fehler bei der Token-Validierung: {e}")
            return False

    def show_help(self):
        """Zeigt die verfügbaren Befehle an"""
        print("\n" + "=" * 50)
        print("VERFÜGBARE BEFEHLE:")
        print("=" * 50)
        print("🔍 'find wallet' - Wallet-Guthaben suchen")
        print("📊 'status'      - API-Status anzeigen")
        print("❓ 'help'        - Diese Hilfe anzeigen")
        print("🚪 'exit'        - Programm beenden")
        print("=" * 50 + "\n")

    def show_status(self):
        """Zeigt den aktuellen Status an"""
        api_usage = self.get_api_status()
        if api_usage is not None:
            usage_percent = api_usage * 100
            print(f"\n📊 API-Status: {usage_percent:.1f}% verwendet")
            if api_usage > self.api_threshold:
                print("⚠️  Warnung: Hohe API-Nutzung!")
        else:
            print("❌ API-Status nicht verfügbar")

    def main_menu(self, token: str):
        """Hauptmenü der Anwendung"""
        print("\n" + "=" * 60)
        print("🚀 BITCOIN WALLET FINDER - AKTUALISIERT 2025")
        print("=" * 60)
        
        while True:
            try:
                online_users = self.get_online_users(token)
                if online_users is not None:
                    print(f"\n👥 Online: {online_users} Benutzer")
                else:
                    print(f"\n👥 Online: Nicht verfügbar")
                
                print("\nGeben Sie 'help' für eine Liste der Befehle ein.")
                command = input("btc-finder> ").strip().lower()

                if command == "help":
                    self.show_help()
                elif command == "find wallet":
                    self.find_wallet_balance(token)
                elif command == "status":
                    self.show_status()
                elif command == "exit":
                    print("👋 Auf Wiedersehen!")
                    break
                else:
                    print("❌ Ungültiger Befehl. Geben Sie 'help' ein für verfügbare Befehle.")
                    
            except KeyboardInterrupt:
                print("\n👋 Auf Wiedersehen!")
                break
            except Exception as e:
                logger.error(f"Fehler im Hauptmenü: {e}")
                print("❌ Ein unerwarteter Fehler ist aufgetreten.")

    def run(self):
        """Haupteinstiegspunkt der Anwendung"""
        print("🔐 Token-Eingabe erforderlich...")
        
        # Token aus Datei laden wenn verfügbar
        if os.path.exists("saved_token.txt"):
            try:
                with open("saved_token.txt", "r") as f:
                    saved_token = f.read().strip()
                if saved_token:
                    use_saved = input(f"Gespeichertes Token verwenden? (j/n): ").lower()
                    if use_saved in ['j', 'ja', 'y', 'yes']:
                        token = saved_token
                    else:
                        token = input("Neues Token eingeben: ").strip()
                else:
                    token = input("Token eingeben: ").strip()
            except:
                token = input("Token eingeben: ").strip()
        else:
            token = input("Token eingeben: ").strip()
        
        if not token:
            print("❌ Kein Token eingegeben. Programm wird beendet.")
            return
            
        print("🔍 Token wird validiert...")
        if not self.validate_token(token):
            print("❌ Ungültiges Token. Programm wird beendet.")
            return
        
        # Token speichern
        try:
            with open("saved_token.txt", "w") as f:
                f.write(token)
        except:
            pass
            
        print("✅ Token gültig!")
        self.main_menu(token)

def main():
    try:
        finder = BTCWalletFinder()
        finder.run()
    except Exception as e:
        logger.error(f"Kritischer Fehler: {e}")
        print("❌ Ein kritischer Fehler ist aufgetreten. Siehe Logs für Details.")

if __name__ == "__main__":
    main()
