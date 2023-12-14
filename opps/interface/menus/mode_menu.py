from pathlib import Path

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QMenu

from opps import app


class ModeMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        #
        self.setTitle("Mode")
        self.create_actions()
        self.create_layout()

    def create_actions(self):
        self.creation_mode_action = QAction("Creation Mode")
        self.edition_mode_action = QAction("Edition Mode")
        self.creation_mode_action.triggered.connect(self.creation_mode_callback)
        self.edition_mode_action.triggered.connect(self.edition_mode_callback)

    def create_layout(self):
        self.addAction(self.creation_mode_action)
        self.addAction(self.edition_mode_action)

    def creation_mode_callback(self):
        app().main_window.start_creation_mode()

    def edition_mode_callback(self):
        app().main_window.start_edition_mode()
