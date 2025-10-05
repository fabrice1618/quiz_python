#!/usr/bin/env python3
"""
Quiz Python - Application interactive de quiz
"""

import json
import random
import argparse
import os
from typing import Dict, List


def load_quiz(filename: str) -> Dict:
    """Charge un quiz depuis un fichier JSON."""
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def build_quiz_structure(data: Dict) -> Dict:
    """Construit la structure du quiz à partir des données chargées."""
    quiz = {
        'quiz_title': data['quiz_title'],
        'nom': '',
        'prenom': '',
        'questions': []
    }

    for question in data['questions']:
        question_quiz = {
            'question_id': question['id'],
            'question': question['question'],
            'correct': False,
            'liste_choix': []
        }

        for numero, choice in enumerate(question['choices']):
            choix = {
                'choix': choice,
                'correct': (numero == question['answer_index'])
            }
            question_quiz['liste_choix'].append(choix)

        quiz['questions'].append(question_quiz)

    return quiz


def get_valid_input(prompt: str, min_val: int, max_val: int) -> int | None:
    """Obtient une entrée valide de l'utilisateur entre min_val et max_val.

    Retourne None si l'utilisateur appuie sur Entrée sans saisir de valeur (pour passer la question).
    """
    while True:
        try:
            user_input = input(prompt).strip()

            # Si l'utilisateur appuie sur Entrée sans rien saisir, passer la question
            if not user_input:
                return None

            value = int(user_input)
            if min_val <= value <= max_val:
                return value
            else:
                print(f"⚠️  Le nombre doit être entre {min_val} et {max_val}")
        except ValueError:
            print(f"⚠️  Veuillez entrer un nombre valide entre {min_val} et {max_val}")


def run_questionnaire(quiz: Dict) -> None:
    """Exécute le questionnaire interactif."""
    # Sélectionner les questions non répondues
    questions_a_poser = [q for q in quiz["questions"] if not q["correct"]]

    if not questions_a_poser:
        print("✅ Toutes les questions ont déjà été répondues correctement!")
        return

    questions_selectionnees = random.sample(questions_a_poser, len(questions_a_poser))
    total_questions = len(questions_selectionnees)

    for index, question_pose in enumerate(questions_selectionnees, 1):
        print(f'{index} / {total_questions} - {question_pose["question"]}\n')

        choix_propose = random.sample(question_pose["liste_choix"], len(question_pose["liste_choix"]))

        for numero, choix in enumerate(choix_propose):
            # Gérer le formatage multiligne pour le code
            choix_text = choix["choix"]
            lines = choix_text.split('\n')
            if len(lines) > 1:
                # Afficher la première ligne avec le numéro
                print(f'\t{numero + 1} : {lines[0]}')
                # Afficher les lignes suivantes avec indentation
                for line in lines[1:]:
                    print(f'\t    {line}')
            else:
                print(f'\t{numero + 1} : {choix_text}')

        reponse = get_valid_input("\nRenseignez votre choix (Entrée pour passer) : ", 1, len(choix_propose))

        # Si l'utilisateur a appuyé sur Entrée sans réponse, passer à la question suivante
        if reponse is None:
            os.system('clear' if os.name != 'nt' else 'cls')
            continue

        reponse -= 1  # Convertir en index (1-based to 0-based)

        if choix_propose[reponse]["correct"]:
            for question in quiz["questions"]:
                if question_pose["question_id"] == question["question_id"]:
                    question["correct"] = True

        # Effacer l'écran avant la question suivante
        os.system('clear' if os.name != 'nt' else 'cls')


def save_results(quiz: Dict, filename: str) -> None:
    """Enregistre les résultats du quiz dans un fichier JSON."""
    with open(filename, 'w', encoding='utf-8') as fichier:
        json.dump(quiz, fichier, indent=2, ensure_ascii=False)

    # Calculer le score
    correct_count = sum(1 for q in quiz['questions'] if q['correct'])
    total_count = len(quiz['questions'])

    print(f"\n{'='*60}")
    print(f"  Résultats")
    print(f"{'='*60}")
    print(f"Score: {correct_count}/{total_count}")
    print(f"✅ Les résultats ont été sauvegardés")


def main():
    """Point d'entrée principal de l'application."""
    parser = argparse.ArgumentParser(
        description="Quiz Python - Application interactive de quiz"
    )
    parser.add_argument(
        '-q', '--quiz',
        default='quiz',
        help='Nom du fichier de quiz sans extension (défaut: quiz)'
    )
    parser.add_argument(
        '-o', '--output',
        default='resultat',
        help='Nom du fichier de résultats sans extension (défaut: resultat)'
    )
    parser.add_argument(
        '-r', '--resume',
        action='store_true',
        help='Reprendre un quiz sur les questions incorrectes du fichier de résultats'
    )

    args = parser.parse_args()

    # Construire les chemins complets avec les dossiers et extensions
    script_dir = os.path.dirname(os.path.abspath(__file__))
    quiz_path = os.path.join(script_dir, 'quiz', f'{args.quiz}.json')
    output_path = os.path.join(script_dir, 'resultats', f'{args.output}.json')

    try:
        if args.resume:
            # Mode reprise: charger le fichier de résultats existant
            if not os.path.exists(output_path):
                print(f"❌ Erreur: Le fichier de résultats '{output_path}' n'existe pas.")
                return 1

            quiz = load_quiz(output_path)

            # Calculer le score actuel
            correct_count = sum(1 for q in quiz['questions'] if q['correct'])
            total_count = len(quiz['questions'])

            print("\n" + "="*60)
            print("  Reprise du Quiz")
            print("="*60 + "\n")
            print(f"Quiz: {quiz['quiz_title']}")
            print(f"Utilisateur: {quiz['prenom']} {quiz['nom']}")
            print(f"\nScore actuel : {correct_count} / {total_count}")
            input("\nAppuyez sur Entrée pour reprendre...")

            # Effacer l'écran avant d'afficher la première question
            os.system('clear' if os.name != 'nt' else 'cls')
        else:
            # Mode normal: charger le quiz depuis le fichier source
            data = load_quiz(quiz_path)

            # Construire la structure
            quiz = build_quiz_structure(data)

            # Demander nom et prénom
            print("\n" + "="*60)
            print(f"  Bienvenue au {quiz['quiz_title']}")
            print("="*60 + "\n")
            quiz['nom'] = input("Entrez votre nom : ").strip()
            quiz['prenom'] = input("Entrez votre prénom : ").strip()

            input("\nAppuyez sur Entrée pour commencer...")

            # Effacer l'écran avant d'afficher la première question
            os.system('clear' if os.name != 'nt' else 'cls')

        # Lancer le questionnaire
        run_questionnaire(quiz)

        # Sauvegarder les résultats
        save_results(quiz, output_path)

    except FileNotFoundError:
        print(f"❌ Erreur: Le fichier '{quiz_path}' n'a pas été trouvé.")
        return 1
    except json.JSONDecodeError:
        print(f"❌ Erreur: Le fichier '{quiz_path}' n'est pas un JSON valide.")
        return 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Quiz interrompu par l'utilisateur.")
        save_results(quiz, output_path)
        return 130
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
