#!/bin/bash
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
