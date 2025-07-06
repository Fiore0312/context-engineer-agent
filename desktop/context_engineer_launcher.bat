@echo off
REM ==============================================================================
REM AiGENIO by Franco - Desktop Launcher for Windows/WSL
REM Automatically opens WSL in the correct directory and starts AiGENIO
REM ==============================================================================

title AiGENIO by Franco - AI Development Assistant

REM Check if WSL is available
where wsl >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ❌ WSL non trovato!
    echo.
    echo Per utilizzare AiGENIO è necessario installare WSL:
    echo 1. Apri PowerShell come amministratore
    echo 2. Esegui: wsl --install
    echo 3. Riavvia il computer
    echo 4. Configura Ubuntu o la tua distribuzione preferita
    echo.
    echo Per maggiori informazioni: https://docs.microsoft.com/en-us/windows/wsl/install
    echo.
    pause
    exit /b 1
)

REM Display banner
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    AiGENIO by Franco                     ║
echo ║        🤖 AI-Powered Context Engineering Assistant       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🚀 Avvio AiGENIO in WSL...
echo.

REM Define the AiGENIO directory path in WSL
set AIGENIO_PATH=/home/franco/context-engineer-agent

REM Check if AiGENIO directory exists in WSL
wsl test -d "%AIGENIO_PATH%"
if %errorlevel% neq 0 (
    echo ❌ Directory AiGENIO non trovato in WSL!
    echo.
    echo Percorso atteso: %AIGENIO_PATH%
    echo.
    echo Assicurati che AiGENIO sia installato nella posizione corretta.
    echo Se hai installato AiGENIO in un percorso diverso, modifica questo launcher.
    echo.
    pause
    exit /b 1
)

REM Check if Python dependencies are installed
echo 📦 Verifica dipendenze Python...
wsl bash -c "cd %AIGENIO_PATH% && python3 -c 'import click, rich, inquirer' 2>/dev/null"
if %errorlevel% neq 0 (
    echo ⚠️ Dipendenze Python mancanti. Installazione in corso...
    echo.
    
    REM First ensure pip3 is available
    wsl bash -c "command -v pip3"
    if %errorlevel% neq 0 (
        echo 📦 Installazione pip3...
        wsl bash -c "sudo apt update && sudo apt install -y python3-pip"
    )
    
    REM Install requirements
    wsl bash -c "cd %AIGENIO_PATH% && pip3 install --user -r requirements.txt"
    if %errorlevel% neq 0 (
        echo ❌ Errore durante l'installazione delle dipendenze!
        echo.
        echo Risoluzione problemi:
        echo 1. Assicurati che Python3 e pip3 siano installati in WSL
        echo 2. Esegui manualmente: wsl
        echo 3. Poi: cd %AIGENIO_PATH%
        echo 4. Poi: pip3 install --user -r requirements.txt
        echo.
        pause
        exit /b 1
    )
    echo ✅ Dipendenze installate con successo!
    echo.
)

REM Launch AiGENIO interactive menu
echo 🎯 Avvio menu interattivo AiGENIO...
echo.
echo Suggerimento: Se è la prima volta che usi AiGENIO:
echo 1. Configura le tue preferenze di sviluppo
echo 2. Imposta l'integrazione GitHub (opzionale)
echo 3. Seleziona o crea il tuo primo progetto
echo.

REM Start AiGENIO in WSL with proper environment
wsl bash -c "cd %AIGENIO_PATH% && export PYTHONPATH=%AIGENIO_PATH%/src && python3 src/cli.py"

REM Check exit code
if %errorlevel% neq 0 (
    echo.
    echo ⚠️ AiGENIO si è chiuso con errore (codice: %errorlevel%)
    echo.
    echo Risoluzione problemi:
    echo 1. Verifica che tutti i file di AiGENIO siano presenti
    echo 2. Controlla i permessi del file
    echo 3. Esegui manualmente per vedere errori dettagliati:
    echo    wsl
    echo    cd %AIGENIO_PATH%
    echo    python3 src/cli.py --debug
    echo.
    pause
    exit /b 1
)

REM Success message
echo.
echo ✅ AiGENIO terminato correttamente.
echo.
echo 💡 Suggerimenti per la prossima volta:
echo   • Puoi usare i comandi direttamente da WSL
echo   • Consulta la documentazione in README.md
echo   • Unisciti alla community per supporto e aggiornamenti
echo.

REM Option to keep window open
echo Premi un tasto per chiudere questa finestra...
pause >nul

exit /b 0