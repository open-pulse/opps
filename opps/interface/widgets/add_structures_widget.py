from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal


class AddStructuresWidget(QWidget):
    modified = pyqtSignal(float, float, float)
    applied = pyqtSignal(float, float, float)
    on_close = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.configure_window()

        self.dx_box = QLineEdit()
        self.dy_box = QLineEdit()
        self.dz_box = QLineEdit()
        self.apply_button = QPushButton("Apply")

        layout = QVBoxLayout()
        layout.addWidget(self.dx_box)
        layout.addWidget(self.dy_box)
        layout.addWidget(self.dz_box)
        layout.addWidget(self.apply_button)
        self.setLayout(layout)

        self.dx_box.textEdited.connect(self.modify_callback)
        self.dy_box.textEdited.connect(self.modify_callback)
        self.dz_box.textEdited.connect(self.modify_callback)
        self.apply_button.clicked.connect(self.apply_callback)
        self.apply_button.clicked.connect(self.modify_callback)

    def get_displacement(self):
        try:
            dx = self.dx_box.text() or 0
            dy = self.dy_box.text() or 0
            dz = self.dz_box.text() or 0
            dx = float(dx)
            dy = float(dy)
            dz = float(dz)
        except ValueError:
            dx, dy, dz = 0, 0, 0
        return dx, dy, dz

    def modify_callback(self):
        dx, dy, dz = self.get_displacement()
        self.modified.emit(dx, dy, dz)

    def apply_callback(self):
        dx, dy, dz = self.get_displacement()
        if (dx, dy, dz) == (0,0,0):
            return
        self.applied.emit(dx, dy, dz)

    def configure_window(self):
        self.setWindowTitle("Add Structures")
        self.setGeometry(200, 200, 400, 350)

        self.setWindowFlags(
            Qt.Window
            | Qt.CustomizeWindowHint
            | Qt.WindowTitleHint
            | Qt.WindowStaysOnTopHint
            | Qt.WindowCloseButtonHint
            | Qt.FramelessWindowHint
            | Qt.WindowShadeButtonHint
        )

    def closeEvent(self, a0) -> None:
        self.on_close.emit()
        return super().closeEvent(a0)