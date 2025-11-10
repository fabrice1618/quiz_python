"""
Configuration
"""

import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()  # charge .env depuis le répertoire courant (ou parent)
data_path: Path = Path(os.getenv("DATA_PATH", "."))

QUIZ_PATH = "quiz"
RESULT_PATH = "resultats"
