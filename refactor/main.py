#!/usr/bin/env python3
"""
Quiz Python - Application interactive de quiz en CLI

Ce module gère l'exécution du questionnaire :
- Orchestration du déroulement du quiz
- Gestion de l'ordre des questions
- Validation des réponses
"""

import argparse
from typing import Dict, List
import random
import quiz_data
import resultats_data
import ui


def is_answer_correct(choices: List[Dict], reponse: int | None) -> bool:
    """
    Vérifie si la réponse donnée est correcte.

    Args:
        choices: Liste des choix avec leur statut correct/incorrect
                 Format: [{"choix": "...", "correct": True/False}, ...]
        reponse: Index de la réponse choisie (None si pas de réponse)

    Returns:
        True si la réponse est correcte, False sinon

    """
    # Handle no answer
    if reponse is None:
        return False

    # Handle out of bounds (defensive)
    if reponse < 0 or reponse >= len(choices):
        return False

    return choices[reponse]["correct"]


def run_questionnaire(quiz: Dict, resultats: Dict) -> Dict:
    """Exécute le questionnaire interactif."""
    # Sélectionner les questions non répondues
    questions_selectionnees = resultats_data.questions_a_poser(resultats)
    total_questions = len(questions_selectionnees)

    for index, question_id in enumerate(questions_selectionnees, 1):
        question_pose = quiz_data.read_question(question_id, quiz)

        # Mélanger les options
        choix_propose = random.sample(
            question_pose["liste_choix"], len(question_pose["liste_choix"])
        )

        reponse = ui.form_question(
            question_pose["question"], choix_propose, index, total_questions
        )

        # Si l'utilisateur a appuyé sur Entrée sans réponse, passer à la question suivante
        if is_answer_correct(choix_propose, reponse):
            resultats = resultats_data.valider_resultat(question_id, resultats)

    return resultats


def main() -> None:
    """Point d'entrée principal de l'application."""
    parser = argparse.ArgumentParser(
        description="Quiz Python - Application interactive de quiz"
    )
    parser.add_argument(
        "-q",
        "--quiz",
        default="quiz",
        help="Nom du fichier de quiz sans extension (défaut: quiz)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="resultat",
        help="Nom du fichier de résultats sans extension (défaut: resultat)",
    )
    parser.add_argument(
        "-r",
        "--resume",
        action="store_true",
        help="Reprendre un quiz sur les questions incorrectes du fichier de résultats",
    )

    args = parser.parse_args()

    # charger le quiz depuis le fichier source
    quiz = quiz_data.load(args.quiz)

    resultats = None
    try:
        if args.resume:
            # Mode reprise: charger le fichier de résultats existant
            resultats = resultats_data.load(args.output)

            ui.view_reprise(
                quiz["quiz_title"],
                resultats["prenom"],
                resultats["nom"],
                resultats["correct_count"],
                quiz["nombre_questions"],
            )

        else:
            prenom, nom = ui.form_demarrage(quiz["quiz_title"])

            # Construire la structure
            resultats = resultats_data.create(
                quiz["quiz_name"], quiz_data.liste_questions(quiz), prenom, nom
            )
            resultats_data.save(resultats, args.output)

        # Lancer le questionnaire
        resultats = run_questionnaire(quiz, resultats)

    except KeyboardInterrupt:
        print("\n\n⚠️  Quiz interrompu par l'utilisateur.")

    finally:
        # Sauvegarder les résultats
        if resultats:
            resultats_data.save(resultats, args.output)
            ui.view_resultats(
                quiz["quiz_title"], resultats["correct_count"], quiz["nombre_questions"]
            )


if __name__ == "__main__":
    main()
