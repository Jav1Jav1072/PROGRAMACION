# tests/conftest.py
import sys
from pathlib import Path

# Carpeta raíz del proyecto (una por encima de /tests)
ROOT = Path(__file__).resolve().parent.parent

# Carpeta /src
SRC = ROOT / "src"

# Añadimos /src al path de Python
sys.path.insert(0, str(SRC))
