"""
Modèle resultats
"""

import json
from typing import Dict, List
import random
import config


class QuizResultatError(Exception):
    """Erreur liée au fichier de quiz (format, lecture, validation)."""


def load(resultat_file: str) -> Dict:
    """Charge un quiz depuis un fichier JSON."""

    resultat_path = config.data_path / config.RESULT_PATH / (resultat_file + ".json")

    try:
        with open(resultat_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as exc:
        raise QuizResultatError(
            f"Erreur: {resultat_path} Le fichier n'existe pas."
        ) from exc
    except json.JSONDecodeError as exc:
        raise QuizResultatError(
            f"Erreur: {resultat_path} format de fichier incorrect."
        ) from exc


def save(resultats: Dict, resultat_file: str) -> None:
    """Enregistre les résultats du quiz dans un fichier JSON."""

    resultat_path = config.data_path / config.RESULT_PATH / (resultat_file + ".json")

    with open(resultat_path, "w", encoding="utf-8") as fichier:
        json.dump(resultats, fichier, indent=2, ensure_ascii=False)


def create(quiz_name: str, liste_questions: List[int], prenom: str, nom: str) -> Dict:
    """Construit la structure du quiz à partir des données chargées."""
    resultats = {
        "quiz_name": quiz_name,
        "nom": nom,
        "prenom": prenom,
        "correct_count": 0,
        "questions": [],
    }

    resultats["questions"] = [
        {"question_id": question_id, "correct": False}
        for question_id in liste_questions
    ]

    return resultats


def valider_resultat(question_id: int, resultats: Dict) -> Dict:
    """
    Retourne un nouveau dict de résultats avec la question marquée comme correcte.
    Pure function: Ne modifie pas l'input, retourne une nouvelle structure.

    Args:
        question_id: ID de la question à marquer comme correcte
        resultats: Dict des résultats actuels (non modifié)

    Returns:
        Nouveau dict avec la question mise à jour
    """
    # Create new questions list with updated question
    new_questions = [
        {**q, "correct": True} if q["question_id"] == question_id else dict(q)
        for q in resultats["questions"]
    ]

    # Recalculate correct count from the new data (single source of truth)
    correct_count = sum(1 for q in new_questions if q["correct"])

    # Return new dict with updated values (shallow copy for top level)
    return {**resultats, "questions": new_questions, "correct_count": correct_count}


def questions_a_poser(resultats: Dict) -> List:
    """Retourne une liste aléatoire des questions non encore répondues correctement."""
    questions_non_repondues = [
        q["question_id"] for q in resultats["questions"] if not q["correct"]
    ]

    if not questions_non_repondues:
        return []

    questions_selectionnees = random.sample(
        questions_non_repondues, len(questions_non_repondues)
    )
    return questions_selectionnees
