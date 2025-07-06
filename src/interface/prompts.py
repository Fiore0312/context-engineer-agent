"""
Advanced interactive prompts for project configuration
"""

import inquirer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from typing import Dict, List, Optional

console = Console()

def ask_new_project_questions() -> Dict:
    """Ask comprehensive questions for new project setup"""
    
    console.print(Panel(
        "🆕 [bold]Configurazione Nuovo Progetto[/bold]\n\n"
        "Rispondi alle seguenti domande per creare un progetto ottimizzato",
        title="[bold blue]Setup Progetto[/bold blue]",
        border_style="blue"
    ))
    
    questions = [
        inquirer.List(
            'project_type',
            message="Che tipo di progetto vuoi creare?",
            choices=[
                ('🌐 Applicazione Web', 'web'),
                ('📱 Applicazione Mobile', 'mobile'),
                ('🖥️ Applicazione Desktop', 'desktop'),
                ('🤖 Progetto AI/ML', 'ai_ml'),
                ('🔧 Tool/Utility', 'tool'),
                ('📚 Libreria/Framework', 'library'),
                ('🔗 API/Microservizio', 'api'),
                ('📊 Analisi Dati', 'data_analysis'),
                ('🎮 Game Development', 'game'),
                ('🔐 Sistema di Sicurezza', 'security'),
                ('🌟 Altro', 'other')
            ],
            default='web'
        ),
        inquirer.List(
            'language_preference',
            message="Hai linguaggi di programmazione preferiti?",
            choices=[
                ('🐍 Python', 'python'),
                ('🟨 JavaScript/TypeScript', 'javascript'),
                ('🔵 PHP', 'php'),
                ('☕ Java', 'java'),
                ('🦀 Rust', 'rust'),
                ('🔷 C#', 'csharp'),
                ('🌊 Go', 'go'),
                ('💎 Ruby', 'ruby'),
                ('🏗️ C++', 'cpp'),
                ('⚡ Kotlin', 'kotlin'),
                ('🎯 Swift', 'swift'),
                ('🤖 Scegli tu in base al progetto', 'auto')
            ],
            default='auto'
        ),
        inquirer.Confirm(
            'use_mcp',
            message="Vuoi che consulti i server MCP per best practices aggiornate?",
            default=True
        ),
        inquirer.List(
            'project_approach',
            message="Preferisci un approccio più strutturato o più flessibile?",
            choices=[
                ('🏗️ Strutturato (con framework e convenzioni rigide)', 'structured'),
                ('🎨 Flessibile (più libertà creative)', 'flexible'),
                ('⚖️ Bilanciato (via di mezzo)', 'balanced')
            ],
            default='balanced'
        ),
        inquirer.Confirm(
            'has_specific_frameworks',
            message="Hai framework specifici in mente?",
            default=False
        )
    ]
    
    answers = inquirer.prompt(questions)
    
    # Check if user cancelled
    if answers is None:
        return None
    
    # Ask for specific frameworks if user wants them
    if answers['has_specific_frameworks']:
        framework_question = inquirer.Text(
            'preferred_frameworks',
            message="Specifica i framework preferiti (separati da virgola):"
        )
        framework_answer = inquirer.prompt([framework_question])
        if framework_answer is None:
            return None
        answers.update(framework_answer)
    
    # Ask about database needs
    database_questions = [
        inquirer.Confirm(
            'needs_database',
            message="Il progetto avrà bisogno di un database?",
            default=True
        )
    ]
    
    db_answers = inquirer.prompt(database_questions)
    if db_answers is None:
        return None
    answers.update(db_answers)
    
    if db_answers['needs_database']:
        db_type_question = inquirer.List(
            'database_type',
            message="Quale tipo di database?",
            choices=[
                ('🐘 PostgreSQL', 'postgresql'),
                ('🐬 MySQL/MariaDB', 'mysql'),
                ('🍃 MongoDB', 'mongodb'),
                ('🔥 Redis', 'redis'),
                ('📊 SQLite', 'sqlite'),
                ('🌊 InfluxDB (Time Series)', 'influxdb'),
                ('🔍 Elasticsearch', 'elasticsearch'),
                ('🤖 Scegli tu in base al progetto', 'auto')
            ],
            default='auto'
        )
        db_type_answer = inquirer.prompt([db_type_question])
        if db_type_answer is None:
            return None
        answers.update(db_type_answer)
    
    # Ask about additional features
    additional_questions = [
        inquirer.Checkbox(
            'additional_features',
            message="Quali funzionalità aggiuntive vuoi includere?",
            choices=[
                ('🔐 Autenticazione e autorizzazione', 'auth'),
                ('🔄 Sistema di backup automatico', 'backup'),
                ('📧 Sistema di notifiche/email', 'notifications'),
                ('📊 Analytics e metriche', 'analytics'),
                ('🔍 Sistema di ricerca', 'search'),
                ('🌍 Internazionalizzazione', 'i18n'),
                ('📱 API REST/GraphQL', 'api'),
                ('🧪 Test automatici', 'testing'),
                ('🚀 CI/CD Pipeline', 'cicd'),
                ('📝 Documentazione automatica', 'docs'),
                ('🎨 UI/UX avanzato', 'ui'),
                ('🔧 Monitoring e logging', 'monitoring')
            ]
        ),
        inquirer.Confirm(
            'use_git_integration',
            message="Vuoi attivare l'integrazione Git automatica?",
            default=True
        ),
        inquirer.List(
            'deployment_target',
            message="Dove prevedi di deployare il progetto?",
            choices=[
                ('☁️ Cloud (AWS, Azure, GCP)', 'cloud'),
                ('🐳 Container (Docker/Kubernetes)', 'container'),
                ('🖥️ Server tradizionale', 'server'),
                ('🌐 Hosting web (Netlify, Vercel)', 'web_hosting'),
                ('📱 App Store (mobile)', 'app_store'),
                ('🤷 Non so ancora', 'unknown')
            ],
            default='cloud'
        )
    ]
    
    additional_answers = inquirer.prompt(additional_questions)
    
    # Check if user cancelled
    if additional_answers is None:
        return None
        
    answers.update(additional_answers)
    
    return answers

def ask_existing_project_questions() -> Dict:
    """Ask questions for existing project analysis"""
    
    console.print(Panel(
        "📂 [bold]Analisi Progetto Esistente[/bold]\n\n"
        "Aiutami a capire come migliorare il tuo progetto",
        title="[bold green]Analisi Progetto[/bold green]",
        border_style="green"
    ))
    
    questions = [
        inquirer.List(
            'improvement_goal',
            message="Cosa vuoi migliorare in questo progetto?",
            choices=[
                ('🐛 Bug fix e correzioni', 'bug_fix'),
                ('✨ Nuove funzionalità', 'new_features'),
                ('🔧 Refactoring e ottimizzazione', 'refactoring'),
                ('🚀 Performance e velocità', 'performance'),
                ('🔐 Sicurezza', 'security'),
                ('📊 Scalabilità', 'scalability'),
                ('🎨 UI/UX', 'ui_ux'),
                ('📚 Documentazione', 'documentation'),
                ('🧪 Testing e qualità', 'testing'),
                ('🔄 Modernizzazione tecnologica', 'modernization'),
                ('🌍 SEO e accessibilità', 'seo_accessibility'),
                ('🔍 Analisi generale', 'general_analysis')
            ]
        ),
        inquirer.Confirm(
            'has_specific_problems',
            message="Ci sono problemi specifici che hai notato?",
            default=False
        )
    ]
    
    answers = inquirer.prompt(questions)
    
    # Check if user cancelled
    if answers is None:
        return None
    
    # Ask for specific problems if user has them
    if answers['has_specific_problems']:
        problem_question = inquirer.Text(
            'specific_problems',
            message="Descrivi i problemi specifici che hai notato:"
        )
        problem_answer = inquirer.prompt([problem_question])
        if problem_answer is None:
            return None
        answers.update(problem_answer)
    
    # Additional analysis questions
    analysis_questions = [
        inquirer.Confirm(
            'analyze_best_practices',
            message="Vuoi che analizzi le best practices attuali del progetto?",
            default=True
        ),
        inquirer.Confirm(
            'check_dependencies',
            message="Devo cercare aggiornamenti per le dipendenze?",
            default=True
        ),
        inquirer.Confirm(
            'security_audit',
            message="Vuoi un audit di sicurezza?",
            default=True
        ),
        inquirer.Checkbox(
            'analysis_areas',
            message="Su quali aree vuoi concentrare l'analisi?",
            choices=[
                ('🏗️ Architettura del codice', 'architecture'),
                ('📊 Performance', 'performance'),
                ('🔐 Sicurezza', 'security'),
                ('🧪 Test coverage', 'testing'),
                ('📚 Documentazione', 'documentation'),
                ('🔄 Dipendenze', 'dependencies'),
                ('🎨 UI/UX', 'ui_ux'),
                ('🌐 SEO', 'seo'),
                ('♿ Accessibilità', 'accessibility'),
                ('📱 Responsive design', 'responsive'),
                ('🚀 Build process', 'build_process'),
                ('🔧 Configuration', 'configuration')
            ]
        ),
        inquirer.Confirm(
            'generate_improvement_plan',
            message="Vuoi che generi un piano di miglioramento dettagliato?",
            default=True
        )
    ]
    
    analysis_answers = inquirer.prompt(analysis_questions)
    
    # Check if user cancelled
    if analysis_answers is None:
        return None
        
    answers.update(analysis_answers)
    
    return answers

def ask_preferences_questions() -> Dict:
    """Ask questions for user preferences setup"""
    
    console.print(Panel(
        "⚙️ [bold]Configurazione Preferenze[/bold]\n\n"
        "Personalizza AiGENIO in base alle tue preferenze",
        title="[bold yellow]Preferenze Utente[/bold yellow]",
        border_style="yellow"
    ))
    
    questions = [
        inquirer.Checkbox(
            'favorite_languages',
            message="Quali sono i tuoi linguaggi di programmazione preferiti?",
            choices=[
                ('🐍 Python', 'python'),
                ('🟨 JavaScript', 'javascript'),
                ('🔷 TypeScript', 'typescript'),
                ('🔵 PHP', 'php'),
                ('☕ Java', 'java'),
                ('🦀 Rust', 'rust'),
                ('🔷 C#', 'csharp'),
                ('🌊 Go', 'go'),
                ('💎 Ruby', 'ruby'),
                ('🏗️ C++', 'cpp'),
                ('⚡ Kotlin', 'kotlin'),
                ('🎯 Swift', 'swift')
            ]
        ),
        inquirer.Checkbox(
            'favorite_frameworks',
            message="Quali framework usi più spesso?",
            choices=[
                ('⚛️ React', 'react'),
                ('🖖 Vue.js', 'vue'),
                ('🅰️ Angular', 'angular'),
                ('🔥 Laravel', 'laravel'),
                ('🐍 Django', 'django'),
                ('⚡ FastAPI', 'fastapi'),
                ('🚀 Express.js', 'express'),
                ('🍃 Spring Boot', 'spring'),
                ('🔷 .NET', 'dotnet'),
                ('🦀 Axum', 'axum'),
                ('💎 Ruby on Rails', 'rails')
            ]
        ),
        inquirer.List(
            'coding_style',
            message="Che stile di codifica preferisci?",
            choices=[
                ('🎯 Minimalista e pulito', 'minimal'),
                ('📝 Documentato e verboso', 'verbose'),
                ('🔧 Pragmatico e funzionale', 'pragmatic'),
                ('🏗️ Strutturato e formale', 'structured')
            ],
            default='pragmatic'
        ),
        inquirer.Confirm(
            'auto_git_backup',
            message="Vuoi attivare il backup automatico su Git?",
            default=True
        ),
        inquirer.Confirm(
            'use_mcp_by_default',
            message="Vuoi consultare i server MCP per default?",
            default=True
        ),
        inquirer.List(
            'project_structure_preference',
            message="Che struttura di progetto preferisci?",
            choices=[
                ('📁 Flat (file nella root)', 'flat'),
                ('🏗️ Modular (directory separate)', 'modular'),
                ('🌳 Hierarchical (struttura ad albero)', 'hierarchical'),
                ('🎯 Domain-driven (per dominio)', 'domain_driven')
            ],
            default='modular'
        )
    ]
    
    answers = inquirer.prompt(questions)
    
    return answers

def ask_git_configuration() -> Dict:
    """Ask questions for Git integration setup"""
    
    console.print(Panel(
        "🔄 [bold]Configurazione Git[/bold]\n\n"
        "Configura l'integrazione automatica con GitHub",
        title="[bold blue]Git Integration[/bold blue]",
        border_style="blue"
    ))
    
    questions = [
        inquirer.Confirm(
            'has_github_token',
            message="Hai già un token GitHub personale?",
            default=False
        ),
        inquirer.Text(
            'github_username',
            message="Inserisci il tuo username GitHub:"
        ),
        inquirer.List(
            'backup_frequency',
            message="Con che frequenza vuoi fare il backup automatico?",
            choices=[
                ('🔄 Dopo ogni sessione', 'session'),
                ('📅 Giornaliero', 'daily'),
                ('📆 Settimanale', 'weekly'),
                ('🎯 Solo quando richiesto', 'manual')
            ],
            default='session'
        ),
        inquirer.Confirm(
            'create_new_repos',
            message="Vuoi che AiGENIO possa creare nuovi repository?",
            default=True
        ),
        inquirer.Text(
            'default_commit_message',
            message="Messaggio di commit di default:",
            default="Context Engineering - Auto-backup"
        )
    ]
    
    answers = inquirer.prompt(questions)
    
    return answers

def show_summary(answers: Dict, title: str = "Riepilogo Configurazione"):
    """Show a summary of the answers"""
    
    summary_text = ""
    for key, value in answers.items():
        if isinstance(value, list):
            value_str = ", ".join(value) if value else "Nessuna"
        elif isinstance(value, bool):
            value_str = "Sì" if value else "No"
        else:
            value_str = str(value)
        
        # Format key for display
        key_display = key.replace('_', ' ').title()
        summary_text += f"• {key_display}: {value_str}\n"
    
    console.print(Panel(
        summary_text,
        title=f"[bold green]{title}[/bold green]",
        border_style="green"
    ))

def confirm_proceed(message: str = "Vuoi procedere con questa configurazione?") -> bool:
    """Ask user to confirm before proceeding"""
    
    question = inquirer.Confirm('confirm', message=message, default=True)
    answer = inquirer.prompt([question])
    return answer['confirm']