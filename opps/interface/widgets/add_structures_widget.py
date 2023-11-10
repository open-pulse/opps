from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel


class AddStructuresWidget(QWidget):
    # index_changed = pyqtSignal(int)
    # modified = pyqtSignal(float, float, float)
    # applied = pyqtSignal(float, float, float)
    on_close = pyqtSignal()

    def __init__(self, parent, render_widget):
        super().__init__(parent)
        self.configure_window()

        self.render_widget = render_widget

        self.index_box = QLineEdit()
        self.dx_box = QLineEdit()
        self.dy_box = QLineEdit()
        self.dz_box = QLineEdit()
        self.flange_button = QPushButton("Add Flange")
        self.apply_button = QPushButton("Apply")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("index"))
        layout.addWidget(self.index_box)
        layout.addWidget(QLabel("dx"))
        layout.addWidget(self.dx_box)
        layout.addWidget(QLabel("dy"))
        layout.addWidget(self.dy_box)
        layout.addWidget(QLabel("dz"))
        layout.addWidget(self.dz_box)
        layout.addWidget(self.flange_button)
        layout.addWidget(self.apply_button)
        self.setLayout(layout)

        self.index_box.textEdited.connect(self.index_changed_callback)
        self.dx_box.textEdited.connect(self.coords_modified_callback)
        self.dy_box.textEdited.connect(self.coords_modified_callback)
        self.dz_box.textEdited.connect(self.coords_modified_callback)
        self.flange_button.clicked.connect(self.add_flange_callback)
        self.apply_button.clicked.connect(self.apply_callback)

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

    def coords_modified_callback(self):
        dx, dy, dz = self.get_displacement()
        self.render_widget.stage_pipe_deltas(dx, dy, dz)
    
    def index_changed_callback(self):
        i = self.index_box.text()
        if not i:
            return
        self.render_widget.change_index(int(i))

    def add_flange_callback(self):
        self.render_widget.add_flange()
        self.coords_modified_callback()

    def apply_callback(self):
        dx, dy, dz = self.get_displacement()
        if (dx, dy, dz) == (0, 0, 0):
            return
        self.render_widget.commit_structure()
        self.coords_modified_callback()

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
