# API de Templates - Architecture DDD

Cette application permet de créer et gérer des templates avec leurs sections associées, en suivant les principes du Domain-Driven Design (DDD) avec une approche fonctionnelle.

## Architecture

L'application suit une architecture hexagonale avec les couches suivantes :

- **Domain** : Entités, agrégats, repositories et services de domaine
- **Application** : Services applicatifs (fonctions) et DTOs
- **Infrastructure** : Implémentations des repositories et unit of work
- **API** : Contrôleurs FastAPI

### Approche Fonctionnelle

La couche application utilise des **fonctions pures** plutôt que des classes, ce qui offre :
- Plus de simplicité et de lisibilité
- Meilleure testabilité
- Moins de couplage
- Facilité de composition

## Fonctionnalités

### Templates

- **POST** `/templates/create` - Créer un nouveau template
- **POST** `/templates/{template_id}/publish` - Publier un template
- **POST** `/templates/{template_id}/sections` - Ajouter une section à un template

## Modèles de Données

### Template

```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "status": "draft|published",
  "sections": []
}
```

### Section

```json
{
  "id": "uuid",
  "title": "string",
  "description": "string"
}
```

## Structure des Services

### Services Template (`app/application/services/template_service.py`)

```python
# Fonctions principales
async def create_template(uow: AbstractUnitOfWork, title: str, description: str | None = None) -> TemplateAggregate
async def publish_template(uow: AbstractUnitOfWork, template_id: UUID) -> TemplateAggregate
async def add_section(uow: AbstractUnitOfWork, template_id: UUID, data: CreateSectionDTO) -> TemplateAggregate
```

## Installation et Lancement

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

2. Lancer l'application :
```bash
uvicorn app.api.main:app --reload
```

3. Accéder à la documentation interactive :
```
http://localhost:8000/docs
```

## Exemples d'Utilisation

### Créer un template
```bash
curl -X POST "http://localhost:8000/templates/create" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Template de Satisfaction",
    "description": "Questionnaire de satisfaction client"
  }'
```

### Publier un template
```bash
curl -X POST "http://localhost:8000/templates/{template_id}/publish"
```

### Ajouter une section à un template
```bash
curl -X POST "http://localhost:8000/templates/{template_id}/sections" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Section 1",
    "description": "Description de la section"
  }'
```

## Structure du Projet

```
backend/
├── app/
│   ├── api/                    # Contrôleurs FastAPI
│   │   ├── main.py            # Configuration FastAPI
│   │   ├── template.py        # Routes des templates
│   │   └── helpers.py         # Utilitaires API
│   ├── application/           # Couche application
│   │   ├── dtos/             # Data Transfer Objects
│   │   └── services/         # Services applicatifs (fonctions)
│   ├── domain/               # Couche domaine
│   │   ├── aggregates/       # Agrégats
│   │   ├── entities/         # Entités
│   │   ├── repositories/     # Interfaces des repositories
│   │   └── value_objects/    # Objets de valeur
│   └── infrastructure/       # Couche infrastructure
│       ├── dependencies.py   # Injection de dépendances
│       └── persistence/      # Implémentations des repositories
├── requirements.txt
└── README.md
```

## Avantages de l'Approche Fonctionnelle

1. **Simplicité** : Les fonctions sont plus simples à comprendre que les classes
2. **Testabilité** : Plus facile de tester des fonctions pures
3. **Composition** : Les fonctions peuvent être facilement composées
4. **Immutabilité** : Moins d'état mutable à gérer
5. **Dépendances explicites** : L'UnitOfWork est passé explicitement en paramètre

## Technologies Utilisées

- **FastAPI** : Framework web moderne et rapide
- **Pydantic** : Validation de données
- **SQLAlchemy** : ORM pour la persistance
- **Alembic** : Migrations de base de données
- **Pytest** : Tests unitaires et d'intégration
- **Uvicorn** : Serveur ASGI

## Tests

Pour exécuter les tests :

```bash
pytest
```

Pour les tests avec couverture :

```bash
pytest --cov=app
``` 