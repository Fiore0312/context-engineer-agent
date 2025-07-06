"""
Generatore INITIAL.md per nuove feature
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from jinja2 import Template

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import read_file


class InitialGenerator:
    """Genera file INITIAL.md per nuove feature"""
    
    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent.parent / 'templates'
        
        # Template per diversi tipi di feature
        self.feature_templates = {
            'crud': self._get_crud_template(),
            'api': self._get_api_template(),
            'ui': self._get_ui_template(),
            'auth': self._get_auth_template(),
            'integration': self._get_integration_template(),
            'optimization': self._get_optimization_template(),
            'security': self._get_security_template(),
            'testing': self._get_testing_template(),
            'documentation': self._get_documentation_template(),
            'generic': self._get_generic_template()
        }
    
    def generate(self, analysis: Dict[str, Any], feature_description: str, template: Optional[str] = None) -> Dict[str, Any]:
        """Genera INITIAL.md per la feature specificata"""
        
        # Determina tipo di feature
        feature_type = self._classify_feature(feature_description)
        
        # Seleziona template
        if template:
            template_content = self.feature_templates.get(template, self.feature_templates['generic'])
        else:
            template_content = self.feature_templates.get(feature_type, self.feature_templates['generic'])
        
        # Analizza feature per estrarre dettagli
        feature_details = self._analyze_feature_description(feature_description)
        
        # Costruisci contesto
        context = self._build_context(analysis, feature_description, feature_details)
        
        # Genera contenuto
        template_obj = Template(template_content)
        content = template_obj.render(**context)
        
        # Calcola complessità e tempo stimato
        complexity = self._estimate_complexity(feature_description, analysis)
        estimated_time = self._estimate_time(complexity, feature_type)
        
        return {
            'content': content,
            'feature_type': feature_type,
            'complexity': complexity,
            'estimated_time': estimated_time,
            'sections': self._extract_sections(content),
            'generated_at': datetime.now().isoformat()
        }
    
    def _classify_feature(self, description: str) -> str:
        """Classifica tipo di feature basato su descrizione"""
        description_lower = description.lower()
        
        # Parole chiave per classificazione
        keywords = {
            'crud': ['create', 'read', 'update', 'delete', 'crud', 'gestione', 'gestire', 'tabella', 'form'],
            'api': ['api', 'endpoint', 'rest', 'graphql', 'service', 'microservice', 'integration'],
            'ui': ['ui', 'interface', 'component', 'page', 'design', 'layout', 'frontend', 'view'],
            'auth': ['auth', 'login', 'register', 'user', 'permission', 'role', 'security', 'session'],
            'integration': ['integrate', 'connect', 'sync', 'import', 'export', 'webhook', 'third-party'],
            'optimization': ['optimize', 'performance', 'speed', 'cache', 'faster', 'improve'],
            'security': ['security', 'secure', 'protect', 'encrypt', 'vulnerability', 'ssl', 'https'],
            'testing': ['test', 'testing', 'unit', 'integration', 'coverage', 'quality'],
            'documentation': ['doc', 'document', 'readme', 'guide', 'tutorial', 'help']
        }
        
        # Conta occorrenze per ogni tipo
        scores = {}
        for feature_type, words in keywords.items():
            score = sum(1 for word in words if word in description_lower)
            if score > 0:
                scores[feature_type] = score
        
        # Restituisce tipo con score più alto
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return 'generic'
    
    def _analyze_feature_description(self, description: str) -> Dict[str, Any]:
        """Analizza descrizione feature per estrarre dettagli"""
        details = {
            'entities': [],
            'actions': [],
            'components': [],
            'integrations': [],
            'requirements': []
        }
        
        # Estrai entità (sostantivi)
        entities = self._extract_entities(description)
        details['entities'] = entities
        
        # Estrai azioni (verbi)
        actions = self._extract_actions(description)
        details['actions'] = actions
        
        # Estrai componenti menzionati
        components = self._extract_components(description)
        details['components'] = components
        
        # Estrai integrazioni
        integrations = self._extract_integrations(description)
        details['integrations'] = integrations
        
        # Estrai requisiti
        requirements = self._extract_requirements(description)
        details['requirements'] = requirements
        
        return details
    
    def _extract_entities(self, description: str) -> List[str]:
        """Estrae entità dalla descrizione"""
        # Implementazione semplificata
        common_entities = [
            'user', 'admin', 'product', 'order', 'customer', 'payment',
            'article', 'post', 'category', 'tag', 'comment', 'file',
            'image', 'video', 'document', 'report', 'dashboard'
        ]
        
        found_entities = []
        description_lower = description.lower()
        
        for entity in common_entities:
            if entity in description_lower:
                found_entities.append(entity)
        
        return found_entities
    
    def _extract_actions(self, description: str) -> List[str]:
        """Estrae azioni dalla descrizione"""
        common_actions = [
            'create', 'add', 'insert', 'new',
            'read', 'view', 'show', 'display', 'list',
            'update', 'edit', 'modify', 'change',
            'delete', 'remove', 'cancel',
            'search', 'filter', 'sort',
            'upload', 'download', 'export', 'import',
            'send', 'receive', 'process', 'validate'
        ]
        
        found_actions = []
        description_lower = description.lower()
        
        for action in common_actions:
            if action in description_lower:
                found_actions.append(action)
        
        return found_actions
    
    def _extract_components(self, description: str) -> List[str]:
        """Estrae componenti dalla descrizione"""
        common_components = [
            'form', 'table', 'modal', 'button', 'menu', 'navbar',
            'sidebar', 'footer', 'header', 'card', 'list', 'grid',
            'chart', 'graph', 'calendar', 'datepicker', 'dropdown'
        ]
        
        found_components = []
        description_lower = description.lower()
        
        for component in common_components:
            if component in description_lower:
                found_components.append(component)
        
        return found_components
    
    def _extract_integrations(self, description: str) -> List[str]:
        """Estrae integrazioni dalla descrizione"""
        common_integrations = [
            'email', 'sms', 'notification', 'payment', 'stripe', 'paypal',
            'social', 'facebook', 'google', 'twitter', 'api', 'rest',
            'database', 'redis', 'cache', 'queue', 'webhook'
        ]
        
        found_integrations = []
        description_lower = description.lower()
        
        for integration in common_integrations:
            if integration in description_lower:
                found_integrations.append(integration)
        
        return found_integrations
    
    def _extract_requirements(self, description: str) -> List[str]:
        """Estrae requisiti dalla descrizione"""
        requirements = []
        
        # Cerca pattern di requisiti
        requirement_patterns = [
            'deve', 'should', 'must', 'required', 'need', 'necessary',
            'important', 'essential', 'mandatory', 'obligatory'
        ]
        
        sentences = description.split('.')
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            if any(pattern in sentence_lower for pattern in requirement_patterns):
                requirements.append(sentence.strip())
        
        return requirements
    
    def _build_context(self, analysis: Dict[str, Any], description: str, details: Dict[str, Any]) -> Dict[str, Any]:
        """Costruisce contesto per template"""
        return {
            'project_name': analysis.get('name', 'Progetto'),
            'project_type': analysis.get('type', 'unknown'),
            'framework': analysis.get('framework', 'unknown'),
            'languages': analysis.get('languages', []),
            'feature_description': description,
            'feature_details': details,
            'generated_date': datetime.now().strftime('%Y-%m-%d'),
            'generated_time': datetime.now().strftime('%H:%M:%S'),
            'entities': details.get('entities', []),
            'actions': details.get('actions', []),
            'components': details.get('components', []),
            'integrations': details.get('integrations', []),
            'requirements': details.get('requirements', [])
        }
    
    def _estimate_complexity(self, description: str, analysis: Dict[str, Any]) -> str:
        """Stima complessità della feature"""
        complexity_score = 0
        
        # Lunghezza descrizione
        if len(description) > 500:
            complexity_score += 2
        elif len(description) > 200:
            complexity_score += 1
        
        # Numero di entità/azioni
        details = self._analyze_feature_description(description)
        complexity_score += len(details['entities']) * 0.5
        complexity_score += len(details['actions']) * 0.3
        complexity_score += len(details['integrations']) * 1.5
        
        # Parole chiave complesse
        complex_keywords = [
            'integration', 'security', 'authentication', 'authorization',
            'real-time', 'sync', 'async', 'microservice', 'api',
            'complex', 'advanced', 'multiple', 'system'
        ]
        
        description_lower = description.lower()
        for keyword in complex_keywords:
            if keyword in description_lower:
                complexity_score += 1
        
        # Determina livello
        if complexity_score >= 8:
            return 'very_high'
        elif complexity_score >= 6:
            return 'high'
        elif complexity_score >= 4:
            return 'medium'
        elif complexity_score >= 2:
            return 'low'
        else:
            return 'very_low'
    
    def _estimate_time(self, complexity: str, feature_type: str) -> str:
        """Stima tempo per implementazione"""
        base_times = {
            'crud': {'very_low': '2-4 ore', 'low': '4-8 ore', 'medium': '1-2 giorni', 'high': '2-3 giorni', 'very_high': '3-5 giorni'},
            'api': {'very_low': '3-6 ore', 'low': '6-12 ore', 'medium': '1-3 giorni', 'high': '3-5 giorni', 'very_high': '5-7 giorni'},
            'ui': {'very_low': '2-4 ore', 'low': '4-8 ore', 'medium': '1-2 giorni', 'high': '2-4 giorni', 'very_high': '4-6 giorni'},
            'auth': {'very_low': '4-8 ore', 'low': '8-16 ore', 'medium': '2-3 giorni', 'high': '3-5 giorni', 'very_high': '5-8 giorni'},
            'integration': {'very_low': '4-8 ore', 'low': '8-16 ore', 'medium': '2-4 giorni', 'high': '4-7 giorni', 'very_high': '7-10 giorni'},
            'optimization': {'very_low': '2-4 ore', 'low': '4-8 ore', 'medium': '1-2 giorni', 'high': '2-3 giorni', 'very_high': '3-5 giorni'},
            'security': {'very_low': '4-8 ore', 'low': '8-16 ore', 'medium': '2-3 giorni', 'high': '3-5 giorni', 'very_high': '5-8 giorni'},
            'testing': {'very_low': '2-4 ore', 'low': '4-8 ore', 'medium': '1-2 giorni', 'high': '2-3 giorni', 'very_high': '3-5 giorni'},
            'documentation': {'very_low': '1-2 ore', 'low': '2-4 ore', 'medium': '4-8 ore', 'high': '1-2 giorni', 'very_high': '2-3 giorni'},
            'generic': {'very_low': '2-4 ore', 'low': '4-8 ore', 'medium': '1-2 giorni', 'high': '2-4 giorni', 'very_high': '4-6 giorni'}
        }
        
        return base_times.get(feature_type, base_times['generic']).get(complexity, '1-2 giorni')
    
    def _extract_sections(self, content: str) -> List[str]:
        """Estrae sezioni dal contenuto"""
        sections = []
        for line in content.split('\n'):
            if line.startswith('## '):
                sections.append(line.replace('## ', '').strip())
        return sections
    
    # Template per diversi tipi di feature
    def _get_crud_template(self) -> str:
        return """# FEATURE: {{ feature_description }}

**Tipo**: CRUD Operations
**Progetto**: {{ project_name }}
**Framework**: {{ framework }}
**Complessità**: {{ complexity }}
**Generato**: {{ generated_date }} {{ generated_time }}

## Descrizione

Implementare operazioni CRUD per {{ entities | join(', ') if entities else 'entità' }}.

## Obiettivi

{% for entity in entities %}
- Gestione completa {{ entity }}
{% endfor %}
{% for action in actions %}
- Implementare {{ action }}
{% endfor %}

## Requisiti Tecnici

### Database
- Tabelle necessarie: {{ entities | join(', ') if entities else 'da definire' }}
- Relazioni tra entità
- Indici per performance
- Validazione dati

### Backend
- Model per {{ entities | join(', ') if entities else 'entità' }}
- Controller con metodi CRUD
- Validation rules
- API endpoints (se necessario)

### Frontend
{% for component in components %}
- {{ component.title() }} per gestione
{% endfor %}
{% if not components %}
- Form per create/update
- Lista per visualizzazione
- Conferma per delete
{% endif %}

## Implementazione

### Step 1: Database
```sql
-- Creare migration per tabelle
-- Definire relazioni
-- Aggiungere indici
```

### Step 2: Backend
```
- Creare Model
- Implementare Controller
- Definire routes
- Aggiungere validation
```

### Step 3: Frontend
```
- Creare componenti UI
- Implementare form handling
- Gestire state management
- Aggiungere error handling
```

### Step 4: Testing
```
- Unit tests per Model
- Controller tests
- Integration tests
- UI tests
```

## Criteri di Accettazione

{% for requirement in requirements %}
- {{ requirement }}
{% endfor %}
{% if not requirements %}
- CRUD operations funzionanti
- Validation appropriata
- Error handling implementato
- UI user-friendly
{% endif %}

## Note Tecniche

- Seguire convenzioni {{ framework }}
- Implementare proper error handling
- Ottimizzare query database
- Gestire concorrenza se necessario

## Stima Tempo

**Tempo stimato**: {{ estimated_time }}

---
*Generato automaticamente da Context Engineering Agent*
"""
    
    def _get_api_template(self) -> str:
        return """# FEATURE: {{ feature_description }}

**Tipo**: API Development
**Progetto**: {{ project_name }}
**Framework**: {{ framework }}
**Complessità**: {{ complexity }}
**Generato**: {{ generated_date }} {{ generated_time }}

## Descrizione

Sviluppare API endpoints per {{ feature_description }}.

## Endpoints da Implementare

{% for action in actions %}
- {{ action.upper() }} endpoint
{% endfor %}
{% if not actions %}
- GET /api/resource
- POST /api/resource
- PUT /api/resource/:id
- DELETE /api/resource/:id
{% endif %}

## Specifiche API

### Request/Response Format
```json
{
  "data": {},
  "meta": {
    "status": "success",
    "message": "Operation completed"
  }
}
```

### Authentication
- Implementare authentication middleware
- Validare permissions
- Rate limiting

### Validation
- Input validation
- Business rules validation
- Error responses standardizzate

## Implementazione

### Step 1: Route Definition
```
- Definire routes
- Applicare middleware
- Documentare endpoints
```

### Step 2: Controller Logic
```
- Implementare business logic
- Gestire database operations
- Validare input
```

### Step 3: Response Formatting
```
- Standardizzare responses
- Gestire errori
- Implementare pagination
```

### Step 4: Documentation
```
- API documentation
- Swagger/OpenAPI
- Esempi di utilizzo
```

### Step 5: Testing
```
- Unit tests
- Integration tests
- API tests
- Performance tests
```

## Criteri di Accettazione

- API endpoints funzionanti
- Proper HTTP status codes
- Comprehensive error handling
- Performance acceptable
- Security implemented
- Documentation completa

## Stima Tempo

**Tempo stimato**: {{ estimated_time }}

---
*Generato automaticamente da Context Engineering Agent*
"""
    
    def _get_ui_template(self) -> str:
        return """# FEATURE: {{ feature_description }}

**Tipo**: UI Development
**Progetto**: {{ project_name }}
**Framework**: {{ framework }}
**Complessità**: {{ complexity }}
**Generato**: {{ generated_date }} {{ generated_time }}

## Descrizione

Sviluppare interfaccia utente per {{ feature_description }}.

## Componenti UI

{% for component in components %}
- {{ component.title() }} component
{% endfor %}
{% if not components %}
- Layout principale
- Navigation
- Content area
- Interactive elements
{% endif %}

## Design Requirements

### Responsive Design
- Mobile-first approach
- Breakpoints appropriati
- Touch-friendly interface

### Accessibility
- ARIA labels
- Keyboard navigation
- Screen reader support
- High contrast support

### Performance
- Lazy loading
- Optimized images
- Minimal JavaScript
- Fast loading times

## Implementazione

### Step 1: Component Structure
```
- Creare componenti base
- Definire props interface
- Implementare state management
```

### Step 2: Styling
```
- CSS/SCSS implementation
- Responsive design
- Theme support
- Animation/transitions
```

### Step 3: Interactivity
```
- Event handlers
- Form validation
- State updates
- API integration
```

### Step 4: Testing
```
- Unit tests
- Integration tests
- Visual regression tests
- Accessibility tests
```

## Criteri di Accettazione

- UI responsive su tutti i dispositivi
- Accessibility compliant
- Performance ottimale
- Cross-browser compatibility
- User experience eccellente

## Stima Tempo

**Tempo stimato**: {{ estimated_time }}

---
*Generato automaticamente da Context Engineering Agent*
"""
    
    def _get_auth_template(self) -> str:
        return """# FEATURE: {{ feature_description }}

**Tipo**: Authentication & Authorization
**Progetto**: {{ project_name }}
**Framework**: {{ framework }}
**Complessità**: {{ complexity }}
**Generato**: {{ generated_date }} {{ generated_time }}

## Descrizione

Implementare sistema di autenticazione e autorizzazione per {{ feature_description }}.

## Funzionalità Auth

- User registration
- User login/logout
- Password reset
- Session management
- Role-based access control
- Permission system

## Security Requirements

### Password Security
- Minimum password requirements
- Password hashing (bcrypt/argon2)
- Password reset flow
- Account lockout protection

### Session Management
- Secure session storage
- Session timeout
- CSRF protection
- XSS prevention

### Authorization
- Role-based permissions
- Resource-level access control
- API authentication
- Middleware protection

## Implementazione

### Step 1: Database Schema
```sql
-- Users table
-- Roles table
-- Permissions table
-- User_roles junction table
-- Sessions table
```

### Step 2: Authentication Logic
```
- User model
- Authentication service
- Session management
- Password utilities
```

### Step 3: Authorization System
```
- Role model
- Permission model
- Access control middleware
- Policy classes
```

### Step 4: UI Components
```
- Login form
- Registration form
- Password reset form
- User profile
- Admin panel
```

### Step 5: Security Features
```
- Rate limiting
- CSRF protection
- Input validation
- Security headers
```

## Criteri di Accettazione

- Secure authentication flow
- Proper session management
- Role-based access control
- Security best practices
- Comprehensive testing
- Audit logging

## Stima Tempo

**Tempo stimato**: {{ estimated_time }}

---
*Generato automaticamente da Context Engineering Agent*
"""
    
    def _get_integration_template(self) -> str:
        return """# FEATURE: {{ feature_description }}

**Tipo**: System Integration
**Progetto**: {{ project_name }}
**Framework**: {{ framework }}
**Complessità**: {{ complexity }}
**Generato**: {{ generated_date }} {{ generated_time }}

## Descrizione

Implementare integrazione con sistema esterno per {{ feature_description }}.

## Integrazioni Identificate

{% for integration in integrations %}
- {{ integration.title() }} integration
{% endfor %}
{% if not integrations %}
- API integration
- Data synchronization
- Event handling
{% endif %}

## Requisiti Integrazione

### API Communication
- HTTP client configuration
- Authentication setup
- Request/response handling
- Error handling
- Retry logic

### Data Synchronization
- Data mapping
- Transformation logic
- Conflict resolution
- Batch processing

### Event Handling
- Webhook endpoints
- Event processing
- Queue management
- Notification system

## Implementazione

### Step 1: API Client
```
- HTTP client setup
- Authentication implementation
- Request/response models
- Error handling
```

### Step 2: Data Processing
```
- Data transformation
- Validation logic
- Mapping functions
- Error recovery
```

### Step 3: Integration Service
```
- Service layer
- Business logic
- Data persistence
- Event handling
```

### Step 4: Monitoring
```
- Logging
- Metrics collection
- Health checks
- Alerting
```

## Criteri di Accettazione

- Successful data exchange
- Error handling robusto
- Performance acceptable
- Monitoring implementato
- Documentation completa

## Stima Tempo

**Tempo stimato**: {{ estimated_time }}

---
*Generato automaticamente da Context Engineering Agent*
"""
    
    def _get_optimization_template(self) -> str:
        return """# FEATURE: {{ feature_description }}

**Tipo**: Performance Optimization
**Progetto**: {{ project_name }}
**Framework**: {{ framework }}
**Complessità**: {{ complexity }}
**Generato**: {{ generated_date }} {{ generated_time }}

## Descrizione

Ottimizzare performance per {{ feature_description }}.

## Aree di Ottimizzazione

### Database
- Query optimization
- Index creation
- Connection pooling
- Caching strategies

### Backend
- Code optimization
- Memory management
- Algorithm improvements
- Resource usage

### Frontend
- Bundle optimization
- Lazy loading
- Image optimization
- Caching strategies

## Implementazione

### Step 1: Performance Analysis
```
- Profiling applicazione
- Identificare bottlenecks
- Misurare baseline metrics
- Definire target performance
```

### Step 2: Database Optimization
```
- Analizzare query slow
- Creare indici appropriati
- Ottimizzare schema
- Implementare caching
```

### Step 3: Backend Optimization
```
- Ottimizzare algoritmi
- Implementare caching
- Ridurre memory usage
- Ottimizzare I/O operations
```

### Step 4: Frontend Optimization
```
- Code splitting
- Lazy loading
- Image optimization
- Bundle analysis
```

### Step 5: Monitoring
```
- Performance metrics
- Real-time monitoring
- Alerting system
- Regular analysis
```

## Criteri di Accettazione

- Performance targets raggiunti
- Metrics di monitoring attivi
- Regressioni prevent
- Documentation aggiornata

## Stima Tempo

**Tempo stimato**: {{ estimated_time }}

---
*Generato automaticamente da Context Engineering Agent*
"""
    
    def _get_security_template(self) -> str:
        return """# FEATURE: {{ feature_description }}

**Tipo**: Security Implementation
**Progetto**: {{ project_name }}
**Framework**: {{ framework }}
**Complessità**: {{ complexity }}
**Generato**: {{ generated_date }} {{ generated_time }}

## Descrizione

Implementare misure di sicurezza per {{ feature_description }}.

## Security Measures

### Input Validation
- Sanitization
- Validation rules
- XSS prevention
- SQL injection prevention

### Authentication & Authorization
- Secure login
- Session management
- Access control
- Role-based permissions

### Data Protection
- Encryption at rest
- Encryption in transit
- Sensitive data handling
- GDPR compliance

### Network Security
- HTTPS enforcement
- Security headers
- Rate limiting
- DDoS protection

## Implementazione

### Step 1: Security Audit
```
- Vulnerability assessment
- Code security review
- Dependencies check
- Configuration review
```

### Step 2: Input Security
```
- Validation implementation
- Sanitization functions
- Error handling
- Logging security events
```

### Step 3: Authentication Security
```
- Secure authentication
- Session security
- Password policies
- Multi-factor authentication
```

### Step 4: Data Security
```
- Encryption implementation
- Secure storage
- Access logging
- Data anonymization
```

### Step 5: Monitoring
```
- Security monitoring
- Intrusion detection
- Audit logging
- Incident response
```

## Criteri di Accettazione

- Security vulnerabilities addressed
- Compliance requirements met
- Security testing passed
- Monitoring implemented
- Documentation completa

## Stima Tempo

**Tempo stimato**: {{ estimated_time }}

---
*Generato automaticamente da Context Engineering Agent*
"""
    
    def _get_testing_template(self) -> str:
        return """# FEATURE: {{ feature_description }}

**Tipo**: Testing Implementation
**Progetto**: {{ project_name }}
**Framework**: {{ framework }}
**Complessità**: {{ complexity }}
**Generato**: {{ generated_date }} {{ generated_time }}

## Descrizione

Implementare test suite per {{ feature_description }}.

## Test Strategy

### Unit Tests
- Function/method testing
- Component testing
- Mock implementations
- Edge case testing

### Integration Tests
- API endpoint testing
- Database integration
- Service integration
- Component interaction

### End-to-End Tests
- User workflow testing
- Cross-browser testing
- Mobile testing
- Performance testing

## Implementazione

### Step 1: Test Setup
```
- Test framework setup
- Test environment configuration
- Mock setup
- Test data preparation
```

### Step 2: Unit Tests
```
- Function tests
- Component tests
- Service tests
- Utility tests
```

### Step 3: Integration Tests
```
- API tests
- Database tests
- Service integration
- Component integration
```

### Step 4: E2E Tests
```
- User journey tests
- Cross-browser tests
- Mobile tests
- Performance tests
```

### Step 5: Test Automation
```
- CI/CD integration
- Automated test runs
- Test reporting
- Coverage analysis
```

## Criteri di Accettazione

- Test coverage > 80%
- All tests passing
- CI/CD integration
- Test documentation
- Performance benchmarks

## Stima Tempo

**Tempo stimato**: {{ estimated_time }}

---
*Generato automaticamente da Context Engineering Agent*
"""
    
    def _get_documentation_template(self) -> str:
        return """# FEATURE: {{ feature_description }}

**Tipo**: Documentation
**Progetto**: {{ project_name }}
**Framework**: {{ framework }}
**Complessità**: {{ complexity }}
**Generato**: {{ generated_date }} {{ generated_time }}

## Descrizione

Creare documentazione per {{ feature_description }}.

## Documentation Types

### Technical Documentation
- API documentation
- Code documentation
- Architecture documentation
- Database schema

### User Documentation
- User guides
- Tutorials
- FAQ
- Help system

### Development Documentation
- Setup guides
- Contributing guidelines
- Coding standards
- Deployment procedures

## Implementazione

### Step 1: Documentation Planning
```
- Define documentation structure
- Identify target audiences
- Choose documentation tools
- Create content outline
```

### Step 2: Technical Docs
```
- API documentation
- Code comments
- Architecture diagrams
- Database documentation
```

### Step 3: User Docs
```
- User guides
- Step-by-step tutorials
- Screenshots/videos
- FAQ section
```

### Step 4: Development Docs
```
- Setup instructions
- Development workflow
- Contributing guide
- Deployment guide
```

### Step 5: Maintenance
```
- Documentation updates
- Version control
- Review process
- Quality assurance
```

## Criteri di Accettazione

- Documentation complete
- Easy to understand
- Up-to-date information
- Searchable content
- Multiple formats available

## Stima Tempo

**Tempo stimato**: {{ estimated_time }}

---
*Generato automaticamente da Context Engineering Agent*
"""
    
    def _get_generic_template(self) -> str:
        return """# FEATURE: {{ feature_description }}

**Tipo**: Generic Feature
**Progetto**: {{ project_name }}
**Framework**: {{ framework }}
**Complessità**: {{ complexity }}
**Generato**: {{ generated_date }} {{ generated_time }}

## Descrizione

Implementare {{ feature_description }}.

## Analisi Requisiti

### Entità Identificate
{% for entity in entities %}
- {{ entity.title() }}
{% endfor %}
{% if not entities %}
- Da definire durante l'analisi
{% endif %}

### Azioni Richieste
{% for action in actions %}
- {{ action.title() }}
{% endfor %}
{% if not actions %}
- Da definire durante l'analisi
{% endif %}

### Componenti UI
{% for component in components %}
- {{ component.title() }}
{% endfor %}
{% if not components %}
- Da definire durante l'analisi
{% endif %}

## Implementazione

### Step 1: Analisi Dettagliata
```
- Definire requisiti specifici
- Identificare use cases
- Progettare architettura
- Pianificare implementazione
```

### Step 2: Backend Development
```
- Implementare business logic
- Creare API endpoints
- Gestire database operations
- Implementare validazione
```

### Step 3: Frontend Development
```
- Creare componenti UI
- Implementare user interactions
- Gestire state management
- Integrare con backend
```

### Step 4: Testing
```
- Unit tests
- Integration tests
- User acceptance tests
- Performance tests
```

### Step 5: Documentation
```
- Technical documentation
- User documentation
- API documentation
- Deployment guides
```

## Criteri di Accettazione

{% for requirement in requirements %}
- {{ requirement }}
{% endfor %}
{% if not requirements %}
- Funzionalità implementata correttamente
- Test passano
- Performance accettabile
- Documentazione completa
{% endif %}

## Stima Tempo

**Tempo stimato**: {{ estimated_time }}

---
*Generato automaticamente da Context Engineering Agent*
"""