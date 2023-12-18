from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QStackedLayout,
    QWidget,
)
from PyQt5 import uic
from pathlib import Path

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
        point = app().get_selected_point()
        if point is None:
            return
        self.dx_box.setText(str(point.x))
        self.dy_box.setText(str(point.y))
        self.dz_box.setText(str(point.z))

    def _create_connections(self):
        self.dx_box.textEdited.connect(self.position_edited_callback)
        self.dy_box.textEdited.connect(self.position_edited_callback)
        self.dz_box.textEdited.connect(self.position_edited_callback)

    def _define_qt_variables(self):
        self.dx_box: QLineEdit = self.findChild(QLineEdit, "dx_box")
        self.dy_box: QLineEdit = self.findChild(QLineEdit, "dy_box")
        self.dz_box: QLineEdit = self.findChild(QLineEdit, "dz_box")

    def get_position(self):
        dx = self.dx_box.text()
        dy = self.dy_box.text()
        dz = self.dz_box.text()
        dx = float(dx)
        dy = float(dy)
        dz = float(dz)
        return dx, dy, dz

    def position_edited_callback(self):
        point: Point = app().get_selected_point()
        if point is None:
            return

        try:
            x, y, z = self.get_position()
        except ValueError:
            return

        point.set_coords(x, y, z)
        app().update()