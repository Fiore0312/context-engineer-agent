@echo off
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
    echo Installa WSL e riprova.
    pause
    exit /b 1
)

set AIGENIO_PATH=/home/franco/context-engineer-agent

echo Controllo AiGENIO...
wsl test -d "%AIGENIO_PATH%"
if %errorlevel% neq 0 (
    echo ERRORE: Directory AiGENIO non trovata!
    echo Percorso: %AIGENIO_PATH%
    pause
    exit /b 1
)

echo Attivazione ambiente virtuale...
wsl bash -c "cd %AIGENIO_PATH% && test -f venv/bin/activate"
if %errorlevel% neq 0 (
    echo Creo ambiente virtuale...
    wsl bash -c "cd %AIGENIO_PATH% && python3 -m venv venv"
)

echo Verifica dipendenze...
wsl bash -c "cd %AIGENIO_PATH% && source venv/bin/activate && python3 -c 'import click' 2>/dev/null"
if %errorlevel% neq 0 (
    echo Installo dipendenze...
    wsl bash -c "cd %AIGENIO_PATH% && source venv/bin/activate && pip3 install click rich inquirer pydantic requests python-dotenv gitpython pyyaml jinja2"
)

echo.
echo Avvio AiGENIO...
echo.

REM Launch AiGENIO
wsl bash -c "cd %AIGENIO_PATH% && source venv/bin/activate && python3 src/cli.py"

if %errorlevel% neq 0 (
    echo.
    echo AiGENIO terminato con errore.
    echo.
    echo Per debug:
    echo   wsl
    echo   cd %AIGENIO_PATH%
    echo   source venv/bin/activate
    echo   python3 src/cli.py
    echo.
    pause
)

echo.
echo Grazie per aver usato AiGENIO!
pause >nul
exit /b 0
