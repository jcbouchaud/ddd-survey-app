#!/usr/bin/env python3
"""
Script de test pour l'API de questionnaires templates - Architecture Fonctionnelle
"""

import requests

BASE_URL = "http://localhost:8000"


def test_functional_architecture():
    """Test de l'architecture fonctionnelle"""
    print("🚀 Test de l'architecture fonctionnelle")
    print("=" * 50)
    
    # Test 1: Créer des questions
    print("\n📝 Test 1: Création de questions")
    question_ids = []
    
    questions_data = [
        {
            "title": "Satisfaction globale",
            "description": "Évaluez votre satisfaction globale",
            "weighting": [1, 2, 3]
        },
        {
            "title": "Qualité du service",
            "description": "Évaluez la qualité du service reçu",
            "weighting": [1, 2, 3]
        },
        {
            "title": "Recommandation",
            "description": "Recommanderiez-vous notre service ?",
            "weighting": [1, 2, 3]
        }
    ]
    
    for i, question_data in enumerate(questions_data, 1):
        response = requests.post(f"{BASE_URL}/questions/", json=question_data)
        if response.status_code == 200:
            question_id = response.json()["id"]
            question_ids.append(question_id)
            print(f"  ✅ Question {i} créée: {question_id}")
        else:
            print(f"  ❌ Erreur création question {i}: {response.status_code}")
    
    # Test 2: Créer un template
    print("\n📋 Test 2: Création d'un template")
    template_data = {
        "name": "Questionnaire Satisfaction Client",
        "description": "Template pour évaluer la satisfaction client"
    }
    
    template_response = requests.post(f"{BASE_URL}/templates/", json=template_data)
    if template_response.status_code == 200:
        template_id = template_response.json()["id"]
        print(f"  ✅ Template créé: {template_id}")
    else:
        print(f"  ❌ Erreur création template: {template_response.status_code}")
        return
    
    # Test 3: Associer les questions au template
    print("\n🔗 Test 3: Association des questions au template")
    association_response = requests.post(
        f"{BASE_URL}/templates/{template_id}/questions",
        json=question_ids
    )
    
    if association_response.status_code == 200:
        updated_template = association_response.json()
        question_count = len(updated_template['questions_ids'])
        print(f"  ✅ Questions associées: {question_count} questions")
        print(f"  📊 Template final: {updated_template['name']}")
    else:
        print(f"  ❌ Erreur association: {association_response.status_code}")
    
    # Test 4: Récupérer toutes les questions
    print("\n📋 Test 4: Récupération de toutes les questions")
    questions_response = requests.get(f"{BASE_URL}/questions/")
    if questions_response.status_code == 200:
        questions = questions_response.json()
        print(f"  ✅ {len(questions)} questions récupérées")
        for q in questions:
            print(f"    - {q['title']}")
    else:
        print(f"  ❌ Erreur récupération questions: {questions_response.status_code}")
    
    # Test 5: Récupérer tous les templates
    print("\n📋 Test 5: Récupération de tous les templates")
    templates_response = requests.get(f"{BASE_URL}/templates/")
    if templates_response.status_code == 200:
        templates = templates_response.json()
        print(f"  ✅ {len(templates)} templates récupérés")
        for t in templates:
            print(f"    - {t['name']} ({len(t['questions_ids'])} questions)")
    else:
        print(f"  ❌ Erreur récupération templates: {templates_response.status_code}")
    
    # Test 6: Mettre à jour une question
    print("\n✏️ Test 6: Mise à jour d'une question")
    if question_ids:
        update_data = {
            "title": "Satisfaction globale (mise à jour)",
            "description": "Description mise à jour"
        }
        update_response = requests.put(
            f"{BASE_URL}/questions/{question_ids[0]}",
            json=update_data
        )
        if update_response.status_code == 200:
            updated_question = update_response.json()
            print(f"  ✅ Question mise à jour: {updated_question['title']}")
        else:
            print(f"  ❌ Erreur mise à jour: {update_response.status_code}")


def main():
    """Fonction principale"""
    print("🎯 Test de l'API avec architecture fonctionnelle")
    print("=" * 60)
    
    try:
        test_functional_architecture()
        print("\n✅ Tous les tests terminés avec succès !")
        print(f"📖 Documentation interactive: {BASE_URL}/docs")
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        print("Assurez-vous que l'API est démarrée sur http://localhost:8000")


if __name__ == "__main__":
    main()
