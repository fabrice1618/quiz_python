#!/usr/bin/env python3
"""
Outil de migration pour chiffrer les fichiers JSON existants.

Ce script parcourt les dossiers quiz/ et resultats/ et convertit
tous les fichiers JSON clairs en format chiffré.

Usage:
    python3 migrate_encryption.py

Le script détecte automatiquement les fichiers déjà chiffrés et ne les
modifie pas.
"""

import sys
from pathlib import Path
import crypto
import config


def migrate_directory(directory: Path, description: str) -> tuple[int, int, int]:
    """
    Migre tous les fichiers JSON d'un répertoire vers le format chiffré.

    Args:
        directory: Chemin du répertoire à traiter
        description: Description du répertoire pour l'affichage

    Returns:
        Tuple (encrypted_count, already_encrypted_count, error_count)
    """
    print(f"\n{description}:")
    print("─" * 60)

    # Chercher tous les fichiers .json
    json_files = list(directory.glob("*.json"))

    if not json_files:
        print(f"  Aucun fichier trouvé dans {directory}")
        return (0, 0, 0)

    encrypted_count = 0
    already_encrypted_count = 0
    error_count = 0

    for json_file in sorted(json_files):
        try:
            # Lire le fichier
            with open(json_file, "rb") as f:
                file_bytes = f.read()

            # Vérifier si déjà chiffré
            if crypto.is_encrypted(file_bytes):
                print(f"  ✓ {json_file.name:<30} déjà chiffré")
                already_encrypted_count += 1
                continue

            # Charger le JSON clair
            data = crypto.load_json(file_bytes)

            # Sauvegarder en format chiffré
            encrypted_bytes = crypto.save_json(data, encrypt=True)

            # Écrire le fichier
            with open(json_file, "wb") as f:
                f.write(encrypted_bytes)

            print(f"  ✓ {json_file.name:<30} chiffré avec succès")
            encrypted_count += 1

        except Exception as e:
            print(f"  ✗ {json_file.name:<30} erreur: {e}")
            error_count += 1

    return (encrypted_count, already_encrypted_count, error_count)


def main():
    """Point d'entrée principal du script."""
    print("=" * 60)
    print("Outil de Migration - Chiffrement des fichiers Quiz")
    print("=" * 60)

    # Afficher la configuration
    print(f"\nRépertoire de données: {config.data_path}")

    # Statistiques globales
    total_encrypted = 0
    total_already = 0
    total_errors = 0

    # Migrer les fichiers de quiz
    quiz_dir = config.data_path / config.QUIZ_PATH
    if quiz_dir.exists():
        enc, already, err = migrate_directory(quiz_dir, "Fichiers Quiz")
        total_encrypted += enc
        total_already += already
        total_errors += err
    else:
        print(f"\n⚠ Répertoire quiz non trouvé: {quiz_dir}")

    # Migrer les fichiers de résultats
    results_dir = config.data_path / config.RESULT_PATH
    if results_dir.exists():
        enc, already, err = migrate_directory(results_dir, "Fichiers Résultats")
        total_encrypted += enc
        total_already += already
        total_errors += err
    else:
        print(f"\n⚠ Répertoire résultats non trouvé: {results_dir}")

    # Afficher le résumé
    print("\n" + "=" * 60)
    print("Résumé de la migration:")
    print("=" * 60)
    print(f"  Fichiers chiffrés:           {total_encrypted}")
    print(f"  Fichiers déjà chiffrés:      {total_already}")
    print(f"  Erreurs:                     {total_errors}")
    print(f"  Total traité:                {total_encrypted + total_already + total_errors}")
    print("=" * 60)

    if total_errors > 0:
        print("\n⚠ Des erreurs se sont produites. Vérifiez les messages ci-dessus.")
        return 1
    elif total_encrypted == 0 and total_already == 0:
        print("\n⚠ Aucun fichier trouvé à migrer.")
        return 0
    else:
        print("\n✓ Migration terminée avec succès!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
