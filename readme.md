# 🚀 BTCSt3aIer - Bitcoin Wallet Finder (2025 Update)

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/github/license/lopekinz/BTCSt3aIer" alt="License">
  <img src="https://img.shields.io/badge/Status-Updated%202025-green.svg" alt="Status">
  <img src="https://img.shields.io/badge/Version-2.0.0-orange.svg" alt="Version">
</p>

<p align="center">
  <strong>Ein leistungsstarker Bitcoin Wallet Balance Checker mit modernisiertem Code, verbesserter Fehlerbehandlung und aktualisierten APIs.</strong>
</p>

## 🎯 Was ist neu in Version 2.0.0?

### ✅ Behobene Probleme
- ✅ **Online Users Funktionalität**: Vollständig repariert und funktionsfähig
- ✅ **Token-Validierung**: Robuste Token-Validierung ohne Bugs
- ✅ **API-Endpunkte**: Alle Bitcoin APIs aktualisiert und funktionsfähig
- ✅ **Fehlerbehandlung**: Verbesserte Fehlerbehandlung und Logging
- ✅ **Code-Qualität**: Modernisierter Python-Code mit Typen-Hints

### 🚀 Neue Features
- 🔒 **Sicherheit**: Verbesserte Token-Sicherheit
- 📊 **Status-Dashboard**: Detaillierte API-Status-Informationen
- 💾 **Token-Speicherung**: Automatisches Speichern und Laden von Tokens
- 🎨 **Bessere UI**: Farbige Konsolen-Ausgabe und bessere Benutzerführung
- ⚡ **Performance**: Optimierte API-Aufrufe und Rate-Limiting
- 🔄 **Auto-Fallback**: Automatisches Wechseln zwischen APIs bei Ausfällen

## 🛠️ Installation

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)

### Schritt-für-Schritt Installation

1. **Repository klonen oder herunterladen**
   ```bash
   git clone https://github.com/lopekinz/BTCSt3aIer.git
   cd BTCSt3aIer
   ```

2. **Virtuelle Umgebung erstellen (empfohlen)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\\Scripts\\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Abhängigkeiten installieren**
   ```bash
   pip install -r requirements.txt
   ```

4. **Server starten**
   ```bash
   python server.py
   ```
   Der Server läuft nun auf `http://localhost:5000`

5. **Client starten (neues Terminal)**
   ```bash
   python main.py
   ```

## 🎮 Verwendung

### Erste Schritte

1. **Server starten**: Führen Sie zuerst `python server.py` aus
2. **Client starten**: Führen Sie in einem neuen Terminal `python main.py` aus
3. **Token eingeben**: Beim ersten Start wird ein Token automatisch generiert
4. **Befehle verwenden**: Nutzen Sie die verfügbaren Befehle

### Verfügbare Befehle

```bash
🔍 'find wallet' - Wallet-Guthaben suchen
📊 'status'      - API-Status anzeigen  
❓ 'help'        - Hilfe anzeigen
🚪 'exit'        - Programm beenden
```

### Beispiel-Session

```bash
btc-finder> find wallet
Anzahl der zu generierenden Adressen eingeben: 100
Dateiname zum Speichern eingeben: ergebnisse.txt

Überprüfe 100 Adressen...
Überprüft: 100/100 Adressen...
🎉 0 Adressen mit Guthaben gefunden!
Ergebnisse gespeichert in: ergebnisse.txt
```

## 🔧 Konfiguration

### API-Konfiguration
Die Anwendung nutzt mehrere Bitcoin-APIs für maximale Zuverlässigkeit:
- Blockchain.info
- Blockstream.info  
- BlockCypher
- Blockchair.com
- BTC.com
- Mempool.space

### Token-Management
- Tokens werden automatisch generiert und in `tokens.txt` gespeichert
- Benutzer-Tokens werden in `saved_token.txt` für Wiederverwendung gespeichert
- Token sind 32 Zeichen lang und kryptographisch sicher

## 📊 API-Endpunkte

### Server-Endpunkte
- `GET /status` - API-Status und Statistiken
- `POST /validate_token` - Token-Validierung
- `POST /generate_token` - Neuen Token generieren
- `GET /balance/<address>` - Bitcoin-Guthaben abrufen
- `GET /online_users` - Online-Benutzer Anzahl
- `GET /health` - Server-Gesundheitscheck

## 🚨 Wichtige Hinweise

### ⚠️ Warnungen
- **Realistische Erwartungen**: Bitcoin-Adressen mit Guthaben zu finden ist extrem unwahrscheinlich
- **Bildungszweck**: Diese Software ist primär für Bildungs- und Forschungszwecke gedacht
- **Rate Limiting**: Respektieren Sie die API-Limits der verwendeten Services
- **Kostenlos**: Falls Sie für diese Software bezahlt haben, wurden Sie betrogen!

### 🔒 Sicherheit
- Teilen Sie Ihre Tokens nicht mit anderen
- Verwenden Sie die Software nur für legale Zwecke
- Die Software sammelt keine persönlichen Daten

## 🐛 Fehlerbehebung

### Häufige Probleme

**Problem**: Server startet nicht
```bash
# Lösung: Prüfen Sie ob Port 5000 frei ist
netstat -ano | findstr :5000
```

**Problem**: Token-Validierung schlägt fehl
```bash
# Lösung: Löschen Sie saved_token.txt und starten Sie neu
del saved_token.txt
python main.py
```

**Problem**: Alle APIs schlagen fehl
```bash
# Lösung: Prüfen Sie Ihre Internetverbindung
python -c "import requests; print(requests.get('https://google.com').status_code)"
```

## 📈 Performance-Tipps

1. **Moderate Anzahl**: Verwenden Sie nicht mehr als 1000 Adressen pro Durchgang
2. **Pausen einlegen**: Bei häufiger Nutzung Pausen zwischen den Sessions einlegen
3. **Lokaler Server**: Verwenden Sie immer den lokalen Server für beste Performance

## 🤝 Beitrag leisten

Verbesserungsvorschläge und Bug-Reports sind willkommen! 

### Development Setup
```bash
# Entwicklungs-Abhängigkeiten installieren
pip install pytest pytest-flask black flake8

# Tests ausführen
pytest

# Code formatieren
black *.py
```

## 📄 Lizenz

Dieses Projekt steht unter der [MIT License](LICENSE).

## 📞 Support

- **E-Mail**: pinkyhax@gmail.com
- **Issues**: GitHub Issues verwenden
- **Kostenlos**: Diese Software ist und bleibt kostenlos!

## 🙏 Danksagungen

- Bitcoin-Community für die APIs
- Alle Contributor und Tester
- Open-Source-Libraries die verwendet werden

---

<p align="center">
  <strong>⭐ Falls diese Software hilfreich war, hinterlassen Sie einen Stern! ⭐</strong>
</p>

<p align="center">
  <em>Entwickelt mit ❤️ für die Bitcoin-Community</em>
</p>
