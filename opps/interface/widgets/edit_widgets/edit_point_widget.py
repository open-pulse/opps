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

from opps import app
from opps.model import Point


class EditPointWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi(Path("data/ui_files/edit_point.ui"), self)
        self._define_qt_variables()
        self._create_connections()

    def update(self):
        super().update()
        *_, point = app().get_selected_points()
        if point is None:
            return
        self.dx_box.setText(str(point.x))
        self.dy_box.setText(str(point.y))
        self.dz_box.setText(str(point.z))

    def _define_qt_variables(self):
        self.dx_box: QLineEdit = self.findChild(QLineEdit, "dx_box")
        self.dy_box: QLineEdit = self.findChild(QLineEdit, "dy_box")
        self.dz_box: QLineEdit = self.findChild(QLineEdit, "dz_box")
        self.flange_button: QPushButton = self.findChild(QPushButton, "flange_button")
        self.bend_button: QPushButton = self.findChild(QPushButton, "bend_button")
        self.elbow_button: QPushButton = self.findChild(QPushButton, "elbow_button")

    def _create_connections(self):
        self.dx_box.textEdited.connect(self.position_edited_callback)
        self.dy_box.textEdited.connect(self.position_edited_callback)
        self.dz_box.textEdited.connect(self.position_edited_callback)
        self.flange_button.clicked.connect(self.flange_callback)
        self.bend_button.clicked.connect(self.bend_callback)
        self.elbow_button.clicked.connect(self.elbow_callback)

    def get_position(self):
        dx = self.dx_box.text()
        dy = self.dy_box.text()
        dz = self.dz_box.text()
        dx = float(dx)
        dy = float(dy)
        dz = float(dz)
        return dx, dy, dz

    def position_edited_callback(self):
        *_, point = app().get_selected_points()
        if point is None:
            return

        try:
            x, y, z = self.get_position()
        except ValueError:
            return

        point.set_coords(x, y, z)
        app().update()

    def flange_callback(self):
        print("flange")

    def bend_callback(self):
        print("bend")

    def elbow_callback(self):
        print("elbow")
