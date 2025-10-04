#!/usr/bin/env python3
"""
Quiz Python - Application interactive de quiz
Convertie depuis quiz.ipynb
"""

import json
import random
import argparse
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


def get_valid_input(prompt: str, min_val: int, max_val: int) -> int:
    """Obtient une entrée valide de l'utilisateur entre min_val et max_val."""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                print(f"⚠️  Veuillez entrer un nombre entre {min_val} et {max_val}")
                continue

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

    print(f"\n{'='*60}")
    print(f"  {quiz['quiz_title']}")
    print(f"{'='*60}\n")

    for question_pose in questions_selectionnees:
        print(f'{question_pose["question_id"]}) {question_pose["question"]}\n')

        choix_propose = random.sample(question_pose["liste_choix"], len(question_pose["liste_choix"]))

        for numero, choix in enumerate(choix_propose):
            print(f'\t{numero + 1} - {choix["choix"]}')

        reponse = get_valid_input("\nRenseignez votre choix : ", 1, len(choix_propose)) - 1

        if choix_propose[reponse]["correct"]:
            print("✅ Correct!\n")
            for question in quiz["questions"]:
                if question_pose["question_id"] == question["question_id"]:
                    question["correct"] = True
        else:
            print("❌ Incorrect!\n")


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
    print(f"✅ Les résultats ont été sauvegardés dans '{filename}'")


def main():
    """Point d'entrée principal de l'application."""
    parser = argparse.ArgumentParser(
        description="Quiz Python - Application interactive de quiz"
    )
    parser.add_argument(
        '-q', '--quiz',
        default='quiz_python.json',
        help='Chemin vers le fichier JSON du quiz (défaut: quiz_python.json)'
    )
    parser.add_argument(
        '-o', '--output',
        default='resultat.json',
        help='Chemin vers le fichier de résultats (défaut: resultat.json)'
    )

    args = parser.parse_args()

    try:
        # Charger le quiz
        data = load_quiz(args.quiz)

        # Construire la structure
        quiz = build_quiz_structure(data)

        # Demander nom et prénom
        print("\n" + "="*60)
        print("  Bienvenue au Quiz Python!")
        print("="*60 + "\n")
        quiz['nom'] = input("Entrez votre nom : ").strip()
        quiz['prenom'] = input("Entrez votre prénom : ").strip()

        # Lancer le questionnaire
        run_questionnaire(quiz)

        # Sauvegarder les résultats
        save_results(quiz, args.output)

    except FileNotFoundError:
        print(f"❌ Erreur: Le fichier '{args.quiz}' n'a pas été trouvé.")
        return 1
    except json.JSONDecodeError:
        print(f"❌ Erreur: Le fichier '{args.quiz}' n'est pas un JSON valide.")
        return 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Quiz interrompu par l'utilisateur.")
        return 130
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
