# API de Questionnaires Templates - Architecture DDD

Cette application permet de créer et gérer des questionnaires templates et leurs questions associées, en suivant les principes du Domain-Driven Design (DDD) avec une approche fonctionnelle.

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

### Templates de Questionnaires

- **POST** `/templates/` - Créer un nouveau template
- **GET** `/templates/` - Récupérer tous les templates
- **GET** `/templates/{template_id}` - Récupérer un template spécifique
- **POST** `/templates/{template_id}/questions` - Associer des questions à un template

### Questions

- **POST** `/questions/` - Créer une nouvelle question
- **GET** `/questions/` - Récupérer toutes les questions
- **GET** `/questions/{question_id}` - Récupérer une question spécifique
- **PUT** `/questions/{question_id}` - Mettre à jour une question

## Modèles de Données

### Template

```json
{
  "id": "uuid",
  "name": "string",
  "description": "string",
  "questions_ids": ["uuid"]
}
```

### Question

```json
{
  "id": "uuid",
  "title": "string",
  "description": "string",
  "weighting": [1, 2, 3]
}
```

## Structure des Services

### Services Template (`app/application/services/template_functions.py`)

```python
# Fonctions principales
async def create_template(dto: CreateTemplateDTO, uow: UnitOfWork) -> TemplateResponseDTO
async def get_template_by_id(template_id: UUID, uow: UnitOfWork) -> Optional[TemplateResponseDTO]
async def get_all_templates(uow: UnitOfWork) -> List[TemplateResponseDTO]
async def update_template(template_id: UUID, dto: UpdateTemplateDTO, uow: UnitOfWork) -> Optional[TemplateResponseDTO]
async def add_questions_to_template(template_id: UUID, question_ids: List[UUID], uow: UnitOfWork) -> TemplateResponseDTO
```

### Services Question (`app/application/services/question_functions.py`)

```python
# Fonctions principales
async def create_question(dto: CreateQuestionDTO, uow: UnitOfWork) -> QuestionResponseDTO
async def get_question_by_id(question_id: UUID, uow: UnitOfWork) -> Optional[QuestionResponseDTO]
async def get_all_questions(uow: UnitOfWork) -> List[QuestionResponseDTO]
async def update_question(question_id: UUID, dto: UpdateQuestionDTO, uow: UnitOfWork) -> Optional[QuestionResponseDTO]
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

### Créer une question
```bash
curl -X POST "http://localhost:8000/questions/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Quelle est votre satisfaction ?",
    "description": "Évaluez votre niveau de satisfaction",
    "weighting": [1, 2, 3]
  }'
```

### Créer un template
```bash
curl -X POST "http://localhost:8000/templates/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Satisfaction Client",
    "description": "Questionnaire de satisfaction client"
  }'
```

### Associer des questions à un template
```bash
curl -X POST "http://localhost:8000/templates/{template_id}/questions" \
  -H "Content-Type: application/json" \
  -d '["question_id_1", "question_id_2"]'
```

## Avantages de l'Approche Fonctionnelle

1. **Simplicité** : Les fonctions sont plus simples à comprendre que les classes
2. **Testabilité** : Plus facile de tester des fonctions pures
3. **Composition** : Les fonctions peuvent être facilement composées
4. **Immutabilité** : Moins d'état mutable à gérer
5. **Dépendances explicites** : L'UnitOfWork est passé explicitement en paramètre 