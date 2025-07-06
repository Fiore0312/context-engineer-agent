#!/usr/bin/env python3
"""
Setup script per creare il launcher desktop di AiGENIO by Franco
"""

import os
import shutil
import platform
from pathlib import Path

def create_windows_launcher():
    """Crea il launcher per Windows"""
    
    launcher_content = """@echo off
title AiGENIO by Franco - AI Development Assistant

echo.
echo =====================================================
echo           AiGENIO by Franco
echo    AI-Powered Context Engineering Assistant  
echo =====================================================
echo.

REM Check WSL
where wsl >nul 2>nul
if %errorlevel% neq 0 (
    echo ERRORE: WSL non trovato!
    echo Installa WSL da Microsoft Store o PowerShell
    pause
    exit /b 1
)

set AIGENIO_PATH=/home/franco/context-engineer-agent

REM Check directory
echo Controllo directory AiGENIO...
wsl test -d "%AIGENIO_PATH%"
if %errorlevel% neq 0 (
    echo ERRORE: Directory non trovata: %AIGENIO_PATH%
    pause
    exit /b 1
)

REM Setup virtual environment (simple)
echo Controllo ambiente Python...
wsl bash -c "cd %AIGENIO_PATH% && test -f venv/bin/activate"
if %errorlevel% neq 0 (
    echo Creo ambiente virtuale...
    wsl bash -c "cd %AIGENIO_PATH% && rm -rf venv && python3 -m venv venv"
)

REM Install dependencies (simple)
echo Verifico dipendenze...
wsl bash -c "cd %AIGENIO_PATH% && source venv/bin/activate && python -c 'import click' 2>/dev/null"
if %errorlevel% neq 0 (
    echo Installo dipendenze essenziali...
    wsl bash -c "cd %AIGENIO_PATH% && source venv/bin/activate && pip install click rich inquirer pydantic requests python-dotenv"
)

REM Check CLI exists
wsl test -f "%AIGENIO_PATH%/src/cli.py"
if %errorlevel% neq 0 (
    echo ERRORE: File src/cli.py non trovato!
    wsl ls -la "%AIGENIO_PATH%/"
    pause
    exit /b 1
)

echo.
echo Avvio AiGENIO...
echo.

REM Launch AiGENIO (simple)
wsl bash -c "cd %AIGENIO_PATH% && source venv/bin/activate && python src/cli.py"

if %errorlevel% neq 0 (
    echo.
    echo AiGENIO terminato con errore.
    echo.
    echo Per debug manuale:
    echo   wsl
    echo   cd %AIGENIO_PATH%
    echo   source venv/bin/activate  
    echo   python src/cli.py
    echo.
    pause
)

echo.
echo Grazie per aver usato AiGENIO!
pause >nul
exit /b 0
"""
    
    launcher_path = Path("desktop/aigenio_launcher.bat")
    launcher_path.parent.mkdir(exist_ok=True)
    launcher_path.write_text(launcher_content, encoding='utf-8')
    
    print(f"✅ Launcher Windows creato: {launcher_path}")
    return launcher_path

def create_linux_launcher():
    """Crea il launcher per Linux"""
    
    launcher_content = """#!/bin/bash
# AiGENIO by Franco - Linux Launcher

echo "======================================================"
echo "           AiGENIO by Franco"
echo "    AI-Powered Context Engineering Assistant"  
echo "======================================================"
echo

AIGENIO_PATH="$HOME/context-engineer-agent"

# Check directory
if [ ! -d "$AIGENIO_PATH" ]; then
    echo "ERRORE: Directory non trovata: $AIGENIO_PATH"
    read -p "Premi Enter per uscire..."
    exit 1
fi

cd "$AIGENIO_PATH"

# Setup virtual environment
if [ ! -f "venv/bin/activate" ]; then
    echo "Creo ambiente virtuale..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "Verifico dipendenze..."
python -c "import click" 2>/dev/null || {
    echo "Installo dipendenze essenziali..."
    pip install click rich inquirer pydantic requests python-dotenv
}

# Check CLI exists
if [ ! -f "src/cli.py" ]; then
    echo "ERRORE: File src/cli.py non trovato!"
    ls -la
    read -p "Premi Enter per uscire..."
    exit 1
fi

echo
echo "Avvio AiGENIO..."
echo

# Launch AiGENIO
python src/cli.py

echo
echo "Grazie per aver usato AiGENIO!"
read -p "Premi Enter per uscire..."
"""
    
    launcher_path = Path("desktop/aigenio_launcher.sh")
    launcher_path.parent.mkdir(exist_ok=True)
    launcher_path.write_text(launcher_content, encoding='utf-8')
    launcher_path.chmod(0o755)  # Make executable
    
    print(f"✅ Launcher Linux creato: {launcher_path}")
    return launcher_path

def main():
    """Setup launcher principale"""
    
    print("🚀 Setup Launcher AiGENIO by Franco")
    print("=" * 50)
    
    # Detect platform
    system = platform.system().lower()
    
    if system == "windows":
        launcher_path = create_windows_launcher()
        print(f"""
📋 Istruzioni per Windows:
1. Copia il file {launcher_path} sul desktop
2. Fai doppio clic per avviare AiGENIO
3. Il launcher gestirà automaticamente WSL e dipendenze
        """)
    elif system in ["linux", "darwin"]:  # Linux or macOS
        launcher_path = create_linux_launcher()
        print(f"""
📋 Istruzioni per Linux/macOS:
1. Copia il file {launcher_path} sul desktop
2. Fai doppio clic o esegui: ./{launcher_path.name}
3. Il launcher gestirà automaticamente l'ambiente virtuale
        """)
    else:
        print(f"⚠️ Sistema operativo non supportato: {system}")
        print("Usa direttamente: python src/cli.py")
        return
    
    # Copy to desktop if possible
    try:
        desktop_path = Path.home() / "Desktop"
        if desktop_path.exists():
            desktop_launcher = desktop_path / launcher_path.name
            shutil.copy2(launcher_path, desktop_launcher)
            print(f"✅ Launcher copiato sul desktop: {desktop_launcher}")
        else:
            print("ℹ️ Desktop non trovato, copia manualmente il launcher")
    except Exception as e:
        print(f"⚠️ Impossibile copiare sul desktop: {e}")
    
    print(f"""
✅ Setup completato!

🎯 Per avviare AiGENIO:
   • Usa il launcher sul desktop
   • Oppure: python src/cli.py
   • Oppure: python src/cli.py menu

📚 Documentazione completa: README.md
    """)

if __name__ == "__main__":
    main()