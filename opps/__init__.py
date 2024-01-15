from PyQt5.QtWidgets import QApplication
from pathlib import Path


ROOT_DIR = Path(__file__).parent
UI_DIR = ROOT_DIR / "interface/ui_files"

def app() -> "Application":
    return QApplication.instance()

