#!/bin/bash
# Script d'installation du Quiz Python
# Usage: ./install.sh <nom_du_quiz> [--dir <directory>]
#    ou: curl -sSL https://raw.githubusercontent.com/USER/REPO/main/install.sh | bash -s -- <nom_du_quiz>

set -e  # Arrêter en cas d'erreur

# Configuration
GITHUB_RAW_URL="https://raw.githubusercontent.com/fabrice1618/quiz_python/main"
DEFAULT_INSTALL_DIR="$HOME/quiz"
QUIZ_NAME=""
INSTALL_DIR="$DEFAULT_INSTALL_DIR"
INSTALL_ALL=false

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'affichage
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Fonction d'aide
show_help() {
    cat << EOF
Installation du Quiz Python

Usage:
    $0 <nom_du_quiz> [options]
    curl -sSL https://raw.githubusercontent.com/fabrice1618/quiz_python/main/install.sh | bash -s -- <nom_du_quiz>

Arguments:
    nom_du_quiz     Nom du quiz à installer (bases_python, linux, quiz)
                    ou --all pour installer tous les quiz

Options:
    --dir <path>    Répertoire d'installation (défaut: $DEFAULT_INSTALL_DIR)
    -h, --help      Afficher cette aide

Exemples:
    $0 bases_python
    $0 --all --dir ~/mes_quiz
    curl -sSL https://raw.githubusercontent.com/fabrice1618/quiz_python/main/install.sh | bash -s -- bases_python

Quiz disponibles:
    - bases_python : Quiz sur les bases de Python (100 questions)
    - linux        : Quiz sur Linux
    - quiz         : Quiz général
    - python50     : Quiz Python (50 questions)

EOF
}

# Parse des arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        --dir)
            INSTALL_DIR="$2"
            shift 2
            ;;
        --all)
            INSTALL_ALL=true
            shift
            ;;
        *)
            if [[ -z "$QUIZ_NAME" ]]; then
                QUIZ_NAME="$1"
            else
                print_error "Argument inconnu: $1"
                show_help
                exit 1
            fi
            shift
            ;;
    esac
done

# Vérification des paramètres
if [[ -z "$QUIZ_NAME" ]] && [[ "$INSTALL_ALL" == false ]]; then
    print_error "Vous devez spécifier un nom de quiz ou utiliser --all"
    echo ""
    show_help
    exit 1
fi

# Vérification de Python3
print_info "Vérification de Python3..."
if ! command -v python3 &> /dev/null; then
    print_error "Python3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
print_success "Python $PYTHON_VERSION détecté"

# Vérification de curl
if ! command -v curl &> /dev/null; then
    print_error "curl n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Création de la structure de dossiers
print_info "Création de la structure dans: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR/.quiz/quiz"
mkdir -p "$INSTALL_DIR/.quiz/resultats"

# Création de l'environnement virtuel
print_info "Création de l'environnement virtuel Python..."
if python3 -m venv "$INSTALL_DIR/.venv" 2>/dev/null; then
    print_success "Environnement virtuel créé"
else
    print_error "Impossible de créer l'environnement virtuel"
    print_warning "Vérifiez que python3-venv est installé: sudo apt install python3-venv"
    exit 1
fi

# Fonction de téléchargement
download_file() {
    local url="$1"
    local dest="$2"
    local description="$3"

    print_info "Téléchargement de $description..."
    if curl -sSL "$url" -o "$dest"; then
        print_success "$description téléchargé"
        return 0
    else
        print_error "Échec du téléchargement de $description"
        return 1
    fi
}

# Téléchargement du script principal
download_file "$GITHUB_RAW_URL/refactor/main.py" "$INSTALL_DIR/.quiz/main.py" "main.py"
chmod +x "$INSTALL_DIR/.quiz/main.py"

# Téléchargement des modules Python
download_file "$GITHUB_RAW_URL/refactor/quiz_data.py" "$INSTALL_DIR/.quiz/quiz_data.py" "quiz_data.py"
download_file "$GITHUB_RAW_URL/refactor/resultats_data.py" "$INSTALL_DIR/.quiz/resultats_data.py" "resultats_data.py"
download_file "$GITHUB_RAW_URL/refactor/config.py" "$INSTALL_DIR/.quiz/config.py" "config.py"
download_file "$GITHUB_RAW_URL/refactor/ui.py" "$INSTALL_DIR/.quiz/ui.py" "ui.py"
download_file "$GITHUB_RAW_URL/refactor/crypto.py" "$INSTALL_DIR/.quiz/crypto.py" "crypto.py"

# Téléchargement du fichier .env.example et création du .env
download_file "$GITHUB_RAW_URL/refactor/.env.example" "$INSTALL_DIR/.quiz/.env.example" ".env.example"
if [ ! -f "$INSTALL_DIR/.quiz/.env" ]; then
    cat > "$INSTALL_DIR/.quiz/.env" << ENVEOF
DATA_PATH=$INSTALL_DIR/.quiz
ENVEOF
    print_success "Fichier .env créé"
fi

# Création du fichier requirements.txt avec dépendances runtime uniquement
cat > "$INSTALL_DIR/requirements.txt" << 'REQEOF'
python-dotenv
REQEOF

# Installation des dépendances dans le venv
print_info "Installation des dépendances Python..."
if "$INSTALL_DIR/.venv/bin/pip" install --upgrade pip > /dev/null 2>&1 && \
   "$INSTALL_DIR/.venv/bin/pip" install -r "$INSTALL_DIR/requirements.txt" > /dev/null 2>&1; then
    print_success "Dépendances installées"
else
    print_error "Erreur lors de l'installation des dépendances"
    exit 1
fi

# Création du script wrapper
cat > "$INSTALL_DIR/quiz" << 'WRAPPEREOF'
#!/bin/bash
# Script de lancement du quiz Python

# Obtenir le répertoire du script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Lancer le script Python avec le venv
"$SCRIPT_DIR/.venv/bin/python3" "$SCRIPT_DIR/.quiz/main.py" "$@"
WRAPPEREOF
chmod +x "$INSTALL_DIR/quiz"

# Créer un README dans le dossier resultats
cat > "$INSTALL_DIR/.quiz/resultats/readme.md" << 'EOF'
# Dossier des résultats

Ce dossier contient les fichiers de résultats des quiz effectués.

Chaque fichier JSON contient :
- Le nom et prénom de l'utilisateur
- Les questions et les réponses correctes
- Le statut de chaque question (correcte ou non)
EOF

# Téléchargement des quiz
if [[ "$INSTALL_ALL" == true ]]; then
    print_info "Téléchargement de tous les quiz..."
    QUIZ_LIST=("bases_python" "linux" "quiz" "python50" "php50")
    for quiz in "${QUIZ_LIST[@]}"; do
        download_file "$GITHUB_RAW_URL/.quiz/quiz/${quiz}.json" "$INSTALL_DIR/.quiz/quiz/${quiz}.json" "${quiz}.json"
    done
else
    download_file "$GITHUB_RAW_URL/.quiz/quiz/${QUIZ_NAME}.json" "$INSTALL_DIR/.quiz/quiz/${QUIZ_NAME}.json" "${QUIZ_NAME}.json"
fi

# Création d'un lien symbolique optionnel dans /usr/local/bin (nécessite sudo)
echo ""
print_info "Installation terminée!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}Le quiz a été installé avec succès dans:${NC} $INSTALL_DIR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Pour utiliser le quiz:"
echo ""
echo "  1. Lancer le quiz par défaut:"
if [[ "$INSTALL_ALL" == true ]]; then
    echo "     cd $INSTALL_DIR && ./quiz -q bases_python"
else
    echo "     cd $INSTALL_DIR && ./quiz -q $QUIZ_NAME"
fi
echo ""
echo "  2. Lancer avec des options:"
echo "     cd $INSTALL_DIR && ./quiz -q $QUIZ_NAME -o mon_resultat"
echo ""
echo "  3. Reprendre un quiz existant:"
echo "     cd $INSTALL_DIR && ./quiz -r -o mon_resultat"
echo ""
echo "  4. Voir l'aide:"
echo "     cd $INSTALL_DIR && ./quiz --help"
echo ""
echo "Options pour créer un alias (optionnel):"
echo ""
echo "  # Ajouter dans ~/.bashrc ou ~/.zshrc:"
echo "  alias quiz='$INSTALL_DIR/quiz'"
echo ""
echo "  # Ou créer un lien symbolique (nécessite sudo):"
echo "  sudo ln -s $INSTALL_DIR/quiz /usr/local/bin/quiz"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exit 0
