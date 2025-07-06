# 🤖 AiGENIO by Franco

> **Your Personal AI Development Assistant with Advanced Context Engineering**

AiGENIO is an intelligent meta-agent that learns your development preferences and automatically generates optimized instructions for AI coding assistants like Claude Code. It bridges the gap between human intent and AI implementation through personalized Context Engineering.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![WSL](https://img.shields.io/badge/WSL-Compatible-orange.svg)](https://docs.microsoft.com/en-us/windows/wsl/)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Integrated-purple.svg)](https://docs.anthropic.com/claude/docs/claude-code)

## 🎯 **Core Features**

### 🖥️ **Intelligent Interface**
```
                            AiGENIO by Franco
             🤖 AI-Powered Context Engineering Assistant
-----------------------------------------------------------------
  1. 🆕 Nuovo Progetto
  2. 📂 Apri Progetto
  3. 📋 Lista Comandi
```

### 🧠 **Persistent Learning System**
- **Preference Storage**: Remembers your coding languages, frameworks, and patterns
- **Best Practices Database**: Builds a knowledge base from successful projects
- **Adaptive Questioning**: Asks smarter questions based on project type and history

### ⚡ **Automated Workflow**
```bash
# AiGENIO workflow
You: "I want to build a web scraper for e-commerce sites"
↓
AiGENIO: [Analyzes request, checks preferences, generates optimized INITIAL.md]
↓
Claude Code: [Implements with full context and your preferred patterns]
↓
Production-ready project with automatic Git backup
```

## 🚀 **Quick Start**

### Prerequisites
- Python 3.8+
- WSL (Windows Subsystem for Linux)
- Claude Code access
- Git configured
- GitHub account (optional, for auto-backup)

### Installation

```bash
# Clone the repository
<<<<<<< HEAD
git clone https://github.com/Fiore0312/context-engineer-agent
=======
gh repo clone Fiore0312/context-engineer-agent
>>>>>>> 80551e1aa47217602712b54e51e32fb2aa81b935
cd context-engineer-agent

# Install dependencies
pip install -r requirements.txt

# Create desktop launcher (Windows)
python setup_launcher.py

# First run
python src/cli.py
```

### Quick Setup
```bash
# Double-click the desktop launcher or run:
./aigenio_launcher

# Follow the interactive setup:
# 1. Configure your preferences
# 2. Set up GitHub integration (optional)
# 3. Choose your first project
```

## 🏗️ Architettura

```
context-engineer-agent/
├── src/
│   ├── cli.py                 # CLI principale
│   ├── agent.py              # Agente core
│   ├── analyzers/            # Analizzatori progetto
│   │   ├── project_analyzer.py
│   │   └── framework_detector.py
│   ├── generators/           # Generatori configurazione
│   │   ├── claude_config_generator.py
│   │   ├── initial_generator.py
│   │   └── prp_generator.py
│   ├── validators/           # Validatori setup
│   │   └── setup_validator.py
│   └── utils.py             # Utilities
├── templates/               # Template per framework
│   ├── php/
│   ├── javascript/
│   └── python/
├── examples/               # Esempi configurazione
└── docs/                  # Documentazione
```

## 🔧 Comandi Disponibili

### `setup`
Configura Context Engineering per un progetto

**Opzioni:**
- `--force`: Forza setup anche se già configurato
- `--template NOME`: Usa template specifico

**Esempio:**
```bash
context-engineer setup ~/projects/my-laravel-app --template laravel
```

### `analyze`
Analizza struttura e tecnologie del progetto

**Opzioni:**
- `--export FILE`: Esporta analisi in JSON

**Esempio:**
```bash
context-engineer analyze ~/projects/my-app --export analysis.json
```

### `generate`
Genera INITIAL.md per nuova feature

**Opzioni:**
- `--feature DESCRIZIONE`: Descrizione della feature
- `--template TIPO`: Template INITIAL.md da usare

**Esempio:**
```bash
context-engineer generate ~/projects/my-app --feature "Dashboard analytics"
```

### `validate`
Valida configurazione Context Engineering

**Esempio:**
```bash
context-engineer validate ~/projects/my-app
```

### `report`
Genera report completo del progetto

**Opzioni:**
- `--output FILE`: Salva report in file

**Esempio:**
```bash
context-engineer report ~/projects/my-app --output report.json
```

### `templates`
Lista template disponibili

**Esempio:**
```bash
context-engineer templates
```

## 📋 Framework Supportati

### Frontend
- ✅ React
- ✅ Vue.js
- ✅ Angular
- ✅ Svelte
- ✅ Next.js
- ✅ Nuxt.js

### Backend
- ✅ Laravel (PHP)
- ✅ Symfony (PHP)
- ✅ Django (Python)
- ✅ Flask (Python)
- ✅ FastAPI (Python)
- ✅ Express.js (Node.js)
- ✅ NestJS (Node.js)

### Mobile
- ✅ React Native
- ✅ Flutter

### Desktop
- ✅ Electron
- ✅ Tauri

## 🎨 Esempi di Output

### CLAUDE.md Generato
```markdown
# My Laravel Project

**Tipo Progetto**: Web Application
**Framework**: Laravel
**Linguaggi**: PHP, JavaScript
**Generato**: 2024-01-15

## Descrizione Progetto
Applicazione web Laravel per gestione progetti aziendali.

## Setup Ambiente di Sviluppo
```bash
# Installa dipendenze
composer install
npm install

# Configura ambiente
cp .env.example .env
php artisan key:generate

# Avvia server
php artisan serve
```

## Regole Context Engineering
- Usa Eloquent ORM per database operations
- Implementa Form Requests per validation
- Segui convenzioni Laravel per naming
- Usa Resource Controllers per API
```

### INITIAL.md Generato
```markdown
# FEATURE: Sistema di Autenticazione Utenti

**Tipo**: Authentication & Authorization
**Progetto**: My Laravel Project
**Complessità**: Medium
**Tempo Stimato**: 2-3 giorni

## Descrizione
Implementare sistema completo di autenticazione con registrazione, login, reset password e gestione sessioni.

## Obiettivi
- User registration e login
- Password reset flow
- Session management
- Role-based access control

## Implementazione
### Step 1: Database Schema
- Users table con campi richiesti
- Roles e permissions tables
- Password reset tokens

### Step 2: Authentication Logic
- User model con relationships
- Auth controllers
- Middleware per protezione route
```

## 🔍 Analisi Automatica

L'agente analizza automaticamente:

- **Struttura Progetto**: Directory, file, architettura
- **Framework Detection**: Riconoscimento automatico tecnologie
- **Linguaggi**: Identificazione linguaggi utilizzati
- **Dipendenze**: Analisi package managers e dipendenze
- **Complessità**: Valutazione complessità progetto
- **Best Practices**: Verifica convenzioni e standard

## 📊 Score di Qualità

L'agente assegna uno score (1-10) basato su:

- ✅ Presenza CLAUDE.md completo
- ✅ Struttura directory organizzata  
- ✅ Configurazione appropriata
- ✅ Esempi e documentazione
- ✅ Test implementati
- ✅ Best practices seguite

## 🛠️ Configurazione

L'agente salva configurazioni in `~/.context-engineer/`:

```
~/.context-engineer/
├── projects.json        # Database progetti
├── templates/          # Template personalizzati
├── config.json         # Configurazione globale
└── agent.log          # Log attività
```

Ogni progetto ottiene anche:

```
project/
├── .context-engineer/
│   └── config.json     # Config progetto
├── .claude/
│   └── examples/       # Esempi progetto
└── CLAUDE.md          # Configurazione principale
```

## 🧩 Estensibilità

### Aggiungere Nuovo Framework

1. Estendi `framework_detector.py`:
```python
'my_framework': {
    'files': ['my_config.json'],
    'dependencies': ['my-framework'],
    'patterns': ['specific patterns'],
    'config_files': ['my.config.js']
}
```

2. Aggiungi template in `templates/`:
```
templates/
└── my_framework/
    ├── claude_template.md
    └── example.md
```

### Template Personalizzati

Crea template personalizzati in `~/.context-engineer/templates/`:

```markdown
# {{ project_name }} Custom Template

**Framework**: {{ framework }}

## Custom Section
...
```

## 🚀 Roadmap

- [ ] **v1.1**: Integrazione con MCP servers
- [ ] **v1.2**: Template visivi con diagrammi
- [ ] **v1.3**: AI-powered code analysis
- [ ] **v1.4**: Multi-project workspace support
- [ ] **v1.5**: Plugin system per IDE
- [ ] **v2.0**: Cloud sync e team collaboration

## 🤝 Contribuire

1. Fork il repository
2. Crea feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)
5. Apri Pull Request

## 📝 License

Questo progetto è sotto licenza MIT. Vedi [LICENSE](LICENSE) per dettagli.

## 🙋‍♂️ Support

- 📧 Email: support@contextengineering.dev
- 💬 Discord: [Context Engineering Community](https://discord.gg/contexteng)
- 📖 Docs: [docs.contextengineering.dev](https://docs.contextengineering.dev)
- 🐛 Issues: [GitHub Issues](https://github.com/contextengineering/agent/issues)

---

**Sviluppato con ❤️ dal team Context Engineering**
