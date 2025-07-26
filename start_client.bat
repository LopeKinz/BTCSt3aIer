@echo off
echo ========================================
echo Bitcoin Wallet Finder - Client
echo ========================================
echo.

REM Aktiviere virtuelle Umgebung falls vorhanden
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo Virtuelle Umgebung aktiviert.
    echo.
)

echo Stelle sicher, dass der Server läuft (start_server.bat)!
echo.
timeout /t 3 /nobreak > nul

REM Starte Client
python main.py

pause
