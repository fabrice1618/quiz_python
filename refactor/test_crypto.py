"""
Tests unitaires pour le module crypto.

Lance les tests avec : python3 -m unittest test_crypto
"""

import unittest
import crypto


class TestXorBytes(unittest.TestCase):
    """Tests pour la fonction xor_bytes()"""

    def test_xor_symmetric(self):
        """XOR appliqué deux fois doit retourner les données originales"""
        data = b"Hello World"
        encrypted = crypto.xor_bytes(data)
        decrypted = crypto.xor_bytes(encrypted)
        self.assertEqual(data, decrypted)

    def test_xor_empty(self):
        """XOR sur données vides doit retourner vide"""
        data = b""
        result = crypto.xor_bytes(data)
        self.assertEqual(result, b"")

    def test_xor_single_byte(self):
        """XOR sur un seul octet"""
        data = b"A"
        encrypted = crypto.xor_bytes(data)
        # A (0x41) XOR 0xA5 = 0xE4
        self.assertEqual(encrypted, b"\xe4")
        # Vérifier symétrie
        decrypted = crypto.xor_bytes(encrypted)
        self.assertEqual(decrypted, data)

    def test_xor_with_custom_key(self):
        """XOR avec clé personnalisée"""
        data = b"Test"
        custom_key = 0xFF
        encrypted = crypto.xor_bytes(data, key=custom_key)
        decrypted = crypto.xor_bytes(encrypted, key=custom_key)
        self.assertEqual(data, decrypted)


class TestIsEncrypted(unittest.TestCase):
    """Tests pour la fonction is_encrypted()"""

    def test_detect_plain_json_curly_brace(self):
        """Détection de JSON clair commençant par {"""
        plain = b'{"key": "value"}'
        self.assertFalse(crypto.is_encrypted(plain))

    def test_detect_plain_json_square_bracket(self):
        """Détection de JSON clair commençant par ["""
        plain = b'["item1", "item2"]'
        self.assertFalse(crypto.is_encrypted(plain))

    def test_detect_plain_json_with_whitespace(self):
        """Détection de JSON clair avec espaces au début"""
        plain = b'  {"key": "value"}'
        self.assertFalse(crypto.is_encrypted(plain))

    def test_detect_encrypted_json(self):
        """Détection de JSON chiffré"""
        plain = b'{"key": "value"}'
        encrypted = crypto.xor_bytes(plain)
        self.assertTrue(crypto.is_encrypted(encrypted))

    def test_detect_empty_file(self):
        """Fichier vide doit être considéré comme non chiffré"""
        self.assertFalse(crypto.is_encrypted(b""))

    def test_detect_encrypted_array(self):
        """Détection de JSON array chiffré"""
        plain = b'["test"]'
        encrypted = crypto.xor_bytes(plain)
        self.assertTrue(crypto.is_encrypted(encrypted))


class TestEncryptDecryptJson(unittest.TestCase):
    """Tests pour encrypt_json() et decrypt_json()"""

    def test_encrypt_decrypt_simple_dict(self):
        """Cycle complet encrypt/decrypt avec dict simple"""
        data = {"name": "Test", "value": 123}
        encrypted = crypto.encrypt_json(data)
        decrypted = crypto.decrypt_json(encrypted)
        self.assertEqual(data, decrypted)

    def test_encrypt_decrypt_nested_dict(self):
        """Cycle complet avec dict imbriqué"""
        data = {
            "quiz_title": "Test Quiz",
            "questions": [
                {"id": 1, "question": "Q1"},
                {"id": 2, "question": "Q2"}
            ]
        }
        encrypted = crypto.encrypt_json(data)
        decrypted = crypto.decrypt_json(encrypted)
        self.assertEqual(data, decrypted)

    def test_encrypt_decrypt_with_unicode(self):
        """Préservation des caractères UTF-8 (accents français)"""
        data = {
            "titre": "Quiz Français",
            "nom": "José",
            "prénom": "François",
            "description": "Élève à l'école"
        }
        encrypted = crypto.encrypt_json(data)
        decrypted = crypto.decrypt_json(encrypted)
        self.assertEqual(data, decrypted)

    def test_encrypt_returns_bytes(self):
        """encrypt_json doit retourner des bytes"""
        data = {"test": True}
        encrypted = crypto.encrypt_json(data)
        self.assertIsInstance(encrypted, bytes)

    def test_encrypted_is_detected_as_encrypted(self):
        """Le résultat de encrypt_json doit être détecté comme chiffré"""
        data = {"test": True}
        encrypted = crypto.encrypt_json(data)
        self.assertTrue(crypto.is_encrypted(encrypted))

    def test_decrypt_invalid_data_raises_error(self):
        """Décrypter des données invalides doit lever une exception"""
        invalid_encrypted = b"\x00\x01\x02\x03"
        with self.assertRaises((UnicodeDecodeError, ValueError)):
            crypto.decrypt_json(invalid_encrypted)


class TestLoadJson(unittest.TestCase):
    """Tests pour load_json() (auto-détection)"""

    def test_load_plain_json(self):
        """Charger du JSON clair"""
        plain_bytes = b'{"test": true, "value": 42}'
        result = crypto.load_json(plain_bytes)
        self.assertEqual(result, {"test": True, "value": 42})

    def test_load_encrypted_json(self):
        """Charger du JSON chiffré"""
        data = {"test": True, "value": 42}
        encrypted = crypto.encrypt_json(data)
        result = crypto.load_json(encrypted)
        self.assertEqual(result, data)

    def test_load_plain_json_with_whitespace(self):
        """Charger du JSON clair avec espaces"""
        plain_bytes = b'  \n{"test": true}'
        result = crypto.load_json(plain_bytes)
        self.assertEqual(result, {"test": True})

    def test_load_array(self):
        """Charger un JSON array"""
        plain_bytes = b'[1, 2, 3]'
        result = crypto.load_json(plain_bytes)
        self.assertEqual(result, [1, 2, 3])

    def test_load_encrypted_array(self):
        """Charger un JSON array chiffré"""
        data = [1, 2, 3]
        encrypted = crypto.encrypt_json(data)
        result = crypto.load_json(encrypted)
        self.assertEqual(result, data)

    def test_load_with_unicode_plain(self):
        """Charger du JSON clair avec caractères UTF-8"""
        plain_bytes = '{"nom": "François"}'.encode('utf-8')
        result = crypto.load_json(plain_bytes)
        self.assertEqual(result, {"nom": "François"})

    def test_load_with_unicode_encrypted(self):
        """Charger du JSON chiffré avec caractères UTF-8"""
        data = {"nom": "François", "ville": "Montréal"}
        encrypted = crypto.encrypt_json(data)
        result = crypto.load_json(encrypted)
        self.assertEqual(result, data)


class TestSaveJson(unittest.TestCase):
    """Tests pour save_json()"""

    def test_save_encrypted_by_default(self):
        """save_json doit chiffrer par défaut"""
        data = {"test": True}
        saved = crypto.save_json(data)
        self.assertTrue(crypto.is_encrypted(saved))

    def test_save_encrypted_explicit(self):
        """save_json avec encrypt=True"""
        data = {"test": True}
        saved = crypto.save_json(data, encrypt=True)
        self.assertTrue(crypto.is_encrypted(saved))

    def test_save_plain(self):
        """save_json avec encrypt=False"""
        data = {"test": True}
        saved = crypto.save_json(data, encrypt=False)
        self.assertFalse(crypto.is_encrypted(saved))

    def test_save_plain_is_readable(self):
        """JSON sauvegardé en clair doit être lisible"""
        data = {"test": True, "value": 42}
        saved = crypto.save_json(data, encrypt=False)
        # Doit pouvoir le charger directement comme JSON
        result = crypto.load_json(saved)
        self.assertEqual(result, data)

    def test_save_encrypted_is_readable(self):
        """JSON sauvegardé chiffré doit être lisible avec load_json"""
        data = {"test": True, "value": 42}
        saved = crypto.save_json(data, encrypt=True)
        result = crypto.load_json(saved)
        self.assertEqual(result, data)


class TestRealWorldScenarios(unittest.TestCase):
    """Tests de scénarios réels d'utilisation"""

    def test_quiz_structure(self):
        """Test avec structure de quiz réelle"""
        quiz_data = {
            "quiz_title": "Python Basics",
            "questions": [
                {
                    "id": 1,
                    "question": "Qu'est-ce que Python?",
                    "choices": ["Un langage", "Un serpent", "Un framework"],
                    "answer_index": 0
                },
                {
                    "id": 2,
                    "question": "Quelle est la syntaxe pour un commentaire?",
                    "choices": ["//", "#", "/**/"],
                    "answer_index": 1
                }
            ]
        }

        # Chiffrer et déchiffrer
        encrypted = crypto.encrypt_json(quiz_data)
        decrypted = crypto.decrypt_json(encrypted)
        self.assertEqual(quiz_data, decrypted)

        # Vérifier que load_json fonctionne
        loaded = crypto.load_json(encrypted)
        self.assertEqual(quiz_data, loaded)

    def test_results_structure(self):
        """Test avec structure de résultats réelle"""
        results_data = {
            "quiz_name": "python_basics",
            "nom": "Dupont",
            "prenom": "Jean",
            "correct_count": 3,
            "questions": [
                {"question_id": 1, "correct": True},
                {"question_id": 2, "correct": True},
                {"question_id": 3, "correct": True},
                {"question_id": 4, "correct": False}
            ]
        }

        # Sauvegarder et charger
        saved = crypto.save_json(results_data, encrypt=True)
        loaded = crypto.load_json(saved)
        self.assertEqual(results_data, loaded)

    def test_migration_scenario(self):
        """Test du scénario de migration: fichier clair → chiffré"""
        # Fichier existant en clair
        original_data = {"quiz": "test", "version": 1}
        plain_bytes = crypto.save_json(original_data, encrypt=False)

        # Premier chargement (fichier clair)
        loaded1 = crypto.load_json(plain_bytes)
        self.assertEqual(original_data, loaded1)

        # Sauvegarde en chiffré
        encrypted_bytes = crypto.save_json(loaded1, encrypt=True)

        # Second chargement (fichier chiffré)
        loaded2 = crypto.load_json(encrypted_bytes)
        self.assertEqual(original_data, loaded2)


if __name__ == '__main__':
    unittest.main()
