#!/usr/bin/env python3
"""
Context Engineering Supervisor Agent CLI
Automatizza setup e gestione Context Engineering per tutti i progetti
"""

import click
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import ContextEngineerAgent
from utils import setup_logging, print_status, print_error, print_success
from interface import show_main_menu, get_menu_choice, show_welcome_message, show_command_list, show_next_steps
from interface import ask_new_project_questions, ask_existing_project_questions


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.pass_context
def cli(ctx, verbose, debug):
    """Context Engineering Supervisor - Il tuo assistente per Claude Code"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['debug'] = debug
    setup_logging(verbose, debug)


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--force', is_flag=True, help='Forza setup anche se già configurato')
@click.option('--template', help='Template specifico da utilizzare')
@click.pass_context
def setup(ctx, project_path, force, template):
    """Setup Context Engineering per un nuovo progetto"""
    try:
        project_path = Path(project_path).resolve()
        agent = ContextEngineerAgent(verbose=ctx.obj['verbose'])
        
        print_status(f"🚀 Avvio setup Context Engineering per: {project_path}")
        
        # Controlla se già configurato
        if not force and (project_path / 'CLAUDE.md').exists():
            print_error("❌ Progetto già configurato! Usa --force per sovrascrivere")
            return
            
        result = agent.setup_project(project_path, template=template)
        
        if result['status'] == 'success':
            print_success(f"✅ Setup completato!")
            print_status(f"📊 Tipo progetto: {result['project_type']}")
            print_status(f"🔧 Framework: {result['framework']}")
            print_status(f"⭐ Score qualità: {result['score']}/10")
            
            print_status("\n📋 Prossimi passi:")
            for step in result['next_steps']:
                print_status(f"  • {step}")
                
        else:
            print_error(f"❌ Setup fallito: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print_error(f"❌ Errore durante setup: {str(e)}")
        if ctx.obj['debug']:
            import traceback
            traceback.print_exc()


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--export', help='Esporta analisi in formato JSON')
@click.pass_context
def analyze(ctx, project_path, export):
    """Analizza progetto esistente e suggerisce miglioramenti"""
    try:
        project_path = Path(project_path).resolve()
        agent = ContextEngineerAgent(verbose=ctx.obj['verbose'])
        
        print_status(f"🔍 Analisi progetto: {project_path}")
        
        analysis = agent.analyze_project(project_path)
        
        print_status(f"📊 Risultati analisi:")
        print_status(f"  • Tipo: {analysis['type']}")
        print_status(f"  • Framework: {analysis['framework']}")
        print_status(f"  • Linguaggi: {', '.join(analysis['languages'])}")
        print_status(f"  • Score Context Engineering: {analysis['ce_score']}/10")
        
        if analysis['issues']:
            print_status(f"\n⚠️  Problemi trovati:")
            for issue in analysis['issues']:
                print_status(f"  • {issue}")
                
        if analysis['suggestions']:
            print_status(f"\n💡 Suggerimenti:")
            for suggestion in analysis['suggestions']:
                print_status(f"  • {suggestion}")
                
        if export:
            export_path = Path(export)
            export_path.write_text(json.dumps(analysis, indent=2))
            print_success(f"✅ Analisi esportata in: {export_path}")
            
    except Exception as e:
        print_error(f"❌ Errore durante analisi: {str(e)}")
        if ctx.obj['debug']:
            import traceback
            traceback.print_exc()


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--feature', prompt='Descrivi la feature da implementare')
@click.option('--template', help='Template INITIAL.md da utilizzare')
@click.pass_context
def generate(ctx, project_path, feature, template):
    """Genera INITIAL.md per nuova feature"""
    try:
        project_path = Path(project_path).resolve()
        agent = ContextEngineerAgent(verbose=ctx.obj['verbose'])
        
        print_status(f"🎯 Generazione INITIAL.md per: {feature}")
        
        result = agent.generate_feature(project_path, feature, template=template)
        
        if result['status'] == 'success':
            print_success(f"✅ INITIAL.md generato: {result['file_path']}")
            print_status(f"📝 Sezioni create: {', '.join(result['sections'])}")
            
            if result['prp_suggestions']:
                print_status(f"\n🔧 PRP suggeriti:")
                for prp in result['prp_suggestions']:
                    print_status(f"  • {prp}")
                    
        else:
            print_error(f"❌ Generazione fallita: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print_error(f"❌ Errore durante generazione: {str(e)}")
        if ctx.obj['debug']:
            import traceback
            traceback.print_exc()


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.pass_context
def validate(ctx, project_path):
    """Valida configurazione Context Engineering esistente"""
    try:
        project_path = Path(project_path).resolve()
        agent = ContextEngineerAgent(verbose=ctx.obj['verbose'])
        
        print_status(f"🔍 Validazione configurazione: {project_path}")
        
        result = agent.validate_project(project_path)
        
        print_status(f"📊 Score validazione: {result['score']}/10")
        
        if result['errors']:
            print_status(f"\n❌ Errori trovati:")
            for error in result['errors']:
                print_status(f"  • {error}")
                
        if result['warnings']:
            print_status(f"\n⚠️  Avvisi:")
            for warning in result['warnings']:
                print_status(f"  • {warning}")
                
        if result['suggestions']:
            print_status(f"\n💡 Suggerimenti:")
            for suggestion in result['suggestions']:
                print_status(f"  • {suggestion}")
                
        if result['score'] >= 8:
            print_success("✅ Configurazione eccellente!")
        elif result['score'] >= 6:
            print_status("⚠️  Configurazione buona, ma migliorabile")
        else:
            print_error("❌ Configurazione necessita miglioramenti")
            
    except Exception as e:
        print_error(f"❌ Errore durante validazione: {str(e)}")
        if ctx.obj['debug']:
            import traceback
            traceback.print_exc()


@cli.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--output', help='File output per report')
@click.pass_context
def report(ctx, project_path, output):
    """Genera report completo del progetto"""
    try:
        project_path = Path(project_path).resolve()
        agent = ContextEngineerAgent(verbose=ctx.obj['verbose'])
        
        print_status(f"📊 Generazione report per: {project_path}")
        
        report_data = agent.generate_report(project_path)
        
        if output:
            output_path = Path(output)
            output_path.write_text(json.dumps(report_data, indent=2))
            print_success(f"✅ Report salvato in: {output_path}")
        else:
            print_status("📈 Report generato:")
            print_status(json.dumps(report_data, indent=2))
            
    except Exception as e:
        print_error(f"❌ Errore durante generazione report: {str(e)}")
        if ctx.obj['debug']:
            import traceback
            traceback.print_exc()


@cli.command()
@click.pass_context
def templates(ctx):
    """Lista template disponibili"""
    try:
        agent = ContextEngineerAgent(verbose=ctx.obj['verbose'])
        templates = agent.list_templates()
        
        print_status("📋 Template disponibili:")
        for category, items in templates.items():
            print_status(f"\n{category.upper()}:")
            for item in items:
                print_status(f"  • {item['name']}: {item['description']}")
                
    except Exception as e:
        print_error(f"❌ Errore durante lista template: {str(e)}")
        if ctx.obj['debug']:
            import traceback
            traceback.print_exc()


@cli.command()
@click.pass_context
def menu(ctx):
    """Avvia il menu interattivo principale"""
    try:
        while True:
            show_main_menu()
            choice = get_menu_choice()
            
            if choice is None:  # User chose to exit
                break
            elif choice == 1:  # Nuovo Progetto
                handle_new_project(ctx)
            elif choice == 2:  # Apri Progetto
                handle_open_project(ctx)
            elif choice == 3:  # Lista Comandi
                show_command_list()
                
    except Exception as e:
        print_error(f"❌ Errore nel menu: {str(e)}")
        if ctx.obj['debug']:
            import traceback
            traceback.print_exc()


def handle_new_project(ctx):
    """Gestisce la creazione di un nuovo progetto"""
    try:
        # Ask comprehensive questions
        answers = ask_new_project_questions()
        
        # Get project path
        project_path = click.prompt("Inserisci il percorso del progetto", type=click.Path())
        project_path = Path(project_path).resolve()
        
        # Create project directory if it doesn't exist
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Setup project with answers
        agent = ContextEngineerAgent(verbose=ctx.obj['verbose'])
        result = agent.setup_project(project_path, config=answers)
        
        if result['status'] == 'success':
            print_success("✅ Progetto creato con successo!")
            
            next_steps = [
                "Rivedi i file CLAUDE.md e INITIAL.md generati",
                "Configura l'ambiente di sviluppo",
                "Inizia a sviluppare seguendo le best practices",
                "Usa 'python -m src.cli validate' per verificare la configurazione"
            ]
            
            if answers.get('use_git_integration'):
                next_steps.append("Configura l'integrazione Git con 'python -m src.cli setup-git'")
            
            show_next_steps(next_steps)
        else:
            print_error(f"❌ Creazione progetto fallita: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print_error(f"❌ Errore durante creazione progetto: {str(e)}")
        if ctx.obj['debug']:
            import traceback
            traceback.print_exc()


def handle_open_project(ctx):
    """Gestisce l'apertura di un progetto esistente"""
    try:
        # Ask for project path
        project_path = click.prompt("Inserisci il percorso del progetto", type=click.Path(exists=True))
        project_path = Path(project_path).resolve()
        
        # Ask questions for existing project
        answers = ask_existing_project_questions()
        
        # Analyze project
        agent = ContextEngineerAgent(verbose=ctx.obj['verbose'])
        analysis = agent.analyze_project(project_path, config=answers)
        
        print_status(f"📊 Analisi completata per: {project_path}")
        print_status(f"  • Score Context Engineering: {analysis['ce_score']}/10")
        
        if analysis['suggestions']:
            print_status(f"\n💡 Suggerimenti:")
            for suggestion in analysis['suggestions']:
                print_status(f"  • {suggestion}")
        
        next_steps = [
            "Rivedi i suggerimenti di miglioramento",
            "Implementa le correzioni consigliate",
            "Riesegui l'analisi per verificare i miglioramenti"
        ]
        
        if answers.get('generate_improvement_plan'):
            next_steps.append("Genera un piano di miglioramento dettagliato")
        
        show_next_steps(next_steps)
        
    except Exception as e:
        print_error(f"❌ Errore durante apertura progetto: {str(e)}")
        if ctx.obj['debug']:
            import traceback
            traceback.print_exc()


if __name__ == '__main__':
    # If no arguments provided, show interactive menu
    if len(sys.argv) == 1:
        ctx = click.Context(cli)
        ctx.obj = {'verbose': False, 'debug': False}
        setup_logging(False, False)
        
        from interface.menu import show_welcome_message
        show_welcome_message()
        
        menu.invoke(ctx)
    else:
        cli()