@echo off
echo ========================================
echo Bitcoin Wallet Finder - Setup Script
echo ========================================
echo.

echo [1/4] Überprüfe Python-Installation...
python --version
if %errorlevel% neq 0 (
    echo FEHLER: Python ist nicht installiert oder nicht im PATH!
    echo Bitte installieren Sie Python 3.8+ von https://python.org
    pause
    exit /b 1
)

echo [2/4] Erstelle virtuelle Umgebung...
python -m venv venv
if %errorlevel% neq 0 (
    echo FEHLER: Konnte virtuelle Umgebung nicht erstellen!
    pause
    exit /b 1
)

echo [3/4] Aktiviere virtuelle Umgebung...
call venv\Scripts\activate.bat

echo [4/4] Installiere Abhängigkeiten...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo FEHLER: Installation der Abhängigkeiten fehlgeschlagen!
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ Setup erfolgreich abgeschlossen!
echo ========================================
echo.
echo Nächste Schritte:
echo 1. Starten Sie den Server: python server.py
echo 2. Öffnen Sie ein neues Terminal
echo 3. Starten Sie den Client: python main.py
echo.
echo Hinweis: Die virtuelle Umgebung ist bereits aktiviert.
echo.
pause
