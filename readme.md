# Quiz Python

Application interactive de quiz en ligne de commande.

## Installation

Aucune installation requise. Le script utilise uniquement des bibliothèques standard Python.

## Structure des dossiers

```
quiz_python/
├── quiz.py                          # Application principale
├── quiz_data/
│   ├── quiz/                        # Fichiers de quiz (format JSON)
│   │   └── quiz_python.json
│   └── resultats/                   # Fichiers de résultats
│       └── resultat.json
```

## Utilisation

### Lancer un nouveau quiz

```bash
# Quiz par défaut (quiz_python.json)
python3 quiz.py

# Quiz personnalisé
python3 quiz.py -q mon_quiz

# Spécifier le fichier de sortie
python3 quiz.py -o mes_resultats

# Les deux options combinées
python3 quiz.py -q advanced_quiz -o john_results
```

### Reprendre un quiz

Pour reprendre un quiz et refaire uniquement les questions incorrectes :

```bash
# Reprendre le quiz par défaut (resultat.json)
python3 quiz.py -r

# Reprendre un quiz spécifique
python3 quiz.py -r -o mes_resultats
```

## Options de ligne de commande

| Option | Description | Défaut |
|--------|-------------|--------|
| `-q`, `--quiz` | Nom du fichier de quiz (sans extension .json) | `quiz_python` |
| `-o`, `--output` | Nom du fichier de résultats (sans extension .json) | `resultat` |
| `-r`, `--resume` | Reprendre un quiz sur les questions incorrectes | - |

## Fonctionnalités

- **Questions aléatoires** : Les questions sont présentées dans un ordre aléatoire
- **Choix aléatoires** : Les réponses sont mélangées pour chaque question
- **Passer une question** : Appuyez sur Entrée sans saisir de réponse
- **Reprise** : Possibilité de reprendre un quiz pour refaire les questions incorrectes
- **Sauvegarde automatique** : Les résultats sont enregistrés automatiquement

## Format du fichier de quiz

Les fichiers de quiz doivent être au format JSON et placés dans `quiz_data/quiz/` :

```json
{
  "quiz_title": "Mon Quiz",
  "language": "fr",
  "questions": [
    {
      "id": 1,
      "question": "Quelle est la capitale de la France ?",
      "choices": [
        "Paris",
        "Londres",
        "Berlin",
        "Madrid"
      ],
      "answer_index": 0
    }
  ]
}
```

### Structure

- `quiz_title` : Titre du quiz
- `language` : Langue du quiz
- `questions` : Liste des questions
  - `id` : Identifiant unique de la question
  - `question` : Texte de la question
  - `choices` : Liste des choix possibles (4 choix)
  - `answer_index` : Index de la bonne réponse (0-3)

## Format du fichier de résultats

Les résultats sont sauvegardés dans `quiz_data/resultats/` au format JSON :

```json
{
  "quiz_title": "Mon Quiz",
  "nom": "Dupont",
  "prenom": "Jean",
  "questions": [
    {
      "question_id": 1,
      "question": "Quelle est la capitale de la France ?",
      "correct": true,
      "liste_choix": [...]
    }
  ]
}
```

Le champ `correct` indique si la question a été répondue correctement.

## Exemples

### Nouveau quiz
```bash
python3 quiz.py -q bases_python -o resultats_etudiant1
```

### Reprendre un quiz existant
```bash
python3 quiz.py -r -o resultats_etudiant1
```

### Pendant le quiz
- Saisir un nombre (1-4) pour répondre
- Appuyer sur Entrée sans saisir de réponse pour passer la question
- L'écran est effacé après chaque réponse
