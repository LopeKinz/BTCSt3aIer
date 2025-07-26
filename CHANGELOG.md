# CHANGELOG - Bitcoin Wallet Finder

## Version 2.0.0 (Juli 2025) - Große Aktualisierung

### 🎉 Hauptverbesserungen

#### ✅ Behobene Probleme aus Version 1.0
- **Online Users Funktionalität**: Komplett neu implementiert mit Session-Management
- **Token-Validierung**: Robuste Validierung mit Bearer Token Support
- **API-Endpunkte**: Alle Bitcoin APIs auf aktuelle, funktionierende Endpunkte aktualisiert
- **Redis-Abhängigkeit**: Entfernt, jetzt ohne externe Datenbank

#### 🚀 Neue Features
- **Moderne Code-Struktur**: OOP-Design mit BTCWalletFinder Klasse
- **Verbessertes Logging**: Detaillierte Logs für Debugging
- **Token-Speicherung**: Automatisches Speichern/Laden von Tokens
- **Bessere UI**: Emojis und farbige Ausgaben für bessere UX
- **Error Handling**: Robuste Fehlerbehandlung mit Fallback-Mechanismen
- **Rate Limiting**: Intelligentes API-Rate-Limiting mit automatischem Reset
- **Health Checks**: Server-Gesundheitsüberwachung
- **Session Management**: Automatisches Cleanup alter Sessions

### 🔧 Technische Verbesserungen

#### API-System
- **6 aktuelle Bitcoin APIs**: Blockchain.info, Blockstream.info, BlockCypher, etc.
- **Auto-Fallback**: Automatisches Wechseln bei API-Ausfällen
- **Smart Retry**: Intelligente Wiederholungslogik
- **Response Parsing**: Robustes Parsing verschiedener API-Antworten

#### Sicherheit
- **32-Zeichen Tokens**: Kryptographisch sichere Token-Generierung
- **Bearer Token Support**: Moderne Authorization Headers
- **Input Validation**: Validierung aller Eingaben
- **Session Timeouts**: Automatisches Cleanup nach 5 Minuten Inaktivität

#### Code-Qualität
- **Type Hints**: Vollständige Typisierung für bessere IDE-Unterstützung
- **Documentation**: Ausführliche Docstrings und Kommentare
- **Error Messages**: Benutzerfreundliche deutsche Fehlermeldungen
- **Modular Design**: Saubere Trennung von Verantwortlichkeiten

### 📦 Neue Dateien
- `requirements.txt` - Aktualisierte Abhängigkeiten
- `setup.bat` - Automatisches Setup-Script
- `start_server.bat` - Server-Starter
- `start_client.bat` - Client-Starter
- `CHANGELOG.md` - Diese Datei

### 🔄 Aktualisierte Dependencies
- Flask 3.0.0 (vorher 2.x)
- requests 2.31.0 (aktuell)
- bitcoinlib 0.12.0 (aktuell)
- Neue: validators, colorama, tabulate

### 📊 Performance-Verbesserungen
- **Session Pooling**: Wiederverwendung von HTTP-Verbindungen
- **Smart Caching**: Intelligente Token-Validierung
- **Optimized Timeouts**: 10s Timeouts für bessere Responsivität
- **Memory Management**: Automatisches Cleanup alter Sessions

### 🛠️ Verbesserter Workflow
1. `setup.bat` ausführen für einfache Installation
2. `start_server.bat` für Server
3. `start_client.bat` für Client
4. Automatische Token-Verwaltung

### 🐛 Behobene Bugs
- Online Users Counter zeigt jetzt korrekte Werte
- Token-Validierung funktioniert zuverlässig
- API-Endpunkte sind alle funktionsfähig
- Redis-Dependency-Fehler behoben
- Memory Leaks bei Sessions behoben
- Unicode-Handling in Dateien verbessert

### ⚠️ Breaking Changes
- **Python 3.8+** jetzt erforderlich (vorher 3.6+)
- **Neue Token-Format**: 32 Zeichen statt 16
- **API-Änderungen**: Neue Endpunkt-URLs
- **Config-Änderungen**: Redis nicht mehr erforderlich

### 🎯 Kompatibilität
- ✅ Windows 10/11
- ✅ Python 3.8, 3.9, 3.10, 3.11, 3.12
- ✅ Alle modernen Browser für API-Testing
- ❌ Python < 3.8 nicht mehr unterstützt

---

## Version 1.0.0 (2023) - Original Release

### Features
- Grundlegende Bitcoin Wallet Balance Checking
- Flask-basierte API
- Token-basierte Authentifizierung
- Multiple Bitcoin API Integration
- Redis für Online Users Tracking

### Probleme (behoben in 2.0.0)
- Online Users Funktionalität defekt
- Token-Validierung unzuverlässig
- Veraltete API-Endpunkte
- Fehlende Error Handling
- Redis-Dependency Probleme
