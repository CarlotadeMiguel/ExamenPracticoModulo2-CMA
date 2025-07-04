# backend/tests/conftest.py

import sys
import os

# Añade la carpeta 'backend/' (donde está tu paquete app) al inicio de sys.path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
