#!/bin/bash

BASE_URL="http://localhost:8000"

echo "🚀 Démarrage des tests de l'API de questionnaires templates"
echo "============================================================"

# Créer plusieurs questions
echo -e "\n📝 Création de questions..."
question_ids=()

for i in {1..3}; do
    echo "Création de la question $i..."
    response=$(curl -s -X POST "$BASE_URL/questions/" \
        -H "Content-Type: application/json" \
        -d "{
            \"title\": \"Question $i\",
            \"description\": \"Description de la question $i\",
            \"weighting\": [1, 2, 3]
        }")
    
    question_id=$(echo $response | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
    question_ids+=($question_id)
    echo "Question $i créée avec l'ID: $question_id"
done

# Créer un template
echo -e "\n📋 Création d'un template..."
template_response=$(curl -s -X POST "$BASE_URL/templates/" \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Template de Test",
        "description": "Template pour les tests"
    }')

template_id=$(echo $template_response | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
echo "Template créé avec l'ID: $template_id"

# Associer les questions au template
echo -e "\n🔗 Association des questions au template..."
question_ids_json=$(printf '["%s"]' "$(IFS='","'; echo "${question_ids[*]}")")
curl -s -X POST "$BASE_URL/templates/$template_id/questions" \
    -H "Content-Type: application/json" \
    -d "$question_ids_json" | jq '.'

# Afficher toutes les questions
echo -e "\n📋 Liste de toutes les questions..."
curl -s -X GET "$BASE_URL/questions/" | jq '.'

# Afficher tous les templates
echo -e "\n📋 Liste de tous les templates..."
curl -s -X GET "$BASE_URL/templates/" | jq '.'

echo -e "\n✅ Tests terminés !"
echo "📖 Documentation interactive disponible sur: $BASE_URL/docs" 