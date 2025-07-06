"""
Utility functions per Context Engineering Agent
"""

import json
import logging
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


def setup_logging(verbose: bool = False, debug: bool = False):
    """Configura logging per l'agente"""
    level = logging.DEBUG if debug else (logging.INFO if verbose else logging.WARNING)
    
    # Assicura che la directory .context-engineer esista
    log_dir = Path.home() / '.context-engineer'
    ensure_dir(log_dir)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_dir / 'agent.log')
        ]
    )


def print_status(message: str):
    """Stampa messaggio di status"""
    print(f"ℹ️  {message}")


def print_success(message: str):
    """Stampa messaggio di successo"""
    print(f"✅ {message}")


def print_error(message: str):
    """Stampa messaggio di errore"""
    print(f"❌ {message}")


def ensure_dir(path: Path):
    """Assicura che una directory esista"""
    path.mkdir(parents=True, exist_ok=True)


def copy_template(src: Path, dest: Path):
    """Copia template file"""
    if src.exists():
        shutil.copy2(src, dest)
        return True
    return False


def load_json(path: Path) -> Dict[str, Any]:
    """Carica file JSON"""
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_json(path: Path, data: Dict[str, Any]):
    """Salva file JSON"""
    ensure_dir(path.parent)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_file(path: Path) -> str:
    """Legge file di testo"""
    if path.exists():
        return path.read_text(encoding='utf-8')
    return ""


def write_file(path: Path, content: str):
    """Scrive file di testo"""
    ensure_dir(path.parent)
    path.write_text(content, encoding='utf-8')


def get_file_extension(path: Path) -> str:
    """Ottiene estensione file"""
    return path.suffix.lower()


def is_text_file(path: Path) -> bool:
    """Verifica se è un file di testo"""
    text_extensions = {
        '.py', '.js', '.ts', '.jsx', '.tsx', '.php', '.html', '.css', '.scss',
        '.json', '.xml', '.yaml', '.yml', '.md', '.txt', '.sql', '.sh', '.bat'
    }
    return get_file_extension(path) in text_extensions


def calculate_file_stats(project_path: Path) -> Dict[str, Any]:
    """Calcola statistiche file progetto"""
    stats = {
        'total_files': 0,
        'text_files': 0,
        'directories': 0,
        'size_mb': 0,
        'extensions': {}
    }
    
    for item in project_path.rglob('*'):
        if item.is_file():
            stats['total_files'] += 1
            stats['size_mb'] += item.stat().st_size / (1024 * 1024)
            
            ext = get_file_extension(item)
            stats['extensions'][ext] = stats['extensions'].get(ext, 0) + 1
            
            if is_text_file(item):
                stats['text_files'] += 1
                
        elif item.is_dir():
            stats['directories'] += 1
    
    stats['size_mb'] = round(stats['size_mb'], 2)
    return stats


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """Formatta timestamp"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def truncate_text(text: str, max_length: int = 100) -> str:
    """Tronca testo se troppo lungo"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def normalize_path(path: str) -> Path:
    """Normalizza path"""
    return Path(path).expanduser().resolve()


def get_relative_path(file_path: Path, base_path: Path) -> Path:
    """Ottiene path relativo"""
    try:
        return file_path.relative_to(base_path)
    except ValueError:
        return file_path


def find_files_by_pattern(directory: Path, pattern: str) -> list[Path]:
    """Trova file per pattern"""
    return list(directory.rglob(pattern))


def find_files_by_extension(directory: Path, extension: str) -> list[Path]:
    """Trova file per estensione"""
    if not extension.startswith('.'):
        extension = '.' + extension
    return list(directory.rglob(f'*{extension}'))


def get_project_name(project_path: Path) -> str:
    """Ottiene nome progetto"""
    # Controlla package.json
    package_json = project_path / 'package.json'
    if package_json.exists():
        data = load_json(package_json)
        if 'name' in data:
            return data['name']
    
    # Controlla composer.json
    composer_json = project_path / 'composer.json'
    if composer_json.exists():
        data = load_json(composer_json)
        if 'name' in data:
            return data['name']
    
    # Usa nome directory
    return project_path.name


def detect_git_repo(project_path: Path) -> bool:
    """Rileva se è un repository git"""
    return (project_path / '.git').exists()


def get_git_branch(project_path: Path) -> Optional[str]:
    """Ottiene branch git corrente"""
    try:
        head_file = project_path / '.git' / 'HEAD'
        if head_file.exists():
            content = head_file.read_text().strip()
            if content.startswith('ref: refs/heads/'):
                return content.replace('ref: refs/heads/', '')
    except:
        pass
    return None


def validate_project_path(path: str) -> Path:
    """Valida e normalizza path progetto"""
    project_path = normalize_path(path)
    
    if not project_path.exists():
        raise ValueError(f"Path non esiste: {project_path}")
    
    if not project_path.is_dir():
        raise ValueError(f"Path non è una directory: {project_path}")
    
    return project_path