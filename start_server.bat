@echo off
echo ========================================
echo Bitcoin Wallet Finder - Starter
echo ========================================
echo.

echo Starte Server...
echo.
echo WICHTIG: Lassen Sie dieses Fenster geöffnet!
echo Der Server läuft auf http://localhost:5000
echo.
echo Öffnen Sie ein NEUES Terminal und führen Sie aus:
echo python main.py
echo.

REM Aktiviere virtuelle Umgebung falls vorhanden
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Virtuelle Umgebung aktiviert.
    echo.
)

REM Starte Server
python server.py
