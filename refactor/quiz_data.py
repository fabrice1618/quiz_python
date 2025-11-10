"""
Modèle quiz
"""

import json
from typing import Dict, List
import config


class QuizFileError(Exception):
    """Erreur liée au fichier de quiz (format, lecture, validation)."""


def load(quiz_name: str) -> Dict:
    """
    Charge un quiz depuis un fichier JSON et le transforme au format interne.

    Args:
        quiz_name: Nom du fichier quiz (sans extension .json)

    Returns:
        Quiz au format interne avec questions transformées

    Raises:
        QuizFileError: Si le fichier est introuvable, invalide ou malformé
    """

    quiz_path = config.data_path / config.QUIZ_PATH / (quiz_name + ".json")

    try:
        with open(quiz_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not "quiz_title" in data or not isinstance(data["quiz_title"], str):
                raise QuizFileError(f"Erreur: {quiz_path} format incorrect.")

            if not "questions" in data or not isinstance(data["questions"], list):
                raise QuizFileError(f"Erreur: {quiz_path} format incorrect.")

            # Validation des questions individuelles
            questions = []
            for i, question in enumerate(data["questions"], 1):
                if "id" not in question or not isinstance(question["id"], int):
                    raise QuizFileError(
                        f"Erreur: question {i} - 'id' doit être un int."
                    )
                if "question" not in question or not isinstance(
                    question["question"], str
                ):
                    raise QuizFileError(
                        f"Erreur: question {i} - 'question' doit être un str."
                    )
                if "choices" not in question or not isinstance(
                    question["choices"], list
                ):
                    raise QuizFileError(
                        f"Erreur: question {i} - 'choices' doit être une liste."
                    )
                if "answer_index" not in question or not isinstance(
                    question["answer_index"], int
                ):
                    raise QuizFileError(
                        f"Erreur: question {i} - 'answer_index' doit être un entier."
                    )
                if not 0 <= question["answer_index"] < len(question["choices"]):
                    raise QuizFileError(
                        f"Erreur: question {i} - 'answer_index' hors limites."
                    )

                liste_choix = [
                    {"choix": choix, "correct": (index == question["answer_index"])}
                    for index, choix in enumerate(question["choices"])
                ]

                questions.append(
                    {
                        "question_id": question["id"],
                        "question": question["question"],
                        "liste_choix": liste_choix,
                    }
                )

            quiz = {
                "quiz_title": data["quiz_title"],
                "nombre_questions": len(data["questions"]),
                "quiz_name": quiz_name,
                "questions": questions,
            }

            return quiz

    except FileNotFoundError as exc:
        raise QuizFileError(f"Erreur: {quiz_path} Le fichier n'existe pas.") from exc
    except json.JSONDecodeError as exc:
        raise QuizFileError(
            f"Erreur: {quiz_path} format de fichier incorrect."
        ) from exc


def read_question(question_id: int, quiz: Dict) -> Dict:
    """
    Retourne une question spécifique par son ID.

    Args:
        quiz: Quiz au format interne
        question_id: ID de la question recherchée

    Returns:
        Question au format interne

    Raises:
        QuizFileError: Si la question n'est pas trouvée
    """

    for question in quiz["questions"]:
        if question["question_id"] == question_id:
            return question

    raise QuizFileError(f"Question ID {question_id} introuvable dans le quiz.")


def liste_questions(quiz) -> List[int]:
    """
    Retourne la liste des IDs de toutes les questions du quiz.

    Args:
        quiz: Quiz au format interne

    Returns:
        Liste des IDs de questions
    """
    return [q["question_id"] for q in quiz["questions"]]
