"""
Context Engineering Supervisor Agent
Core logic per automazione Context Engineering
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict

from analyzers.project_analyzer import ProjectAnalyzer
from analyzers.framework_detector import FrameworkDetector
from generators.claude_config_generator import ClaudeConfigGenerator
from generators.initial_generator import InitialGenerator
from generators.prp_generator import PRPGenerator
from validators.setup_validator import SetupValidator
from utils import ensure_dir, copy_template, load_json, save_json


@dataclass
class ProjectInfo:
    """Informazioni base del progetto"""
    path: Path
    name: str
    type: str
    framework: str
    languages: List[str]
    has_claude_config: bool
    has_initial: bool
    ce_score: int
    created_at: datetime
    updated_at: datetime


class ContextEngineerAgent:
    """Agente che supervisiona setup Context Engineering"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)
        
        # Inizializza componenti
        self.project_analyzer = ProjectAnalyzer()
        self.framework_detector = FrameworkDetector()
        self.claude_generator = ClaudeConfigGenerator()
        self.initial_generator = InitialGenerator()
        self.prp_generator = PRPGenerator()
        self.validator = SetupValidator()
        
        # Directory di configurazione
        self.config_dir = Path.home() / '.context-engineer'
        self.templates_dir = Path(__file__).parent.parent / 'templates'
        
        # Assicura che le directory esistano
        ensure_dir(self.config_dir)
        
        # Carica configurazioni esistenti
        self.projects_db = self._load_projects_db()
        
    def _load_projects_db(self) -> Dict[str, Any]:
        """Carica database progetti dalla configurazione"""
        db_path = self.config_dir / 'projects.json'
        if db_path.exists():
            return load_json(db_path)
        return {'projects': {}, 'last_updated': datetime.now().isoformat()}
    
    def _save_projects_db(self):
        """Salva database progetti"""
        db_path = self.config_dir / 'projects.json'
        self.projects_db['last_updated'] = datetime.now().isoformat()
        save_json(db_path, self.projects_db)
    
    def setup_project(self, project_path: Path, template: Optional[str] = None) -> Dict[str, Any]:
        """Setup completo Context Engineering per progetto con logging dettagliato"""
        try:
            self.logger.info(f"🚀 INIZIO setup per progetto: {project_path}")
            self.logger.info(f"📋 Template richiesto: {template}")
            
            # Verifica path e permessi
            if not project_path.exists():
                project_path.mkdir(parents=True, exist_ok=True)
                self.logger.info(f"📁 Directory creata: {project_path}")
            
            if not os.access(project_path, os.W_OK):
                raise PermissionError(f"Nessun permesso di scrittura: {project_path}")
            
            self.logger.info(f"✅ Permessi verificati")
            
            # 1. Analizza struttura e tecnologie
            try:
                self.logger.info(f"🔍 STEP 1: Avvio analisi progetto...")
                analysis = self.analyze_project(project_path)
                self.logger.info(f"✅ STEP 1 completato: {analysis.get('type', 'unknown')}")
            except Exception as e:
                self.logger.error(f"💥 STEP 1 FALLITO: {e}")
                raise
            
            # 2. Genera CLAUDE.md appropriato
            try:
                self.logger.info(f"🔍 STEP 2: Generando CLAUDE.md...")
                claude_config = self.claude_generator.generate(analysis, template)
                self.logger.info(f"✅ STEP 2a: Config generata")
                
                # 3. Crea file CLAUDE.md
                claude_path = project_path / 'CLAUDE.md'
                claude_path.write_text(claude_config['content'])
                self.logger.info(f"✅ STEP 2b: CLAUDE.md scritto ({claude_path.stat().st_size} bytes)")
            except Exception as e:
                self.logger.error(f"💥 STEP 2 FALLITO: {e}")
                raise
            
            # 3.5. Genera INITIAL.md di default per il progetto
            try:
                self.logger.info(f"🔍 STEP 3: Generando INITIAL.md...")
                initial_content = self.initial_generator.generate(
                    analysis, 
                    f"Setup iniziale progetto {analysis['name']}", 
                    template
                )
                self.logger.info(f"✅ STEP 3a: Content generato")
                
                initial_path = project_path / 'INITIAL.md'
                initial_path.write_text(initial_content['content'])
                self.logger.info(f"✅ STEP 3b: INITIAL.md scritto ({initial_path.stat().st_size} bytes)")
            except Exception as e:
                self.logger.error(f"💥 STEP 3 FALLITO: {e}")
                raise
            
            # 4. Crea struttura directories se necessaria
            try:
                self.logger.info(f"🔍 STEP 4: Creando struttura directory...")
                self._create_project_structure(project_path, analysis)
                self.logger.info(f"✅ STEP 4 completato")
            except Exception as e:
                self.logger.error(f"💥 STEP 4 FALLITO: {e}")
                raise
            
            # 5. Copia esempi rappresentativi
            try:
                self.logger.info(f"🔍 STEP 5: Copiando esempi...")
                examples = self._copy_examples(project_path, analysis)
                self.logger.info(f"✅ STEP 5 completato: {len(examples)} esempi")
            except Exception as e:
                self.logger.error(f"💥 STEP 5 FALLITO: {e}")
                raise
            
            # 6. Genera configurazione .context-engineer
            try:
                self.logger.info(f"🔍 STEP 6: Creando configurazione...")
                self._create_project_config(project_path, analysis)
                self.logger.info(f"✅ STEP 6 completato")
            except Exception as e:
                self.logger.error(f"💥 STEP 6 FALLITO: {e}")
                raise
            
            # 7. Verifica che tutti i file necessari siano stati creati
            verification = self._verify_complete_setup(project_path)
            if not verification['success']:
                self.logger.warning(f"Setup incompleto: {verification['missing_files']}")
            
            # 8. Valida setup
            validation = self.validator.validate_setup(project_path)
            
            # 9. Aggiorna database progetti
            self._update_project_db(project_path, analysis, validation['score'])
            
            return {
                'status': 'success',
                'project_type': analysis['type'],
                'framework': analysis['framework'],
                'score': validation['score'],
                'files_created': [
                    str(claude_path),
                    str(initial_path),
                    *examples,
                    str(project_path / '.context-engineer' / 'config.json')
                ],
                'next_steps': self._suggest_next_steps(analysis, validation)
            }
            
        except Exception as e:
            self.logger.error(f"💥 ERRORE CRITICO durante setup: {str(e)}")
            import traceback
            self.logger.error(f"Traceback completo: {traceback.format_exc()}")
            
            # Crea log file di debug
            debug_log_path = '/tmp/aigenio_debug.log'
            try:
                with open(debug_log_path, 'a', encoding='utf-8') as f:
                    f.write(f"\n=== CRASH SETUP PROGETTO - {datetime.now()} ===\n")
                    f.write(f"Project path: {project_path}\n")
                    f.write(f"Template: {template}\n")
                    f.write(f"Error: {str(e)}\n")
                    f.write(f"Traceback:\n{traceback.format_exc()}\n")
                    f.write("=== END CRASH LOG ===\n\n")
                
                self.logger.error(f"📝 Log di debug salvato in: {debug_log_path}")
            except Exception as log_error:
                self.logger.error(f"Errore anche nel salvare log: {log_error}")
            
            return {
                'status': 'error',
                'error': str(e),
                'debug_log': debug_log_path
            }
    
    def analyze_project(self, project_path: Path) -> Dict[str, Any]:
        """Analizza progetto esistente con logging dettagliato"""
        try:
            self.logger.info(f"🔍 INIZIO analisi progetto: {project_path}")
            
            # Verifica esistenza e permessi
            if not project_path.exists():
                raise FileNotFoundError(f"Path progetto non trovato: {project_path}")
            
            if not os.access(project_path, os.R_OK):
                raise PermissionError(f"Nessun permesso di lettura: {project_path}")
            
            self.logger.info(f"✅ Path e permessi verificati")
            
            # Analisi base struttura
            try:
                self.logger.info(f"🔍 Analizzando struttura progetto...")
                structure = self.project_analyzer.analyze_structure(project_path)
                self.logger.info(f"✅ Struttura analizzata: tipo={structure.get('type', 'unknown')}")
            except Exception as e:
                self.logger.error(f"💥 ERRORE in analyze_structure: {e}")
                import traceback
                self.logger.error(f"Traceback: {traceback.format_exc()}")
                raise
            
            # Rilevamento framework
            try:
                self.logger.info(f"🔍 Rilevando framework...")
                framework_info = self.framework_detector.detect(project_path)
                self.logger.info(f"✅ Framework rilevato: {framework_info.get('primary', 'unknown')}")
            except Exception as e:
                self.logger.error(f"💥 ERRORE in framework_detector: {e}")
                import traceback
                self.logger.error(f"Traceback: {traceback.format_exc()}")
                raise
            
            # Analisi linguaggi
            try:
                self.logger.info(f"🔍 Analizzando linguaggi...")
                languages = self.project_analyzer.detect_languages(project_path)
                self.logger.info(f"✅ Linguaggi rilevati: {languages}")
            except Exception as e:
                self.logger.error(f"💥 ERRORE in detect_languages: {e}")
                import traceback
                self.logger.error(f"Traceback: {traceback.format_exc()}")
                raise
            
            # Analisi Context Engineering esistente
            try:
                self.logger.info(f"🔍 Analizzando Context Engineering esistente...")
                ce_analysis = self._analyze_existing_ce(project_path)
                self.logger.info(f"✅ CE analysis completato")
            except Exception as e:
                self.logger.error(f"💥 ERRORE in _analyze_existing_ce: {e}")
                import traceback
                self.logger.error(f"Traceback: {traceback.format_exc()}")
                raise
            
            # Calcola score generale
            try:
                self.logger.info(f"🔍 Calcolando score CE...")
                score = self._calculate_ce_score(project_path, structure, framework_info, ce_analysis)
                self.logger.info(f"✅ Score calcolato: {score}")
            except Exception as e:
                self.logger.error(f"💥 ERRORE in _calculate_ce_score: {e}")
                import traceback
                self.logger.error(f"Traceback: {traceback.format_exc()}")
                raise
            
            # Costruzione risultato finale
            try:
                self.logger.info(f"🔍 Costruendo risultato analisi...")
                
                result = {
                    'path': str(project_path),
                    'name': project_path.name,
                    'type': structure.get('type', 'unknown'),
                    'framework': framework_info.get('primary', 'unknown'),
                    'frameworks_detected': framework_info.get('all', []),
                    'languages': languages if languages else ['unknown'],
                    'structure': structure,
                    'ce_score': score if score else 5,
                    'has_claude_config': (project_path / 'CLAUDE.md').exists(),
                    'has_initial': (project_path / 'INITIAL.md').exists(),
                    'issues': ce_analysis.get('issues', []),
                    'suggestions': ce_analysis.get('suggestions', []),
                    'complexity': structure.get('complexity', 'medium'),
                    'files_count': structure.get('files_count', 0),
                    'analyzed_at': datetime.now().isoformat()
                }
                
                self.logger.info(f"✅ ANALISI COMPLETATA con successo")
                return result
                
            except Exception as e:
                self.logger.error(f"💥 ERRORE nella costruzione risultato: {e}")
                import traceback
                self.logger.error(f"Traceback: {traceback.format_exc()}")
                raise
            
        except Exception as e:
            self.logger.error(f"💥 ERRORE CRITICO durante analisi: {str(e)}")
            import traceback
            self.logger.error(f"Traceback completo: {traceback.format_exc()}")
            
            # Crea log file di debug
            debug_log_path = '/tmp/aigenio_debug.log'
            try:
                with open(debug_log_path, 'a', encoding='utf-8') as f:
                    f.write(f"\n=== CRASH ANALISI PROGETTO - {datetime.now()} ===\n")
                    f.write(f"Project path: {project_path}\n")
                    f.write(f"Error: {str(e)}\n")
                    f.write(f"Traceback:\n{traceback.format_exc()}\n")
                    f.write("=== END CRASH LOG ===\n\n")
                
                self.logger.error(f"📝 Log di debug salvato in: {debug_log_path}")
            except Exception as log_error:
                self.logger.error(f"Errore anche nel salvare log: {log_error}")
            
            raise
    
    def generate_feature(self, project_path: Path, feature_description: str, template: Optional[str] = None) -> Dict[str, Any]:
        """Genera INITIAL.md per nuova feature"""
        try:
            self.logger.info(f"Generazione feature: {feature_description}")
            
            # Analizza progetto per contesto
            analysis = self.analyze_project(project_path)
            
            # Genera INITIAL.md
            initial_content = self.initial_generator.generate(
                analysis, 
                feature_description, 
                template
            )
            
            # Salva INITIAL.md
            initial_path = project_path / 'INITIAL.md'
            initial_path.write_text(initial_content['content'])
            
            # Genera PRP suggeriti
            prp_suggestions = self.prp_generator.suggest_prps(
                analysis, 
                feature_description
            )
            
            return {
                'status': 'success',
                'file_path': str(initial_path),
                'sections': initial_content['sections'],
                'prp_suggestions': prp_suggestions,
                'estimated_complexity': initial_content['complexity'],
                'estimated_time': initial_content['estimated_time']
            }
            
        except Exception as e:
            self.logger.error(f"Errore durante generazione feature: {str(e)}")
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def validate_project(self, project_path: Path) -> Dict[str, Any]:
        """Valida configurazione Context Engineering esistente"""
        try:
            return self.validator.validate_full(project_path)
            
        except Exception as e:
            self.logger.error(f"Errore durante validazione: {str(e)}")
            raise
    
    def generate_report(self, project_path: Path) -> Dict[str, Any]:
        """Genera report completo del progetto"""
        try:
            analysis = self.analyze_project(project_path)
            validation = self.validate_project(project_path)
            
            return {
                'project_info': {
                    'path': str(project_path),
                    'name': project_path.name,
                    'type': analysis['type'],
                    'framework': analysis['framework']
                },
                'analysis': analysis,
                'validation': validation,
                'recommendations': self._generate_recommendations(analysis, validation),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Errore durante generazione report: {str(e)}")
            raise
    
    def list_templates(self) -> Dict[str, List[Dict[str, str]]]:
        """Lista template disponibili"""
        templates = {}
        
        for category_dir in self.templates_dir.iterdir():
            if category_dir.is_dir():
                category = category_dir.name
                templates[category] = []
                
                for template_file in category_dir.glob('*.json'):
                    template_info = load_json(template_file)
                    templates[category].append({
                        'name': template_file.stem,
                        'description': template_info.get('description', ''),
                        'framework': template_info.get('framework', ''),
                        'complexity': template_info.get('complexity', 'medium')
                    })
        
        return templates
    
    def _analyze_existing_ce(self, project_path: Path) -> Dict[str, Any]:
        """Analizza Context Engineering esistente"""
        issues = []
        suggestions = []
        
        # Controlla CLAUDE.md
        claude_path = project_path / 'CLAUDE.md'
        if not claude_path.exists():
            issues.append("CLAUDE.md mancante")
            suggestions.append("Creare CLAUDE.md con configurazione progetto")
        else:
            # Analizza contenuto CLAUDE.md
            claude_content = claude_path.read_text()
            if len(claude_content) < 100:
                issues.append("CLAUDE.md troppo breve")
                suggestions.append("Espandere CLAUDE.md con più dettagli")
        
        # Controlla struttura .claude/
        claude_dir = project_path / '.claude'
        if not claude_dir.exists():
            suggestions.append("Creare directory .claude/ per configurazioni avanzate")
        
        return {
            'issues': issues,
            'suggestions': suggestions
        }
    
    def _calculate_ce_score(self, project_path: Path, structure: Dict, framework_info: Dict, ce_analysis: Dict) -> int:
        """Calcola score Context Engineering (1-10)"""
        score = 5  # Base score
        
        # Bonus per CLAUDE.md esistente
        if (project_path / 'CLAUDE.md').exists():
            score += 2
        
        # Bonus per struttura organizzata
        if structure['complexity'] == 'low':
            score += 1
        elif structure['complexity'] == 'high':
            score -= 1
        
        # Bonus per framework riconosciuto
        if framework_info['primary'] != 'unknown':
            score += 1
        
        # Malus per problemi trovati
        score -= len(ce_analysis['issues']) * 0.5
        
        # Assicura range 1-10
        return max(1, min(10, int(score)))
    
    def _create_project_structure(self, project_path: Path, analysis: Dict):
        """Crea struttura directory per Context Engineering"""
        # Crea .context-engineer/
        ce_dir = project_path / '.context-engineer'
        ensure_dir(ce_dir)
        
        # Crea .claude/ se non esiste
        claude_dir = project_path / '.claude'
        ensure_dir(claude_dir)
        
        # Crea examples/ se necessario
        if analysis['type'] in ['web', 'api']:
            examples_dir = claude_dir / 'examples'
            ensure_dir(examples_dir)
    
    def _copy_examples(self, project_path: Path, analysis: Dict) -> List[str]:
        """Copia esempi rappresentativi"""
        copied_files = []
        
        # Logica per copiare esempi basata sul tipo di progetto
        framework = analysis['framework']
        project_type = analysis['type']
        
        template_path = self.templates_dir / analysis['type']
        if template_path.exists():
            examples_dir = project_path / '.claude' / 'examples'
            ensure_dir(examples_dir)
            
            # Copia template appropriati
            for example_file in template_path.glob('example_*.md'):
                dest_file = examples_dir / example_file.name
                copy_template(example_file, dest_file)
                copied_files.append(str(dest_file))
        
        return copied_files
    
    def _create_project_config(self, project_path: Path, analysis: Dict):
        """Crea configurazione progetto in .context-engineer/"""
        config = {
            'project_name': analysis['name'],
            'project_type': analysis['type'],
            'framework': analysis['framework'],
            'languages': analysis['languages'],
            'setup_date': datetime.now().isoformat(),
            'version': '1.0.0',
            'agent_version': '1.0.0'
        }
        
        config_path = project_path / '.context-engineer' / 'config.json'
        save_json(config_path, config)
    
    def _update_project_db(self, project_path: Path, analysis: Dict, score: int):
        """Aggiorna database progetti"""
        project_key = str(project_path)
        
        self.projects_db['projects'][project_key] = {
            'name': analysis['name'],
            'type': analysis['type'],
            'framework': analysis['framework'],
            'score': score,
            'last_setup': datetime.now().isoformat(),
            'path': project_key
        }
        
        self._save_projects_db()
    
    def _suggest_next_steps(self, analysis: Dict, validation: Dict) -> List[str]:
        """Suggerisce prossimi passi dopo setup"""
        steps = []
        
        # Passi base
        steps.append("Creare INITIAL.md per la prima feature")
        steps.append("Testare configurazione con Claude Code")
        
        # Passi specifici per framework
        if analysis['framework'] == 'laravel':
            steps.append("Configurare database e migrazioni")
            steps.append("Impostare testing con PHPUnit")
        elif analysis['framework'] == 'react':
            steps.append("Configurare testing con Jest")
            steps.append("Impostare build e deployment")
        
        # Passi basati su score
        if validation['score'] < 7:
            steps.append("Migliorare configurazione CLAUDE.md")
            steps.append("Aggiungere più esempi in .claude/examples/")
        
        return steps
    
    def _generate_recommendations(self, analysis: Dict, validation: Dict) -> List[str]:
        """Genera raccomandazioni basate su analisi e validazione"""
        recommendations = []
        
        # Raccomandazioni basate su score
        if validation['score'] < 6:
            recommendations.append("Configurazione Context Engineering necessita miglioramenti significativi")
        elif validation['score'] < 8:
            recommendations.append("Configurazione buona ma può essere ottimizzata")
        else:
            recommendations.append("Configurazione eccellente!")
        
        # Raccomandazioni specifiche
        if not analysis['has_claude_config']:
            recommendations.append("Creare CLAUDE.md con istruzioni dettagliate")
        
        if analysis['complexity'] == 'high':
            recommendations.append("Considerare suddivisione in moduli più piccoli")
        
        return recommendations
    
    def _verify_complete_setup(self, project_path: Path) -> Dict[str, Any]:
        """Verifica che tutti i file necessari siano stati creati"""
        required_files = {
            'CLAUDE.md': 'Regole e istruzioni per AI assistant',
            'INITIAL.md': 'Feature request iniziale per il progetto'
        }
        
        missing_files = []
        existing_files = []
        
        for file_name, description in required_files.items():
            file_path = project_path / file_name
            if file_path.exists() and file_path.stat().st_size > 0:
                existing_files.append({
                    'name': file_name,
                    'path': str(file_path),
                    'size': file_path.stat().st_size,
                    'description': description
                })
                self.logger.info(f"✅ {file_name} creato correttamente ({file_path.stat().st_size} bytes)")
            else:
                missing_files.append({
                    'name': file_name,
                    'description': description,
                    'expected_path': str(file_path)
                })
                self.logger.error(f"❌ {file_name} mancante o vuoto")
        
        # Verifica opzionali utili
        optional_files = {
            'README.md': 'Documentazione del progetto',
            '.env.example': 'Template variabili ambiente'
        }
        
        optional_existing = []
        for file_name, description in optional_files.items():
            file_path = project_path / file_name
            if file_path.exists():
                optional_existing.append({
                    'name': file_name,
                    'description': description
                })
        
        success = len(missing_files) == 0
        
        return {
            'success': success,
            'required_files': required_files,
            'existing_files': existing_files,
            'missing_files': missing_files,
            'optional_existing': optional_existing,
            'verification_status': 'complete' if success else 'incomplete',
            'total_required': len(required_files),
            'total_existing': len(existing_files)
        }