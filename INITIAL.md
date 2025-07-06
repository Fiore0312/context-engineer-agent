## FEATURE:

Migliorare l'agente Context Engineer con interfaccia utente avanzata, sistema di memoria persistente, integrazione Git automatica e accesso a server MCP per best practices aggiornate.

### Modifiche Specifiche Richieste:

1. **File di Avvio Desktop**: Creare un collegamento desktop che apra automaticamente WSL nella directory corretta dell'agente
2. **Interfaccia CLI Migliorata**: Menu principale con ASCII art "Context Engineer" e 3 opzioni (Nuovo Progetto, Apri Progetto, Lista Comandi)
3. **Sistema di Domande Approfondite**: Espandere le domande di configurazione per progetti nuovi ed esistenti
4. **Sistema di Memoria Persistente**: Salvare preferenze utente, linguaggi preferiti, best practices utilizzate
5. **Integrazione Git Automatica**: Backup automatico su GitHub con selezione repository esistenti o creazione nuovi
6. **Server MCP per Best Practices**: Integrazione con server MCP per ottenere best practices aggiornate per CLAUDE.md e INITIAL.md
7. **Suggerimenti Guidati**: L'agente deve suggerire i prossimi comandi da eseguire dopo ogni operazione

## EXAMPLES:

Utilizzare i seguenti file esistenti come pattern:

- `src/cli.py` - Struttura CLI esistente da espandere
- `src/templates/` - Template esistenti da migliorare
- `src/analyzer.py` - Pattern di analisi da estendere
- `context_engineer_instructions.md` - Workflow esistente da automatizzare

Riferimenti per l'interfaccia:
- ASCII art simile a quello mostrato nello screenshot (stile GEMINI ma con "Context Engineer")
- Menu interattivo con numerazione (1. Nuovo Progetto, 2. Apri Progetto, 3. Lista Comandi)

## DOCUMENTATION:

**Git Integration:**
- GitHub API Documentation: https://docs.github.com/en/rest
- PyGithub library: https://pygithub.readthedocs.io/en/latest/
- Git Python: https://gitpython.readthedocs.io/en/stable/

**MCP Server per Best Practices:**
- Cercare e integrare server MCP specifici per Context Engineering e best practices
- MCP Documentation: https://docs.anthropic.com/en/docs/build-with-claude/mcp

**CLI Improvements:**
- Rich library per interfacce CLI: https://rich.readthedocs.io/en/stable/
- Click library: https://click.palletsprojects.com/en/8.1.x/
- Inquirer per prompt interattivi: https://python-inquirer.readthedocs.io/en/latest/

**Persistent Storage:**
- JSON per configurazioni semplici
- SQLite per dati strutturati (preferenze, cronologia progetti)

## OTHER CONSIDERATIONS:

### Struttura File da Creare/Modificare:

```
context-engineer-agent/
├── src/
│   ├── cli.py (MODIFICARE - menu principale)
│   ├── interface/
│   │   ├── __init__.py
│   │   ├── menu.py (NUOVO - menu ASCII art)
│   │   └── prompts.py (NUOVO - domande approfondite)
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── preferences.py (NUOVO - gestione preferenze)
│   │   └── memory.py (NUOVO - best practices storage)
│   ├── git_integration/
│   │   ├── __init__.py
│   │   ├── github_client.py (NUOVO - client GitHub)
│   │   └── auto_backup.py (NUOVO - backup automatico)
│   ├── mcp_integration/
│   │   ├── __init__.py
│   │   └── best_practices_client.py (NUOVO - client MCP)
│   └── utils/
│       ├── __init__.py
│       └── path_detection.py (NUOVO - rilevamento progetti)
├── desktop/
│   └── context_engineer_launcher.bat (NUOVO - launcher Windows)
├── config/
│   ├── user_preferences.json (NUOVO - preferenze utente)
│   └── best_practices_cache.json (NUOVO - cache best practices)
└── requirements.txt (AGGIORNARE)
```

### Gotchas Importanti:

1. **File Launcher Desktop**: Deve funzionare su Windows con WSL, utilizzare percorsi corretti per wsl.exe
2. **Rilevamento Progetti**: Non limitarsi a xampp/htdocs, cercare in:
   - /mnt/c/xampp/htdocs/
   - /mnt/c/Users/[user]/Desktop
   - /mnt/c/progetti/
   - Cartelle configurabili dall'utente
3. **Token GitHub**: Gestire in modo sicuro, criptare se necessario, chiedere solo se non presente
4. **Domande Approfondite**: Deve adattarsi al tipo di progetto rilevato
5. **Memoria Persistente**: Usare percorsi relativi alla home dell'agente
6. **Server MCP**: Ricercare server specifici per Context Engineering, non generici
7. **Suggerimenti Comandi**: Devono essere specifici per il sistema operativo (WSL)

### Domande da Implementare:

**Per Nuovo Progetto:**
- "Che tipo di progetto vuoi creare?" (Web, Mobile, Desktop, AI, etc.)
- "Hai linguaggi di programmazione preferiti o scelgo io in base al progetto?"
- "Vuoi che consulti i server MCP per best practices aggiornate?"
- "Preferisci un approccio più strutturato o più flessibile?"
- "Hai framework specifici in mente?"
- "Il progetto avrà bisogno di database? Quale tipo?"

**Per Progetto Esistente:**
- "Cosa vuoi migliorare in questo progetto?" (Bug fix, Nuove feature, Refactoring, etc.)
- "Ci sono problemi specifici che hai notato?"
- "Vuoi che analizzi le best practices attuali del progetto?"
- "Devo cercare aggiornamenti per le dipendenze?"

### Istruzioni per CLAUDE.md/INITIAL.md:

Inserire automaticamente nei file generati:

```markdown
### 🔄 Auto-Backup Git
Al termine di ogni sessione di lavoro, Claude Code deve eseguire automaticamente:
1. `git add .`
2. `git commit -m "Context Engineering - [timestamp] - [descrizione breve]"`
3. `git push origin main`

Se il repository non esiste, chiedere se:
- Usare repository esistente (mostrare lista da GitHub)
- Creare nuovo repository
- Saltare il backup per questa sessione

Token GitHub richiesto per l'accesso automatico.
```

### ASCII Art Esempio:

```
╔═══════════════════════════════════════════════════════════════╗
║   ██████╗ ██████╗ ███╗   ██╗████████╗███████╗██╗  ██╗████████╗ ║
║  ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔════╝╚██╗██╔╝╚══██╔══╝ ║
║  ██║     ██║   ██║██╔██╗ ██║   ██║   █████╗   ╚███╔╝    ██║    ║
║  ██║     ██║   ██║██║╚██╗██║   ██║   ██╔══╝   ██╔██╗    ██║    ║
║  ╚██████╗╚██████╔╝██║ ╚████║   ██║   ███████╗██╔╝ ██╗   ██║    ║
║   ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝    ║
║                                                                 ║
║            ███████╗███╗   ██╗ ██████╗ ██╗███╗   ██╗███████╗     ║
║            ██╔════╝████╗  ██║██╔════╝ ██║████╗  ██║██╔════╝     ║
║            █████╗  ██╔██╗ ██║██║  ███╗██║██╔██╗ ██║█████╗       ║
║            ██╔══╝  ██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══╝       ║
║            ███████╗██║ ╚████║╚██████╔╝██║██║ ╚████║███████╗     ║
║            ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝     ║
╚═══════════════════════════════════════════════════════════════╝

               🤖 AI-Powered Context Engineering Assistant

┌─────────────────────────────────────────────────────────────────┐
│  1. 🆕 Nuovo Progetto                                            │
│  2. 📂 Apri Progetto                                             │
│  3. 📋 Lista Comandi                                             │
│                                                                   │
│  Seleziona un'opzione (1-3): ▊                                   │
└─────────────────────────────────────────────────────────────────┘
```