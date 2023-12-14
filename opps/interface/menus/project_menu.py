from pathlib import Path

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QAction, QMenu

from opps import app


class ProjectMenu(QMenu):
    def __init__(self, parent):
        super().__init__(parent)
        #
        self.setTitle("Project")
        self.create_actions()
        self.create_layout()

    def create_actions(self):
        self.new_project_action = QAction("New Project")
        self.open_project_action = QAction("Open Project")
        self.save_project_action = QAction("Save")
        self.save_project_as_action = QAction("Save as")

        self.new_project_action.triggered.connect(self.new_project_callback)
        self.open_project_action.triggered.connect(self.open_project_callback)
        self.save_project_action.triggered.connect(self.save_project_callback)
        self.save_project_as_action.triggered.connect(self.save_project_as_callback)

    def create_layout(self):
        self.addAction(self.new_project_action)
        self.addAction(self.open_project_action)
        self.addAction(self.save_project_action)
        self.addAction(self.save_project_as_action)

    def new_project_callback(self):
        app().new()

    def open_project_callback(self):
        app().main_window.open_dialog()

    def save_project_callback(self):
        app().main_window.save_dialog()

    def save_project_as_callback(self):
        app().main_window.save_as_dialog()
