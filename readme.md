# Quiz Python

Application interactive de quiz en ligne de commande écrite en Python.

## Installation

### Installation rapide via curl

Pour installer le quiz directement depuis GitHub :

```bash
# Installer un quiz spécifique
curl -sSL https://raw.githubusercontent.com/fabrice1618/quiz_python/main/install.sh | bash -s -- bases_python

# Installer tous les quiz disponibles
curl -sSL https://raw.githubusercontent.com/fabrice1618/quiz_python/main/install.sh | bash -s -- --all

# Installer dans un répertoire personnalisé
curl -sSL https://raw.githubusercontent.com/fabrice1618/quiz_python/main/install.sh | bash -s -- bases_python --dir ~/mes_quiz
```

Pour plus de détails sur l'installation, consultez [INSTALL.md](INSTALL.md).

### Installation manuelle

Le script utilise uniquement des bibliothèques standard Python (Python 3.6+).

```bash
git clone https://github.com/fabrice1618/quiz_python.git
cd quiz_python
chmod +x quiz
```

## Structure des dossiers

```
quiz_python/
├── quiz                            # Script de lancement (shell)
├── install.sh                      # Script d'installation à distance
├── INSTALL.md                      # Documentation d'installation
├── .quiz/
│   ├── quiz.py                     # Application Python principale
│   ├── quiz/                       # Fichiers de quiz (format JSON)
│   │   ├── bases_python.json       # Quiz sur les bases de Python (100 questions)
│   │   ├── linux.json              # Quiz sur Linux
│   │   ├── quiz.json               # Quiz général
│   │   └── python50.json           # Quiz Python (50 questions)
│   └── resultats/                  # Fichiers de résultats
│       └── resultat.json
└── readme.md                       # Ce fichier
```

## Utilisation

### Lancer un nouveau quiz

```bash
# Quiz par défaut (quiz.json)
./quiz

# Quiz spécifique
./quiz -q bases_python

# Spécifier le fichier de sortie
./quiz -q bases_python -o mes_resultats

# Les deux options combinées
./quiz -q bases_python -o john_results
```

### Reprendre un quiz

Pour reprendre un quiz et refaire uniquement les questions incorrectes :

```bash
# Reprendre le quiz par défaut (resultat.json)
./quiz -r

# Reprendre un quiz spécifique
./quiz -r -o mes_resultats
```

## Options de ligne de commande

| Option | Description | Défaut |
|--------|-------------|--------|
| `-q`, `--quiz` | Nom du fichier de quiz (sans extension .json) | `quiz` |
| `-o`, `--output` | Nom du fichier de résultats (sans extension .json) | `resultat` |
| `-r`, `--resume` | Reprendre un quiz sur les questions incorrectes | - |
| `-h`, `--help` | Afficher l'aide | - |

## Quiz disponibles

- **bases_python** : Quiz complet sur les bases de Python (100 questions)
  - Types de données, fonctions, boucles, listes, dictionnaires, etc.
- **linux** : Quiz sur les commandes et concepts Linux
- **quiz** : Quiz général
- **python50** : Quiz Python avec 50 questions sélectionnées

## Fonctionnalités

### Pendant le quiz
- **Questions aléatoires** : Les questions sont présentées dans un ordre aléatoire
- **Choix aléatoires** : Les réponses sont mélangées pour chaque question
- **Numérotation progressive** : Affichage "3 / 50 - Question..."
- **Formatage du code** : Les blocs de code multilignes sont correctement formatés
- **Passer une question** : Appuyez sur Entrée sans saisir de réponse
- **Écran clair** : L'écran est effacé entre chaque question pour une meilleure lisibilité

### Reprise et sauvegarde
- **Reprise intelligente** : Affichage du score actuel lors de la reprise
- **Sauvegarde automatique** : Les résultats sont enregistrés automatiquement
- **Sauvegarde lors d'interruption** : Les résultats sont sauvegardés même en cas d'interruption (CTRL+C)

### Interface
- **Message de bienvenue personnalisé** : Affiche le titre du quiz chargé
- **Pause avant démarrage** : Appuyer sur Entrée pour commencer
- **Score final** : Affichage du score à la fin du quiz

## Format du fichier de quiz

Les fichiers de quiz doivent être au format JSON et placés dans `.quiz/quiz/` :

```json
{
  "quiz_title": "Quiz - Bases de Python",
  "language": "fr",
  "questions": [
    {
      "id": 1,
      "question": "Quelle instruction affiche le texte Hello World en Python ?",
      "choices": [
        "print(\"Hello World\")",
        "echo \"Hello World\"",
        "console.log(\"Hello World\")",
        "printf(\"Hello World\")"
      ],
      "answer_index": 0
    },
    {
      "id": 2,
      "question": "Quelle est la bonne syntaxe pour définir une fonction ?",
      "choices": [
        "def add(x, y):\n    return x + y",
        "function add(x, y) {\n  return x + y;\n}",
        "def add x, y:\n    return x + y",
        "def add(x, y) -> x + y"
      ],
      "answer_index": 0
    }
  ]
}
```

### Structure

- `quiz_title` : Titre du quiz affiché à l'utilisateur
- `language` : Langue du quiz (ex: "fr" pour français)
- `questions` : Liste des questions
  - `id` : Identifiant unique de la question
  - `question` : Texte de la question
  - `choices` : Liste des choix possibles (4 choix recommandés)
    - Support du formatage multiligne avec `\n` pour le code
  - `answer_index` : Index de la bonne réponse (commence à 0)

## Format du fichier de résultats

Les résultats sont sauvegardés dans `.quiz/resultats/` au format JSON :

```json
{
  "quiz_title": "Quiz - Bases de Python",
  "nom": "Dupont",
  "prenom": "Jean",
  "questions": [
    {
      "question_id": 1,
      "question": "Quelle instruction affiche le texte Hello World en Python ?",
      "correct": true,
      "liste_choix": [
        {
          "choix": "print(\"Hello World\")",
          "correct": true
        },
        {
          "choix": "echo \"Hello World\"",
          "correct": false
        }
      ]
    }
  ]
}
```

Le champ `correct` indique si la question a été répondue correctement. Lors d'une reprise, seules les questions avec `correct: false` seront proposées.

## Exemples

### Nouveau quiz
```bash
# Lancer le quiz sur les bases de Python
./quiz -q bases_python -o resultats_etudiant1
```

### Reprendre un quiz existant
```bash
# Reprendre le quiz pour refaire les questions incorrectes
./quiz -r -o resultats_etudiant1
```

Le programme affichera le score actuel (ex: "Score actuel : 3 / 5") avant de reprendre.

### Pendant le quiz
- Saisir un nombre (1-4) pour répondre
- Appuyer sur Entrée sans saisir de réponse pour passer la question
- CTRL+C pour interrompre (les résultats seront sauvegardés)
- L'écran est effacé après chaque réponse

## Créer un alias (optionnel)

Pour utiliser la commande `quiz` depuis n'importe où :

```bash
# Ajouter dans ~/.bashrc ou ~/.zshrc
alias quiz='/chemin/vers/quiz_python/quiz'

# Ou créer un lien symbolique (nécessite sudo)
sudo ln -s /chemin/vers/quiz_python/quiz /usr/local/bin/quiz
```

## Développement

### Ajouter un nouveau quiz

1. Créer un fichier JSON dans `.quiz/quiz/`
2. Suivre le format décrit ci-dessus
3. Lancer avec `./quiz -q nom_du_fichier`

### Ajouter au script d'installation

Pour qu'un nouveau quiz soit disponible via `install.sh --all`, l'ajouter dans la liste `QUIZ_LIST` du fichier `install.sh` :

```bash
QUIZ_LIST=("bases_python" "linux" "quiz" "nouveau_quiz")
```

## License

Ce projet est sous licence libre. Consultez le fichier LICENSE pour plus de détails.

## Contributions

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer de nouvelles fonctionnalités
- Ajouter de nouveaux quiz
- Améliorer la documentation

## Auteur

Fabrice - [GitHub](https://github.com/fabrice1618/quiz_python)
