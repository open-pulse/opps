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

from opps import UI_DIR, app
from opps.model import Point


class EditPointWidget(QWidget):
    def __init__(self, render_widget, parent):
        super().__init__(parent)
        uic.loadUi(UI_DIR / "edit_point.ui", self)

        self.render_widget = render_widget

        self._define_qt_variables()
        self._create_connections()

    def update(self):
        super().update()

        pipeline = self.render_widget.pipeline
        if not pipeline.selected_points:
            return

        *_, last_point = pipeline.selected_points
        if not isinstance(last_point, Point):
            return

        self.dx_box.setText(str(round(last_point.x, 3)))
        self.dy_box.setText(str(round(last_point.y, 3)))
        self.dz_box.setText(str(round(last_point.z, 3)))

        enable = last_point in pipeline.points
        self.dx_box.setEnabled(enable)
        self.dy_box.setEnabled(enable)
        self.dz_box.setEnabled(enable)

        if enable:
            text = ""
        else:
            text = "Invalid point"

        self.dx_box.setPlaceholderText(text)
        self.dy_box.setPlaceholderText(text)
        self.dz_box.setPlaceholderText(text)

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
        pipeline = self.render_widget.pipeline
        if not pipeline.selected_points:
            return

        *_, last_point = pipeline.selected_points
        if not isinstance(last_point, Point):
            return

        try:
            x, y, z = self.get_position()
        except ValueError:
            return

        pipeline.move_point(last_point, (x, y, z))
        app().update()

    def flange_callback(self):
        pipeline = self.render_widget.pipeline
        pipeline.add_flange()
        pipeline.commit()
        pipeline.clear_selection()
        app().update()

    def bend_callback(self):
        pipeline = self.render_widget.pipeline
        pipeline.add_bend(0.3)
        pipeline.commit()
        pipeline.clear_selection()
        app().update()

    def elbow_callback(self):
        pipeline = self.render_widget.pipeline
        pipeline.add_elbow()
        pipeline.commit()
        pipeline.clear_selection()
        app().update()
