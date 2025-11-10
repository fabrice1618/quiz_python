"""
Module affichage pour l'interface utilisateur du quiz.

Ce module gère toutes les interactions avec l'utilisateur :
- Affichage des écrans et formulaires
- Collecte des réponses
- Affichage des résultats
"""

import os
from typing import Tuple, Dict


def clear_screen() -> None:
    """Efface l'écran du terminal (compatible Windows et Unix)."""
    os.system("clear" if os.name != "nt" else "cls")


def print_titre(titre: str) -> None:
    """Affiche le titre du quiz"""
    print(f"\n{'=' * 70}")
    print(titre)
    print(f"{'=' * 70}")


def view_resultats(quiz_title: str, correct_count: int, total_count: int) -> None:
    """Affiche les résultats finaux du quiz."""
    clear_screen()
    print_titre(f"  Résultats {quiz_title}")
    print(f"Score: {correct_count}/{total_count}")


def form_demarrage(quiz_title: str) -> Tuple:
    """Affiche l'écran de démarrage et collecte le nom et prénom de l'utilisateur."""
    # Demander nom et prénom
    print_titre(f"  Bienvenue au {quiz_title}")
    nom = input("Entrez votre nom : ").strip()
    prenom = input("Entrez votre prénom : ").strip()

    _ = input("\nAppuyez sur Entrée pour commencer...")

    return (prenom, nom)


def view_reprise(
    quiz_title: str, prenom: str, nom: str, correct_count: int, total_count: int
) -> None:
    """Affiche l'écran de reprise du quiz avec le score actuel."""
    print_titre(f"  Reprise du Quiz {quiz_title}")
    print(f"Utilisateur: {prenom} {nom}")
    print(f"\nScore actuel : {correct_count} / {total_count}")
    _ = input("\nAppuyez sur Entrée pour reprendre...")


def print_question(
    question: str, choix_propose: list[Dict], index: int, total_questions: int
) -> None:
    """Affiche une question avec ses choix"""
    # Effacer l'écran avant la question
    clear_screen()
    print(f"{index} / {total_questions} - {question}\n")
    for numero, choix in enumerate(choix_propose, 1):
        # Gérer le formatage multiligne pour le code
        choix_text = choix["choix"]
        lines = choix_text.split("\n")
        if len(lines) > 1:
            # Afficher la première ligne avec le numéro
            print(f"\t{numero} : {lines[0]}")
            # Afficher les lignes suivantes avec indentation
            for line in lines[1:]:
                print(f"\t    {line}")
        else:
            print(f"\t{numero} : {choix_text}")


def form_question(
    question: str, choix_propose: list[Dict], index: int, total_questions: int
) -> int | None:
    """Affiche une question avec ses choix et collecte la réponse de l'utilisateur."""

    print_question(question, choix_propose, index, total_questions)

    while True:
        try:
            user_input = input(
                "\nRenseignez votre choix (Entrée pour passer) : "
            ).strip()

            # Si l'utilisateur appuie sur Entrée sans rien saisir, passer la question
            if not user_input:
                return None

            value = int(user_input)
            if 1 <= value <= len(choix_propose):
                return value - 1

            print(f"⚠️  Le nombre doit être entre 1 et {len(choix_propose)}")
        except ValueError:
            print(
                f"⚠️  Veuillez entrer un nombre valide entre 1 et {len(choix_propose)}"
            )
