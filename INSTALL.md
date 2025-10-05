# Guide d'installation du Quiz Python

Ce document explique comment installer le Quiz Python sur n'importe quelle machine Linux ou MacBook.

## Prérequis

- **Python 3** : Le script nécessite Python 3 (généralement déjà installé sur Linux et MacBook)
- **curl** : Utilisé pour télécharger les fichiers (généralement déjà installé)
- **bash** : Le shell utilisé pour le script d'installation (standard sur Linux/MacBook)

## Configuration du script d'installation

Le script d'installation est configuré pour télécharger depuis :

```bash
GITHUB_RAW_URL="https://raw.githubusercontent.com/fabrice1618/quiz_python/main"
```

## Méthodes d'installation

### Méthode 1 : Installation directe avec curl (recommandée)

Cette méthode permet d'installer le quiz en une seule commande :

```bash
# Installer un quiz spécifique
curl -sSL https://raw.githubusercontent.com/fabrice1618/quiz_python/main/install.sh | bash -s -- bases_python

# Installer tous les quiz disponibles
curl -sSL https://raw.githubusercontent.com/fabrice1618/quiz_python/main/install.sh | bash -s -- --all

# Installer dans un répertoire personnalisé
curl -sSL https://raw.githubusercontent.com/fabrice1618/quiz_python/main/install.sh | bash -s -- bases_python --dir ~/mes_quiz
```

### Méthode 2 : Télécharger puis exécuter

```bash
# Télécharger le script
curl -O https://raw.githubusercontent.com/fabrice1618/quiz_python/main/install.sh

# Rendre le script exécutable
chmod +x install.sh

# Exécuter l'installation
./install.sh bases_python
```

### Méthode 3 : Clone du repository (pour les développeurs)

```bash
# Cloner le repository
git clone https://github.com/fabrice1618/quiz_python.git

# Copier manuellement les fichiers nécessaires
mkdir -p ~/quiz
cp -r quiz_python/quiz ~/quiz/
cp -r quiz_python/.quiz ~/quiz/
chmod +x ~/quiz/quiz
```

## Quiz disponibles

Le script d'installation permet de télécharger les quiz suivants :

- **bases_python** : Quiz sur les bases de Python (100 questions - boucles, fonctions, types, etc.)
- **linux** : Quiz sur les commandes et concepts Linux
- **quiz** : Quiz général
- **python50** : Quiz Python (50 questions sélectionnées)

## Options du script d'installation

```
Usage:
    ./install.sh <nom_du_quiz> [options]

Arguments:
    nom_du_quiz     Nom du quiz à installer (bases_python, linux, quiz)
                    ou --all pour installer tous les quiz

Options:
    --dir <path>    Répertoire d'installation (défaut: ~/quiz)
    -h, --help      Afficher l'aide
```

## Exemples d'utilisation après installation

Une fois le quiz installé, vous pouvez l'utiliser ainsi :

```bash
# Se déplacer dans le répertoire d'installation
cd ~/quiz

# Lancer un quiz
./quiz -q bases_python

# Lancer un quiz avec un fichier de résultats personnalisé
./quiz -q bases_python -o mon_resultat

# Reprendre un quiz précédent (questions non réussies uniquement)
./quiz -r -o mon_resultat

# Afficher l'aide
./quiz --help
```

## Créer un alias (optionnel)

Pour utiliser la commande `quiz` depuis n'importe où :

### Option 1 : Alias dans le shell

Ajoutez cette ligne dans `~/.bashrc` ou `~/.zshrc` :

```bash
alias quiz='~/quiz/quiz'
```

Puis rechargez la configuration :
```bash
source ~/.bashrc  # ou source ~/.zshrc
```

### Option 2 : Lien symbolique (nécessite sudo)

```bash
sudo ln -s ~/quiz/quiz /usr/local/bin/quiz
```

Après cela, vous pourrez lancer `quiz` depuis n'importe quel répertoire :

```bash
quiz -q bases_python
```

## Structure des fichiers après installation

```
~/quiz/
├── quiz                    # Script de lancement principal
└── .quiz/
    ├── quiz.py            # Script Python du quiz
    ├── quiz/              # Dossier contenant les quiz JSON
    │   ├── bases_python.json
    │   ├── linux.json
    │   └── quiz.json
    └── resultats/         # Dossier pour stocker les résultats
        └── readme.md
```

## Désinstallation

Pour désinstaller le quiz :

```bash
# Supprimer le dossier d'installation
rm -rf ~/quiz

# Si vous avez créé un lien symbolique
sudo rm /usr/local/bin/quiz

# Si vous avez créé un alias, supprimez la ligne dans ~/.bashrc ou ~/.zshrc
```

## Dépannage

### Python3 non trouvé

Si vous obtenez l'erreur "Python3 n'est pas installé" :

**Sur Ubuntu/Debian :**
```bash
sudo apt update
sudo apt install python3
```

**Sur MacOS :**
```bash
brew install python3
```

### Erreur de téléchargement

Si le téléchargement échoue :
1. Vérifiez votre connexion internet
2. Vérifiez que l'URL GitHub est correcte
3. Vérifiez que le repository est public

### Permissions refusées

Si vous obtenez "Permission denied" :
```bash
chmod +x ~/quiz/quiz
```

## Support et contribution

Pour signaler un bug ou contribuer au projet, visitez le repository GitHub.
