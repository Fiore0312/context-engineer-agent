#!/bin/bash
# Context Engineering Supervisor Agent Launcher

# Directory dell'agente
AGENT_DIR="/home/franco/context-engineer-agent"

# Esegui l'agente con i parametri passati
cd "$AGENT_DIR"
python3 src/cli.py "$@"