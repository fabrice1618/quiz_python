# Dossier résultats

Dossier où sont stockés les résultats de quiz.

## Chiffrement

Les fichiers de résultats sont automatiquement chiffrés avec un algorithme XOR (clé 0xA5) pour empêcher la lecture directe par les étudiants.

Le chiffrement est transparent :
- Lors de la lecture, les fichiers sont automatiquement déchiffrés
- Lors de l'écriture, les fichiers sont automatiquement chiffrés
- La compatibilité avec les anciens fichiers JSON clairs est assurée