#!/usr/bin/env python3
"""
Test pour vérifier que les résultats sont bien retournés
même en cas de KeyboardInterrupt (Ctrl+C)
"""

import sys
import unittest
from unittest.mock import patch, MagicMock
import main
import quiz_data
import resultats_data


class TestKeyboardInterrupt(unittest.TestCase):
    """Test de la gestion du KeyboardInterrupt"""

    def setUp(self):
        """Prépare les données de test"""
        # Créer un mini quiz avec 3 questions
        self.quiz = {
            "quiz_title": "Test Quiz",
            "quiz_name": "test",
            "nombre_questions": 3,
            "questions": [
                {
                    "question_id": 1,
                    "question": "Question 1",
                    "liste_choix": [
                        {"choix": "A", "correct": True},
                        {"choix": "B", "correct": False},
                    ],
                },
                {
                    "question_id": 2,
                    "question": "Question 2",
                    "liste_choix": [
                        {"choix": "A", "correct": False},
                        {"choix": "B", "correct": True},
                    ],
                },
                {
                    "question_id": 3,
                    "question": "Question 3",
                    "liste_choix": [
                        {"choix": "A", "correct": True},
                        {"choix": "B", "correct": False},
                    ],
                },
            ],
        }

        # Créer les résultats initiaux
        self.resultats = {
            "quiz_name": "test",
            "nom": "Doe",
            "prenom": "John",
            "correct_count": 0,
            "questions": [
                {"question_id": 1, "correct": False},
                {"question_id": 2, "correct": False},
                {"question_id": 3, "correct": False},
            ],
        }

    @patch("main.random.sample")
    @patch("main.ui.form_question")
    @patch("main.quiz_data.read_question")
    @patch("main.resultats_data.questions_a_poser")
    def test_keyboard_interrupt_saves_partial_results(
        self, mock_questions_a_poser, mock_read_question, mock_form_question, mock_random_sample
    ):
        """
        Test que les résultats partiels sont retournés quand
        l'utilisateur fait Ctrl+C après avoir répondu à 2 questions
        """
        # Désactiver le mélange aléatoire pour avoir un comportement déterministe
        mock_random_sample.side_effect = lambda x, k: x

        # Simuler que toutes les questions doivent être posées
        mock_questions_a_poser.return_value = [1, 2, 3]

        # Simuler la lecture des questions
        mock_read_question.side_effect = lambda q_id, quiz: next(
            q for q in self.quiz["questions"] if q["question_id"] == q_id
        )

        # Simuler les réponses de l'utilisateur:
        # - Question 1: réponse correcte (index 0)
        # - Question 2: réponse correcte (index 1)
        # - Question 3: KeyboardInterrupt (Ctrl+C)
        mock_form_question.side_effect = [0, 1, KeyboardInterrupt()]

        # Exécuter le questionnaire
        resultats_finaux = main.run_questionnaire(self.quiz, self.resultats)

        # Vérifier que les résultats contiennent les 2 réponses données avant le Ctrl+C
        self.assertEqual(resultats_finaux["correct_count"], 2)
        self.assertTrue(resultats_finaux["questions"][0]["correct"])
        self.assertTrue(resultats_finaux["questions"][1]["correct"])
        self.assertFalse(resultats_finaux["questions"][2]["correct"])


if __name__ == "__main__":
    # Exécuter le test
    suite = unittest.TestLoader().loadTestsFromTestCase(TestKeyboardInterrupt)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Retourner le code de sortie approprié
    sys.exit(0 if result.wasSuccessful() else 1)
