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
echo.
echo                    AiGENIO by Franco
echo        🤖 AI-Powered Context Engineering Assistant
echo.
echo 🚀 Avvio AiGENIO in WSL...
echo.

REM Define the AiGENIO directory path in WSL
set AIGENIO_PATH=/home/franco/context-engineer-agent

REM Check if AiGENIO directory exists in WSL
echo 📁 Verifica directory AiGENIO...
wsl test -d "%AIGENIO_PATH%"
if %errorlevel% neq 0 (
    echo ❌ Directory AiGENIO non trovato in WSL!
    echo.
    echo Percorso atteso: %AIGENIO_PATH%
    echo.
    echo Verifica percorsi alternativi...
    wsl ls -la /home/franco/ 2>nul
    echo.
    echo Se AiGENIO è in una posizione diversa, modifica questo launcher.
    echo.
    pause
    exit /b 1
)

REM Check if requirements.txt exists
echo 📋 Verifica file requirements.txt...
wsl test -f "%AIGENIO_PATH%/requirements.txt"
if %errorlevel% neq 0 (
    echo ⚠️ File requirements.txt non trovato! Creazione automatica...
    wsl bash -c "cd %AIGENIO_PATH% && cat > requirements.txt << 'EOF'
click>=8.0.0
rich>=10.0.0
inquirer>=2.8.0
pydantic>=1.8.0
requests>=2.25.0
python-dotenv>=0.19.0
gitpython>=3.1.0
PyGithub>=1.55
pathspec>=0.9.0
jinja2>=3.0.0
pyyaml>=6.0
EOF"
    echo ✅ requirements.txt creato!
)

REM Check if Python3 and venv are available
echo 🐍 Verifica Python3 e venv...
wsl bash -c "python3 --version"
if %errorlevel% neq 0 (
    echo ❌ Python3 non trovato in WSL!
    echo 📦 Installazione Python3...
    wsl bash -c "sudo apt update && sudo apt install -y python3 python3-pip python3-venv"
)

REM Check and create virtual environment
echo 📦 Gestione ambiente virtuale Python...
wsl bash -c "cd %AIGENIO_PATH% && test -f venv/bin/activate"
if %errorlevel% neq 0 (
    echo 🔧 Creazione ambiente virtuale...
    REM Remove any broken venv directory first
    wsl bash -c "cd %AIGENIO_PATH% && rm -rf venv"
    
    REM Create fresh virtual environment
    wsl bash -c "cd %AIGENIO_PATH% && python3 -m venv venv"
    if %errorlevel% neq 0 (
        echo 📦 Installazione python3-venv...
        wsl bash -c "sudo apt update && sudo apt install -y python3-venv"
        echo 🔧 Ripetendo creazione ambiente virtuale...
        wsl bash -c "cd %AIGENIO_PATH% && python3 -m venv venv"
        if %errorlevel% neq 0 (
            echo ❌ Impossibile creare ambiente virtuale!
            pause
            exit /b 1
        )
    )
    echo ✅ Ambiente virtuale creato!
)

REM Verify virtual environment activation
echo 🔍 Test attivazione ambiente virtuale...
wsl bash -c "cd %AIGENIO_PATH% && source venv/bin/activate && python --version"
if %errorlevel% neq 0 (
    echo ❌ Ambiente virtuale non funziona correttamente!
    echo 🔧 Ricostruzione ambiente virtuale...
    wsl bash -c "cd %AIGENIO_PATH% && rm -rf venv && python3 -m venv venv"
    if %errorlevel% neq 0 (
        echo ❌ Fallimento definitivo creazione ambiente virtuale!
        pause
        exit /b 1
    )
)

REM Install/check dependencies
echo 📦 Verifica dipendenze Python...
wsl bash -c "cd %AIGENIO_PATH% && source venv/bin/activate && python -c 'import click, rich, inquirer' 2>/dev/null"
if %errorlevel% neq 0 (
    echo ⚠️ Installazione dipendenze nell'ambiente virtuale...
    wsl bash -c "cd %AIGENIO_PATH% && source venv/bin/activate && pip install --upgrade pip"
    wsl bash -c "cd %AIGENIO_PATH% && source venv/bin/activate && pip install -r requirements.txt"
    if %errorlevel% neq 0 (
        echo ❌ Errore installazione dipendenze!
        echo.
        echo 🔧 Tentativo installazione manuale dei pacchetti essenziali...
        wsl bash -c "cd %AIGENIO_PATH% && source venv/bin/activate && pip install click rich inquirer pydantic requests python-dotenv"
        if %errorlevel% neq 0 (
            echo ❌ Installazione fallita definitivamente!
            pause
            exit /b 1
        )
    )
    echo ✅ Dipendenze installate!
)

REM Check if CLI script exists
echo 📄 Verifica script CLI...
wsl test -f "%AIGENIO_PATH%/src/cli.py"
if %errorlevel% neq 0 (
    echo ❌ File src/cli.py non trovato!
    echo.
    echo Contenuto directory src:
    wsl ls -la "%AIGENIO_PATH%/src/" 2>nul
    echo.
    echo Verifica che AiGENIO sia installato correttamente.
    pause
    exit /b 1
)

REM Launch AiGENIO interactive menu
echo.
echo 🎯 Avvio menu interattivo AiGENIO...
echo.
echo 💡 Suggerimenti per il primo utilizzo:
echo    1. Configura le tue preferenze di sviluppo
echo    2. Imposta l'integrazione GitHub (opzionale)
echo    3. Seleziona o crea il tuo primo progetto
echo.
echo ⏳ Caricamento in corso...
echo.

REM Start AiGENIO in WSL with proper environment and error handling
wsl bash -c "cd %AIGENIO_PATH% && source venv/bin/activate && export PYTHONPATH=%AIGENIO_PATH%/src:%AIGENIO_PATH% && python src/cli.py" 2>error.log

REM Check exit code and show detailed error if needed
if %errorlevel% neq 0 (
    echo.
    echo ⚠️ AiGENIO si è chiuso con errore (codice: %errorlevel%)
    echo.
    echo 📋 Log errori:
    wsl cat "%AIGENIO_PATH%/error.log" 2>nul
    echo.
    echo 🔧 Risoluzione problemi:
    echo    1. Verifica che tutti i file di AiGENIO siano presenti
    echo    2. Controlla i permessi del file
    echo    3. Esegui manualmente per debug dettagliato:
    echo       wsl
    echo       cd %AIGENIO_PATH%
    echo       source venv/bin/activate
    echo       python src/cli.py --debug
    echo.
    echo 💬 Per supporto, condividi il contenuto di error.log
    echo.
    pause
    exit /b 1
)

REM Success message
echo.
echo ✅ AiGENIO terminato correttamente.
echo.
echo 💡 Suggerimenti per la prossima volta:
echo    • Puoi usare i comandi direttamente da WSL
echo    • Consulta la documentazione in README.md
echo    • Il launcher salva automaticamente i log per il debug
echo.

REM Option to keep window open
echo Premi un tasto per chiudere questa finestra...
pause >nul

REM Cleanup error log if everything went well
wsl rm -f "%AIGENIO_PATH%/error.log" 2>nul

exit /b 0