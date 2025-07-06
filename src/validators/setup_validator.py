"""
Validatore setup Context Engineering
"""

from pathlib import Path
from typing import Dict, List, Any
import re

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import read_file, calculate_file_stats


class SetupValidator:
    """Valida configurazione Context Engineering"""
    
    def __init__(self):
        self.required_sections = [
            'Descrizione Progetto',
            'Regole Context Engineering',
            'Best Practices',
            'Workflow'
        ]
        
        self.claude_md_checks = [
            self._check_file_exists,
            self._check_file_length,
            self._check_required_sections,
            self._check_project_info,
            self._check_setup_instructions,
            self._check_best_practices,
            self._check_workflow_defined
        ]
    
    def validate_setup(self, project_path: Path) -> Dict[str, Any]:
        """Valida setup basic Context Engineering"""
        score = 0
        max_score = 10
        errors = []
        warnings = []
        
        # Verifica CLAUDE.md
        claude_result = self._validate_claude_md(project_path)
        score += claude_result['score']
        errors.extend(claude_result['errors'])
        warnings.extend(claude_result['warnings'])
        
        # Verifica struttura directory
        structure_result = self._validate_directory_structure(project_path)
        score += structure_result['score']
        errors.extend(structure_result['errors'])
        warnings.extend(structure_result['warnings'])
        
        return {
            'score': min(10, score),
            'max_score': max_score,
            'errors': errors,
            'warnings': warnings,
            'grade': self._calculate_grade(score, max_score)
        }
    
    def validate_full(self, project_path: Path) -> Dict[str, Any]:
        """Validazione completa del progetto"""
        score = 0
        max_score = 20
        errors = []
        warnings = []
        suggestions = []
        
        # Validazione base
        basic_result = self.validate_setup(project_path)
        score += basic_result['score']
        errors.extend(basic_result['errors'])
        warnings.extend(basic_result['warnings'])
        
        # Validazione avanzata
        advanced_result = self._validate_advanced_setup(project_path)
        score += advanced_result['score']
        errors.extend(advanced_result['errors'])
        warnings.extend(advanced_result['warnings'])
        suggestions.extend(advanced_result['suggestions'])
        
        # Validazione qualità
        quality_result = self._validate_quality(project_path)
        score += quality_result['score']
        warnings.extend(quality_result['warnings'])
        suggestions.extend(quality_result['suggestions'])
        
        return {
            'score': min(10, int((score / max_score) * 10)),
            'max_score': 10,
            'errors': errors,
            'warnings': warnings,
            'suggestions': suggestions,
            'grade': self._calculate_grade(score, max_score),
            'details': {
                'basic': basic_result,
                'advanced': advanced_result,
                'quality': quality_result
            }
        }
    
    def _validate_claude_md(self, project_path: Path) -> Dict[str, Any]:
        """Valida file CLAUDE.md"""
        score = 0
        errors = []
        warnings = []
        
        claude_path = project_path / 'CLAUDE.md'
        
        for check in self.claude_md_checks:
            result = check(claude_path)
            score += result['score']
            errors.extend(result['errors'])
            warnings.extend(result['warnings'])
        
        return {
            'score': min(7, score),
            'errors': errors,
            'warnings': warnings
        }
    
    def _validate_directory_structure(self, project_path: Path) -> Dict[str, Any]:
        """Valida struttura directory"""
        score = 0
        errors = []
        warnings = []
        
        # Verifica directory .claude
        claude_dir = project_path / '.claude'
        if claude_dir.exists():
            score += 1
            
            # Verifica examples
            examples_dir = claude_dir / 'examples'
            if examples_dir.exists():
                score += 1
            else:
                warnings.append("Directory .claude/examples/ non trovata")
        else:
            warnings.append("Directory .claude/ non trovata")
        
        # Verifica .context-engineer
        ce_dir = project_path / '.context-engineer'
        if ce_dir.exists():
            score += 1
            
            # Verifica config.json
            config_file = ce_dir / 'config.json'
            if config_file.exists():
                score += 0.5
            else:
                warnings.append("File .context-engineer/config.json non trovato")
        else:
            warnings.append("Directory .context-engineer/ non trovata")
        
        return {
            'score': min(3, score),
            'errors': errors,
            'warnings': warnings
        }
    
    def _validate_advanced_setup(self, project_path: Path) -> Dict[str, Any]:
        """Validazione setup avanzato"""
        score = 0
        errors = []
        warnings = []
        suggestions = []
        
        # Verifica INITIAL.md
        initial_path = project_path / 'INITIAL.md'
        if initial_path.exists():
            score += 2
            initial_result = self._validate_initial_md(initial_path)
            score += initial_result['score']
            warnings.extend(initial_result['warnings'])
        else:
            suggestions.append("Creare INITIAL.md per documentare feature corrente")
        
        # Verifica esempi
        examples_result = self._validate_examples(project_path)
        score += examples_result['score']
        warnings.extend(examples_result['warnings'])
        suggestions.extend(examples_result['suggestions'])
        
        # Verifica configurazioni framework-specifiche
        framework_result = self._validate_framework_config(project_path)
        score += framework_result['score']
        suggestions.extend(framework_result['suggestions'])
        
        return {
            'score': min(7, score),
            'errors': errors,
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    def _validate_quality(self, project_path: Path) -> Dict[str, Any]:
        """Valida qualità configurazione"""
        score = 0
        warnings = []
        suggestions = []
        
        # Verifica completezza documentazione
        doc_result = self._validate_documentation_completeness(project_path)
        score += doc_result['score']
        suggestions.extend(doc_result['suggestions'])
        
        # Verifica consistenza
        consistency_result = self._validate_consistency(project_path)
        score += consistency_result['score']
        warnings.extend(consistency_result['warnings'])
        
        # Verifica best practices
        practices_result = self._validate_best_practices(project_path)
        score += practices_result['score']
        suggestions.extend(practices_result['suggestions'])
        
        return {
            'score': min(3, score),
            'warnings': warnings,
            'suggestions': suggestions
        }
    
    # Check functions per CLAUDE.md
    def _check_file_exists(self, claude_path: Path) -> Dict[str, Any]:
        """Verifica esistenza CLAUDE.md"""
        if claude_path.exists():
            return {'score': 1, 'errors': [], 'warnings': []}
        else:
            return {'score': 0, 'errors': ['CLAUDE.md non trovato'], 'warnings': []}
    
    def _check_file_length(self, claude_path: Path) -> Dict[str, Any]:
        """Verifica lunghezza file"""
        if not claude_path.exists():
            return {'score': 0, 'errors': [], 'warnings': []}
        
        content = read_file(claude_path)
        length = len(content)
        
        if length > 1000:
            return {'score': 1, 'errors': [], 'warnings': []}
        elif length > 500:
            return {'score': 0.5, 'errors': [], 'warnings': ['CLAUDE.md potrebbe essere più dettagliato']}
        else:
            return {'score': 0, 'errors': [], 'warnings': ['CLAUDE.md troppo breve']}
    
    def _check_required_sections(self, claude_path: Path) -> Dict[str, Any]:
        """Verifica sezioni richieste"""
        if not claude_path.exists():
            return {'score': 0, 'errors': [], 'warnings': []}
        
        content = read_file(claude_path)
        score = 0
        warnings = []
        
        for section in self.required_sections:
            if section.lower() in content.lower():
                score += 0.5
            else:
                warnings.append(f"Sezione '{section}' mancante in CLAUDE.md")
        
        return {'score': min(2, score), 'errors': [], 'warnings': warnings}
    
    def _check_project_info(self, claude_path: Path) -> Dict[str, Any]:
        """Verifica informazioni progetto"""
        if not claude_path.exists():
            return {'score': 0, 'errors': [], 'warnings': []}
        
        content = read_file(claude_path)
        score = 0
        warnings = []
        
        # Verifica presenza di informazioni chiave
        info_patterns = [
            r'(tipo.*progetto|project.*type)',
            r'(framework|tecnologie)',
            r'(linguaggi|languages)',
            r'(descrizione|description)'
        ]
        
        for pattern in info_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                score += 0.25
        
        if score < 0.5:
            warnings.append("CLAUDE.md dovrebbe includere più informazioni sul progetto")
        
        return {'score': min(1, score), 'errors': [], 'warnings': warnings}
    
    def _check_setup_instructions(self, claude_path: Path) -> Dict[str, Any]:
        """Verifica istruzioni setup"""
        if not claude_path.exists():
            return {'score': 0, 'errors': [], 'warnings': []}
        
        content = read_file(claude_path)
        score = 0
        warnings = []
        
        setup_patterns = [
            r'(setup|installazione|installation)',
            r'(comando|command|run)',
            r'(ambiente|environment)',
            r'(dipendenze|dependencies)'
        ]
        
        for pattern in setup_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                score += 0.25
        
        if score < 0.5:
            warnings.append("CLAUDE.md dovrebbe includere istruzioni di setup")
        
        return {'score': min(1, score), 'errors': [], 'warnings': warnings}
    
    def _check_best_practices(self, claude_path: Path) -> Dict[str, Any]:
        """Verifica best practices"""
        if not claude_path.exists():
            return {'score': 0, 'errors': [], 'warnings': []}
        
        content = read_file(claude_path)
        score = 0
        warnings = []
        
        if 'best practices' in content.lower() or 'buone pratiche' in content.lower():
            score += 0.5
        else:
            warnings.append("CLAUDE.md dovrebbe includere best practices")
        
        if 'convenzioni' in content.lower() or 'conventions' in content.lower():
            score += 0.5
        else:
            warnings.append("CLAUDE.md dovrebbe definire convenzioni di codice")
        
        return {'score': min(1, score), 'errors': [], 'warnings': warnings}
    
    def _check_workflow_defined(self, claude_path: Path) -> Dict[str, Any]:
        """Verifica definizione workflow"""
        if not claude_path.exists():
            return {'score': 0, 'errors': [], 'warnings': []}
        
        content = read_file(claude_path)
        score = 0
        warnings = []
        
        workflow_patterns = [
            r'(workflow|flusso.*lavoro)',
            r'(step|passi|processo)',
            r'(1\.|2\.|3\.)',  # Numerazione
            r'(prima|poi|dopo|infine)'
        ]
        
        for pattern in workflow_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                score += 0.25
        
        if score < 0.5:
            warnings.append("CLAUDE.md dovrebbe definire un workflow di sviluppo")
        
        return {'score': min(1, score), 'errors': [], 'warnings': warnings}
    
    def _validate_initial_md(self, initial_path: Path) -> Dict[str, Any]:
        """Valida INITIAL.md"""
        content = read_file(initial_path)
        score = 0
        warnings = []
        
        required_sections = ['descrizione', 'obiettivi', 'implementazione', 'criteri']
        
        for section in required_sections:
            if section in content.lower():
                score += 0.25
        
        if len(content) < 500:
            warnings.append("INITIAL.md dovrebbe essere più dettagliato")
        
        return {'score': min(1, score), 'warnings': warnings}
    
    def _validate_examples(self, project_path: Path) -> Dict[str, Any]:
        """Valida esempi nel progetto"""
        score = 0
        warnings = []
        suggestions = []
        
        examples_dir = project_path / '.claude' / 'examples'
        if examples_dir.exists():
            examples = list(examples_dir.glob('*.md'))
            if examples:
                score += 1
                if len(examples) > 2:
                    score += 0.5
            else:
                warnings.append("Directory examples/ vuota")
        else:
            suggestions.append("Creare directory .claude/examples/ con esempi rappresentativi")
        
        return {'score': min(1.5, score), 'warnings': warnings, 'suggestions': suggestions}
    
    def _validate_framework_config(self, project_path: Path) -> Dict[str, Any]:
        """Valida configurazioni framework-specifiche"""
        score = 0
        suggestions = []
        
        # Verifica configurazioni comuni
        config_files = [
            'package.json', 'composer.json', 'requirements.txt',
            'tsconfig.json', 'webpack.config.js', 'vite.config.js'
        ]
        
        found_configs = 0
        for config_file in config_files:
            if (project_path / config_file).exists():
                found_configs += 1
        
        if found_configs > 0:
            score += 1
        
        if found_configs < 2:
            suggestions.append("Considerare aggiungere più configurazioni framework-specifiche")
        
        return {'score': min(1, score), 'suggestions': suggestions}
    
    def _validate_documentation_completeness(self, project_path: Path) -> Dict[str, Any]:
        """Valida completezza documentazione"""
        score = 0
        suggestions = []
        
        # Verifica presenza README
        readme_files = ['README.md', 'readme.md', 'README.txt']
        if any((project_path / readme).exists() for readme in readme_files):
            score += 0.5
        else:
            suggestions.append("Creare README.md con informazioni base del progetto")
        
        # Verifica documentazione API
        if (project_path / 'docs').exists():
            score += 0.5
        else:
            suggestions.append("Considerare creare directory docs/ per documentazione")
        
        return {'score': min(1, score), 'suggestions': suggestions}
    
    def _validate_consistency(self, project_path: Path) -> Dict[str, Any]:
        """Valida consistenza configurazione"""
        score = 1  # Base score
        warnings = []
        
        claude_path = project_path / 'CLAUDE.md'
        if claude_path.exists():
            claude_content = read_file(claude_path)
            
            # Verifica che le informazioni siano consistenti
            # (implementazione semplificata)
            if len(claude_content) > 100:
                score += 0.5
        
        return {'score': min(1, score), 'warnings': warnings}
    
    def _validate_best_practices(self, project_path: Path) -> Dict[str, Any]:
        """Valida implementazione best practices"""
        score = 0
        suggestions = []
        
        # Verifica .gitignore
        if (project_path / '.gitignore').exists():
            score += 0.5
        else:
            suggestions.append("Creare .gitignore appropriato")
        
        # Verifica presenza test
        test_dirs = ['test', 'tests', '__tests__', 'spec']
        if any((project_path / test_dir).exists() for test_dir in test_dirs):
            score += 0.5
        else:
            suggestions.append("Implementare test suite per il progetto")
        
        return {'score': min(1, score), 'suggestions': suggestions}
    
    def _calculate_grade(self, score: float, max_score: float) -> str:
        """Calcola voto in lettere"""
        percentage = (score / max_score) * 100
        
        if percentage >= 90:
            return 'A+'
        elif percentage >= 85:
            return 'A'
        elif percentage >= 80:
            return 'A-'
        elif percentage >= 75:
            return 'B+'
        elif percentage >= 70:
            return 'B'
        elif percentage >= 65:
            return 'B-'
        elif percentage >= 60:
            return 'C+'
        elif percentage >= 55:
            return 'C'
        elif percentage >= 50:
            return 'C-'
        else:
            return 'D'