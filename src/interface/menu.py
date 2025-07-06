"""
Enhanced CLI menu with ASCII art for AiGENIO by Franco
"""

import os
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

console = Console()

def show_ascii_art():
    """Display the main ASCII art banner for AiGENIO by Franco"""
    
    ascii_art = """
╔═══════════════════════════════════════════════════════════════╗
║        █████╗ ██╗ ██████╗ ███████╗███╗   ██╗██╗ ██████╗       ║
║       ██╔══██╗   ██╔════╝ ██╔════╝████╗  ██║██║██╔═══██╗      ║
║       ███████║██║██║  ███╗█████╗  ██╔██╗ ██║██║██║   ██║      ║
║       ██╔══██║██║██║   ██║██╔══╝  ██║╚██╗██║██║██║   ██║      ║
║       ██║  ██║██║╚██████╔╝███████╗██║ ╚████║██║╚██████╔╝      ║
║       ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝ ╚═════╝       ║
║                                                               ║
║                        ██████╗ ██╗   ██╗                      ║
║                        ██╔══██╗╚██╗ ██╔╝                      ║
║                        ██████╔╝ ╚████╔╝                       ║
║                        ██╔══██╗  ╚██╔╝                        ║
║                        ██████╔╝   ██║                         ║
║                        ╚═════╝    ╚═╝                         ║
║                                                               ║
║       ███████╗██████╗  █████╗ ███╗   ██╗ ██████╗ ██████╗      ║
║       ██╔════╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔═══██╗     ║
║       █████╗  ██████╔╝███████║██╔██╗ ██║██║     ██║   ██║     ║
║       ██╔══╝  ██╔══██╗██╔══██║██║╚██╗██║██║     ██║   ██║     ║
║       ██║     ██║  ██║██║  ██║██║ ╚████║╚██████╗╚██████╔╝     ║
║       ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝      ║
╚═══════════════════════════════════════════════════════════════╝
"""
    
    return ascii_art

def show_main_menu():
    """Display the main menu with ASCII art and options"""
    
    # Clear screen
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Show ASCII art
    ascii_art = show_ascii_art()
    console.print(ascii_art, style="bold cyan")
    
    # Show subtitle
    subtitle = Text("🤖 AI-Powered Context Engineering Assistant", style="bold white")
    console.print(Align.center(subtitle))
    console.print()
    
    # Show menu options
    menu_options = """
┌─────────────────────────────────────────────────────────────────┐
│  1. 🆕 Nuovo Progetto                                            │
│  2. 📂 Apri Progetto                                             │
│  3. 📋 Lista Comandi                                             │
│                                                                   │
│  Seleziona un'opzione (1-3): ▊                                   │
└─────────────────────────────────────────────────────────────────┘
"""
    
    console.print(menu_options, style="bold green")

def get_menu_choice():
    """Get user's menu choice with validation"""
    
    while True:
        try:
            choice = input().strip()
            
            if choice in ['1', '2', '3']:
                return int(choice)
            elif choice.lower() in ['q', 'quit', 'exit']:
                console.print("\n👋 Arrivederci!", style="bold yellow")
                return None
            else:
                console.print("❌ Opzione non valida. Seleziona 1, 2, o 3 (o 'q' per uscire):", style="bold red")
        except KeyboardInterrupt:
            console.print("\n\n👋 Arrivederci!", style="bold yellow")
            return None
        except Exception as e:
            console.print(f"❌ Errore: {e}. Riprova:", style="bold red")

def show_welcome_message():
    """Show welcome message and instructions"""
    
    welcome_panel = Panel(
        """
🎯 [bold]Benvenuto in AiGENIO by Franco![/bold]

Questo strumento ti aiuterà a:
• 🚀 Creare nuovi progetti con best practices
• 📊 Analizzare progetti esistenti
• 🔧 Generare file di configurazione ottimizzati
• 🔄 Integrare backup automatici su GitHub
• 📚 Accedere a best practices aggiornate via MCP

[dim]Suggerimento: Usa 'q' in qualsiasi momento per uscire[/dim]
        """,
        title="[bold blue]AiGENIO Assistant[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    )
    
    console.print(welcome_panel)
    console.print()

def show_command_list():
    """Display available commands"""
    
    commands_panel = Panel(
        """
📋 [bold]Comandi Disponibili:[/bold]

[bold green]Comandi Principali:[/bold green]
• [cyan]setup[/cyan] - Configura un nuovo progetto
• [cyan]analyze[/cyan] - Analizza un progetto esistente
• [cyan]generate[/cyan] - Genera file CLAUDE.md e INITIAL.md
• [cyan]validate[/cyan] - Valida la configurazione del progetto
• [cyan]report[/cyan] - Genera report di analisi
• [cyan]templates[/cyan] - Gestisce i template

[bold blue]Nuove Funzionalità:[/bold blue]
• [cyan]menu[/cyan] - Mostra questo menu interattivo
• [cyan]backup[/cyan] - Backup automatico su GitHub
• [cyan]preferences[/cyan] - Gestisce le preferenze utente
• [cyan]best-practices[/cyan] - Consulta best practices aggiornate

[dim]Usa: python -m src.cli <comando> --help per maggiori dettagli[/dim]
        """,
        title="[bold blue]Lista Comandi[/bold blue]",
        border_style="green",
        padding=(1, 2)
    )
    
    console.print(commands_panel)
    
    input("\nPremi Enter per tornare al menu principale...")

def show_loading_message(message: str):
    """Show a loading message with spinner"""
    
    console.print(f"⏳ {message}...", style="bold yellow")

def show_success_message(message: str):
    """Show a success message"""
    
    console.print(f"✅ {message}", style="bold green")

def show_error_message(message: str):
    """Show an error message"""
    
    console.print(f"❌ {message}", style="bold red")

def show_info_message(message: str):
    """Show an info message"""
    
    console.print(f"ℹ️ {message}", style="bold blue")

def show_next_steps(steps: list):
    """Show suggested next steps"""
    
    if not steps:
        return
    
    steps_panel = Panel(
        "\n".join([f"• {step}" for step in steps]),
        title="[bold blue]📋 Prossimi Passi Suggeriti[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    )
    
    console.print(steps_panel)