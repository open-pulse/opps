from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from opps import UI_DIR


class EditPipeWidget(QWidget):
    def __init__(self, render_widget, parent):
        super().__init__(parent)
        uic.loadUi(UI_DIR / "edit_pipe.ui", self)
