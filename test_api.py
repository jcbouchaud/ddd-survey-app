#!/usr/bin/env python3
"""
Script de test pour l'API de questionnaires templates
"""

import json

import requests

BASE_URL = "http://localhost:8000"


def test_create_question():
    """Test de création d'une question"""
    print("=== Test de création d'une question ===")

    question_data = {
        "title": "Quelle est votre satisfaction globale ?",
        "description": "Évaluez votre niveau de satisfaction global avec notre service",
        "weighting": [1, 2, 3],
    }

    response = requests.post(f"{BASE_URL}/questions/", json=question_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        return response.json()["id"]
    return None


def test_create_template():
    """Test de création d'un template"""
    print("\n=== Test de création d'un template ===")

    template_data = {
        "name": "Questionnaire de Satisfaction",
        "description": "Template pour évaluer la satisfaction client",
    }

    response = requests.post(f"{BASE_URL}/templates/", json=template_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    if response.status_code == 200:
        return response.json()["id"]
    return None


def test_get_all_questions():
    """Test de récupération de toutes les questions"""
    print("\n=== Test de récupération de toutes les questions ===")

    response = requests.get(f"{BASE_URL}/questions/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    return response.json() if response.status_code == 200 else []


def test_get_all_templates():
    """Test de récupération de tous les templates"""
    print("\n=== Test de récupération de tous les templates ===")

    response = requests.get(f"{BASE_URL}/templates/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    return response.json() if response.status_code == 200 else []


def test_associate_questions_to_template(template_id, question_ids):
    """Test d'association de questions à un template"""
    print(f"\n=== Test d'association de questions au template {template_id} ===")

    response = requests.post(
        f"{BASE_URL}/templates/{template_id}/questions", json=question_ids
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def main():
    """Fonction principale de test"""
    print("🚀 Démarrage des tests de l'API de questionnaires templates")
    print("=" * 60)

    # Créer plusieurs questions
    question_ids = []
    for i in range(3):
        question_data = {
            "title": f"Question {i+1}",
            "description": f"Description de la question {i+1}",
            "weighting": [1, 2, 3],
        }
        response = requests.post(f"{BASE_URL}/questions/", json=question_data)
        if response.status_code == 200:
            question_ids.append(response.json()["id"])

    # Créer un template
    template_response = requests.post(
        f"{BASE_URL}/templates/",
        json={"name": "Template de Test", "description": "Template pour les tests"},
    )

    if template_response.status_code == 200:
        template_id = template_response.json()["id"]

        # Associer les questions au template
        test_associate_questions_to_template(template_id, question_ids)

    # Afficher toutes les questions
    test_get_all_questions()

    # Afficher tous les templates
    test_get_all_templates()

    print("\n✅ Tests terminés !")
    print(f"📖 Documentation interactive disponible sur: {BASE_URL}/docs")


if __name__ == "__main__":
    main()
