"""
Generatore configurazione CLAUDE.md
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from jinja2 import Template

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import load_json, read_file


class ClaudeConfigGenerator:
    """Genera configurazione CLAUDE.md appropriata per il progetto"""
    
    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent.parent / 'templates'
        
        # Template base per diversi tipi di progetto
        self.base_templates = {
            'web': self._get_web_template(),
            'api': self._get_api_template(),
            'mobile': self._get_mobile_template(),
            'desktop': self._get_desktop_template(),
            'library': self._get_library_template(),
            'data': self._get_data_template(),
            'unknown': self._get_generic_template()
        }
        
        # Sezioni specifiche per framework
        self.framework_sections = {
            'laravel': self._get_laravel_section(),
            'react': self._get_react_section(),
            'vue': self._get_vue_section(),
            'django': self._get_django_section(),
            'flask': self._get_flask_section(),
            'express': self._get_express_section(),
            'next': self._get_next_section()
        }
    
    def generate(self, analysis: Dict[str, Any], template_name: Optional[str] = None) -> Dict[str, Any]:
        """Genera configurazione CLAUDE.md basata su analisi progetto"""
        
        # Seleziona template appropriato
        if template_name:
            template_content = self._load_custom_template(template_name)
        else:
            template_content = self._select_template(analysis)
        
        # Prepara contesto per template
        context = self._build_context(analysis)
        
        # Genera contenuto
        template = Template(template_content)
        content = template.render(**context)
        
        # Aggiungi sezioni framework-specifiche
        content = self._add_framework_sections(content, analysis)
        
        return {
            'content': content,
            'template_used': template_name or analysis['type'],
            'sections': self._extract_sections(content),
            'generated_at': datetime.now().isoformat()
        }
    
    def _select_template(self, analysis: Dict[str, Any]) -> str:
        """Seleziona template appropriato basato su analisi"""
        project_type = analysis.get('type', 'unknown')
        return self.base_templates.get(project_type, self.base_templates['unknown'])
    
    def _load_custom_template(self, template_name: str) -> str:
        """Carica template personalizzato"""
        template_path = self.templates_dir / f"{template_name}.md"
        if template_path.exists():
            return read_file(template_path)
        return self.base_templates['unknown']
    
    def _build_context(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Costruisce contesto per template"""
        return {
            'project_name': analysis.get('name', 'Progetto'),
            'project_type': analysis.get('type', 'unknown'),
            'framework': analysis.get('framework', 'unknown'),
            'languages': analysis.get('languages', []),
            'has_tests': analysis.get('has_tests', False),
            'has_docs': analysis.get('has_docs', False),
            'complexity': analysis.get('complexity', 'medium'),
            'architecture': analysis.get('architecture', {}),
            'tech_stack': analysis.get('frameworks_detected', {}),
            'generated_date': datetime.now().strftime('%Y-%m-%d'),
            'custom_sections': self._generate_custom_sections(analysis)
        }
    
    def _generate_custom_sections(self, analysis: Dict[str, Any]) -> Dict[str, str]:
        """Genera sezioni personalizzate basate su analisi"""
        sections = {}
        
        # Sezione setup development
        if analysis.get('framework') in ['laravel', 'symfony']:
            sections['setup_dev'] = self._generate_php_setup(analysis)
        elif analysis.get('framework') in ['react', 'vue', 'angular']:
            sections['setup_dev'] = self._generate_js_setup(analysis)
        elif analysis.get('framework') in ['django', 'flask']:
            sections['setup_dev'] = self._generate_python_setup(analysis)
        
        # Sezione testing
        if analysis.get('has_tests'):
            sections['testing'] = self._generate_testing_section(analysis)
        
        # Sezione deployment
        sections['deployment'] = self._generate_deployment_section(analysis)
        
        return sections
    
    def _generate_php_setup(self, analysis: Dict[str, Any]) -> str:
        """Genera sezione setup per progetti PHP"""
        setup = "## Setup Ambiente di Sviluppo\n\n"
        
        if analysis.get('framework') == 'laravel':
            setup += """
### Laravel Setup
```bash
# Installa dipendenze
composer install

# Copia configurazione
cp .env.example .env

# Genera chiave applicazione
php artisan key:generate

# Esegui migrazioni
php artisan migrate

# Avvia server di sviluppo
php artisan serve
```

### Testing
```bash
# Esegui test
php artisan test

# Test specifici
php artisan test --filter TestName
```
"""
        else:
            setup += """
### PHP Setup
```bash
# Installa dipendenze
composer install

# Configura ambiente
cp .env.example .env

# Avvia server
php -S localhost:8000
```
"""
        
        return setup
    
    def _generate_js_setup(self, analysis: Dict[str, Any]) -> str:
        """Genera sezione setup per progetti JavaScript"""
        setup = "## Setup Ambiente di Sviluppo\n\n"
        
        framework = analysis.get('framework', '')
        
        if framework in ['react', 'vue', 'angular']:
            setup += f"""
### {framework.title()} Setup
```bash
# Installa dipendenze
npm install
# oppure
yarn install

# Avvia server di sviluppo
npm start
# oppure
yarn start

# Build per produzione
npm run build
# oppure
yarn build
```

### Testing
```bash
# Esegui test
npm test

# Test con coverage
npm run test:coverage
```
"""
        elif framework == 'next':
            setup += """
### Next.js Setup
```bash
# Installa dipendenze
npm install

# Avvia server di sviluppo
npm run dev

# Build per produzione
npm run build
npm start
```
"""
        else:
            setup += """
### JavaScript Setup
```bash
# Installa dipendenze
npm install

# Avvia applicazione
npm start
```
"""
        
        return setup
    
    def _generate_python_setup(self, analysis: Dict[str, Any]) -> str:
        """Genera sezione setup per progetti Python"""
        setup = "## Setup Ambiente di Sviluppo\n\n"
        
        framework = analysis.get('framework', '')
        
        if framework == 'django':
            setup += """
### Django Setup
```bash
# Crea ambiente virtuale
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oppure
venv\\Scripts\\activate  # Windows

# Installa dipendenze
pip install -r requirements.txt

# Esegui migrazioni
python manage.py migrate

# Crea superuser
python manage.py createsuperuser

# Avvia server
python manage.py runserver
```

### Testing
```bash
# Esegui test
python manage.py test

# Test specifici
python manage.py test app.tests.TestName
```
"""
        elif framework == 'flask':
            setup += """
### Flask Setup
```bash
# Crea ambiente virtuale
python -m venv venv
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt

# Imposta variabili ambiente
export FLASK_APP=app.py
export FLASK_ENV=development

# Avvia server
flask run
```
"""
        else:
            setup += """
### Python Setup
```bash
# Crea ambiente virtuale
python -m venv venv
source venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt

# Avvia applicazione
python main.py
```
"""
        
        return setup
    
    def _generate_testing_section(self, analysis: Dict[str, Any]) -> str:
        """Genera sezione testing"""
        framework = analysis.get('framework', '')
        
        if framework == 'laravel':
            return """
## Testing

### Comandi Test
```bash
# Tutti i test
php artisan test

# Test specifici
php artisan test --filter TestName

# Test con coverage
php artisan test --coverage
```

### Best Practices
- Usa Factory per dati di test
- Implementa test Feature e Unit
- Testa API endpoints
- Verifica autenticazione e autorizzazione
"""
        elif framework in ['react', 'vue', 'angular']:
            return """
## Testing

### Comandi Test
```bash
# Tutti i test
npm test

# Test specifici
npm test -- --testNamePattern="TestName"

# Test con coverage
npm run test:coverage
```

### Best Practices
- Testa componenti isolatamente
- Usa mock per API calls
- Testa user interactions
- Verifica accessibility
"""
        else:
            return """
## Testing

### Comandi Test
```bash
# Esegui test
npm test
# oppure
python -m pytest
```

### Best Practices
- Scrivi test unitari
- Testa casi edge
- Mantieni alta copertura
- Usa fixture per dati
"""
    
    def _generate_deployment_section(self, analysis: Dict[str, Any]) -> str:
        """Genera sezione deployment"""
        framework = analysis.get('framework', '')
        
        base_deployment = """
## Deployment

### Preparazione
1. Verifica tutti i test passino
2. Aggiorna documentazione
3. Verifica configurazione produzione
4. Backup database (se necessario)

### Processo Deploy
"""
        
        if framework == 'laravel':
            base_deployment += """
```bash
# Ottimizza per produzione
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Esegui migrazioni
php artisan migrate --force

# Installa dipendenze produzione
composer install --optimize-autoloader --no-dev
```
"""
        elif framework in ['react', 'vue', 'angular', 'next']:
            base_deployment += """
```bash
# Build per produzione
npm run build

# Deploy su hosting
# (varia per provider)
```
"""
        elif framework in ['django', 'flask']:
            base_deployment += """
```bash
# Installa dipendenze
pip install -r requirements.txt

# Configura variabili ambiente
export DATABASE_URL=...
export SECRET_KEY=...

# Esegui migrazioni (Django)
python manage.py migrate

# Avvia server produzione
gunicorn app:app
```
"""
        
        return base_deployment
    
    def _add_framework_sections(self, content: str, analysis: Dict[str, Any]) -> str:
        """Aggiunge sezioni specifiche del framework"""
        framework = analysis.get('framework', '')
        
        if framework in self.framework_sections:
            framework_section = self.framework_sections[framework]
            content += f"\n\n{framework_section}"
        
        return content
    
    def _extract_sections(self, content: str) -> List[str]:
        """Estrae sezioni dal contenuto generato"""
        sections = []
        lines = content.split('\n')
        
        for line in lines:
            if line.startswith('## '):
                section_name = line.replace('## ', '').strip()
                sections.append(section_name)
        
        return sections
    
    # Template base per diversi tipi di progetto
    def _get_web_template(self) -> str:
        return """# {{ project_name }}

**Tipo Progetto**: {{ project_type.title() }}
**Framework**: {{ framework.title() }}
**Linguaggi**: {{ languages | join(', ') }}
**Generato**: {{ generated_date }}

## Descrizione Progetto

Applicazione web {{ framework }} per {{ project_name }}.

## Struttura Progetto

```
{{ project_name }}/
├── src/                 # Codice sorgente
├── public/             # File statici
├── tests/              # Test
├── docs/               # Documentazione
└── config/             # Configurazione
```

## Regole Context Engineering

### Convenzioni Codice
- Usa nomi descrittivi per variabili e funzioni
- Mantieni funzioni piccole e focalizzate
- Commenta logica complessa
- Segui standard del framework {{ framework }}

### Best Practices
- Implementa error handling appropriato
- Valida input utente
- Ottimizza performance
- Mantieni sicurezza

### Workflow
1. Analizza requisiti
2. Pianifica implementazione
3. Scrivi test
4. Implementa feature
5. Testa e ottimizza
6. Documenta changes

{{ custom_sections.setup_dev if custom_sections.setup_dev else '' }}

{{ custom_sections.testing if custom_sections.testing else '' }}

{{ custom_sections.deployment if custom_sections.deployment else '' }}

## Note Specifiche

{% if complexity == 'high' %}
⚠️ **Progetto Complesso**: Prestare attenzione a:
- Architettura modulare
- Gestione dipendenze
- Performance optimization
- Monitoring e logging
{% endif %}

{% if has_tests %}
✅ **Testing**: Progetto con suite di test esistente
{% else %}
❌ **Testing**: Implementare test per nuove funzionalità
{% endif %}

{% if has_docs %}
📚 **Documentazione**: Aggiornare docs/README per nuove feature
{% endif %}

---
*Configurazione generata automaticamente da Context Engineering Agent*
"""
    
    def _get_api_template(self) -> str:
        return """# {{ project_name }} API

**Tipo Progetto**: API/Backend
**Framework**: {{ framework.title() }}
**Linguaggi**: {{ languages | join(', ') }}
**Generato**: {{ generated_date }}

## Descrizione API

API {{ framework }} per {{ project_name }}.

## Architettura

```
{{ project_name }}/
├── controllers/        # Controller API
├── models/            # Modelli dati
├── middleware/        # Middleware
├── routes/            # Definizione route
├── services/          # Logica business
├── config/            # Configurazione
└── tests/             # Test API
```

## Regole Context Engineering

### API Design
- Usa RESTful conventions
- Implementa proper HTTP status codes
- Valida input richieste
- Gestisci errori gracefully
- Documenta endpoints

### Security
- Implementa autenticazione
- Valida autorizzazioni
- Sanitizza input
- Proteggi contro CSRF/XSS
- Usa HTTPS in produzione

### Performance
- Implementa caching
- Ottimizza query database
- Usa pagination per liste
- Monitora performance

{{ custom_sections.setup_dev if custom_sections.setup_dev else '' }}

{{ custom_sections.testing if custom_sections.testing else '' }}

{{ custom_sections.deployment if custom_sections.deployment else '' }}

## Endpoints Principali

Documenta qui i principali endpoints API:

```
GET    /api/v1/resource      # Lista risorse
POST   /api/v1/resource      # Crea risorsa
GET    /api/v1/resource/:id  # Dettaglio risorsa
PUT    /api/v1/resource/:id  # Aggiorna risorsa
DELETE /api/v1/resource/:id  # Elimina risorsa
```

---
*Configurazione generata automaticamente da Context Engineering Agent*
"""
    
    def _get_mobile_template(self) -> str:
        return """# {{ project_name }} Mobile

**Tipo Progetto**: Mobile App
**Framework**: {{ framework.title() }}
**Linguaggi**: {{ languages | join(', ') }}
**Generato**: {{ generated_date }}

## Descrizione App

Applicazione mobile {{ framework }} per {{ project_name }}.

## Struttura

```
{{ project_name }}/
├── src/
│   ├── components/     # Componenti UI
│   ├── screens/        # Schermate app
│   ├── services/       # API services
│   ├── utils/          # Utilities
│   └── assets/         # Immagini, fonts
├── tests/              # Test
└── docs/               # Documentazione
```

## Regole Context Engineering

### Mobile Best Practices
- Ottimizza per performance mobile
- Gestisci stati offline
- Implementa loading states
- Ottimizza immagini
- Testa su dispositivi reali

### UI/UX
- Segui platform guidelines
- Implementa responsive design
- Gestisci keyboard appropriately
- Ottimizza touch interactions

{{ custom_sections.setup_dev if custom_sections.setup_dev else '' }}

{{ custom_sections.testing if custom_sections.testing else '' }}

---
*Configurazione generata automaticamente da Context Engineering Agent*
"""
    
    def _get_desktop_template(self) -> str:
        return """# {{ project_name }} Desktop

**Tipo Progetto**: Desktop App
**Framework**: {{ framework.title() }}
**Linguaggi**: {{ languages | join(', ') }}
**Generato**: {{ generated_date }}

## Descrizione

Applicazione desktop {{ framework }} per {{ project_name }}.

## Regole Context Engineering

### Desktop Best Practices
- Ottimizza startup time
- Gestisci window states
- Implementa keyboard shortcuts
- Gestisci file system access
- Ottimizza memory usage

{{ custom_sections.setup_dev if custom_sections.setup_dev else '' }}

---
*Configurazione generata automaticamente da Context Engineering Agent*
"""
    
    def _get_library_template(self) -> str:
        return """# {{ project_name }} Library

**Tipo Progetto**: Library/Package
**Framework**: {{ framework.title() }}
**Linguaggi**: {{ languages | join(', ') }}
**Generato**: {{ generated_date }}

## Descrizione

Libreria {{ framework }} per {{ project_name }}.

## Regole Context Engineering

### Library Best Practices
- Mantieni API stabile
- Implementa comprehensive testing
- Documenta API public
- Gestisci backward compatibility
- Ottimizza bundle size

{{ custom_sections.setup_dev if custom_sections.setup_dev else '' }}

---
*Configurazione generata automaticamente da Context Engineering Agent*
"""
    
    def _get_data_template(self) -> str:
        return """# {{ project_name }} Data Project

**Tipo Progetto**: Data Science/Analytics
**Framework**: {{ framework.title() }}
**Linguaggi**: {{ languages | join(', ') }}
**Generato**: {{ generated_date }}

## Descrizione

Progetto di analisi dati per {{ project_name }}.

## Regole Context Engineering

### Data Science Best Practices
- Documenta data sources
- Implementa data validation
- Versiona datasets
- Riproducibilità esperimenti
- Visualizza risultati

{{ custom_sections.setup_dev if custom_sections.setup_dev else '' }}

---
*Configurazione generata automaticamente da Context Engineering Agent*
"""
    
    def _get_generic_template(self) -> str:
        return """# {{ project_name }}

**Tipo Progetto**: {{ project_type.title() }}
**Framework**: {{ framework.title() }}
**Linguaggi**: {{ languages | join(', ') }}
**Generato**: {{ generated_date }}

## Descrizione Progetto

Progetto {{ project_name }} sviluppato con {{ framework }}.

## Regole Context Engineering

### Best Practices Generali
- Usa nomi descrittivi
- Mantieni codice pulito
- Implementa testing
- Documenta changes
- Segui convenzioni del linguaggio

### Workflow
1. Analizza requisiti
2. Pianifica implementazione
3. Implementa soluzione
4. Testa funzionalità
5. Documenta changes

{{ custom_sections.setup_dev if custom_sections.setup_dev else '' }}

{{ custom_sections.testing if custom_sections.testing else '' }}

---
*Configurazione generata automaticamente da Context Engineering Agent*
"""
    
    # Sezioni specifiche framework
    def _get_laravel_section(self) -> str:
        return """
## Laravel Specifiche

### Convenzioni Laravel
- Usa Eloquent ORM per database
- Implementa Form Requests per validation
- Usa Resource Controllers
- Implementa Service Classes per logica business
- Usa Jobs per task asincroni

### Artisan Commands
```bash
# Crea model con migration
php artisan make:model ModelName -m

# Crea controller
php artisan make:controller ControllerName

# Crea middleware
php artisan make:middleware MiddlewareName

# Crea job
php artisan make:job JobName
```

### Testing Laravel
- Usa Feature tests per endpoint
- Usa Unit tests per logica business
- Usa Database factories
- Implementa test per API
"""
    
    def _get_react_section(self) -> str:
        return """
## React Specifiche

### Convenzioni React
- Usa functional components con hooks
- Implementa proper state management
- Usa useEffect per side effects
- Implementa error boundaries
- Ottimizza re-renders

### Best Practices
- Usa TypeScript per type safety
- Implementa prop-types o TypeScript
- Usa React.memo per optimization
- Implementa custom hooks
- Mantieni componenti piccoli
"""
    
    def _get_vue_section(self) -> str:
        return """
## Vue Specifiche

### Convenzioni Vue
- Usa Composition API
- Implementa reactive state
- Usa computed properties
- Implementa watchers appropriately
- Usa Vue Router per navigation

### Best Practices
- Usa TypeScript con Vue
- Implementa Pinia per state management
- Mantieni componenti single-responsibility
- Usa slots per flexibility
"""
    
    def _get_django_section(self) -> str:
        return """
## Django Specifiche

### Convenzioni Django
- Usa Django ORM
- Implementa Class-based views
- Usa Django Forms
- Implementa Django REST Framework per API
- Usa Django Admin

### Best Practices
- Usa migrations per database changes
- Implementa custom managers
- Usa signals appropriately
- Implementa caching
- Usa Django security features
"""
    
    def _get_flask_section(self) -> str:
        return """
## Flask Specifiche

### Convenzioni Flask
- Usa Blueprint per organization
- Implementa Flask-SQLAlchemy
- Usa Flask-WTF per forms
- Implementa Flask-Login per auth
- Usa Flask-Migrate per database

### Best Practices
- Usa application factory pattern
- Implementa proper error handling
- Usa Flask-RESTful per API
- Implementa testing con pytest
"""
    
    def _get_express_section(self) -> str:
        return """
## Express Specifiche

### Convenzioni Express
- Usa middleware per request processing
- Implementa proper routing
- Usa template engines
- Implementa error handling middleware
- Usa database ODM/ORM

### Best Practices
- Usa environment variables
- Implementa logging
- Usa helmet per security
- Implementa rate limiting
- Usa compression middleware
"""
    
    def _get_next_section(self) -> str:
        return """
## Next.js Specifiche

### Convenzioni Next.js
- Usa App Router (Next.js 13+)
- Implementa Server Components
- Usa API Routes
- Implementa proper SEO
- Usa Image optimization

### Best Practices
- Usa TypeScript
- Implementa ISR quando appropriato
- Usa next/image per immagini
- Implementa proper error pages
- Ottimizza Core Web Vitals
"""