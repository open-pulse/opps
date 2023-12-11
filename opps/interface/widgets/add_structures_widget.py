from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QLabel,
    QFrame,
    QLineEdit,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QCheckBox,
)
from .cross_section_widget import CrossSectionWidget

class AddStructuresWidget(QWidget):
    # index_changed = pyqtSignal(int)
    # modified = pyqtSignal(float, float, float)
    # applied = pyqtSignal(float, float, float)
    on_close = pyqtSignal()

    def __init__(self, parent, render_widget):
        super().__init__(parent)
        self.configure_window()

        self.render_widget = render_widget

        self.dx_box = QLineEdit()
        self.dy_box = QLineEdit()
        self.dz_box = QLineEdit()

        self.section_button = QPushButton("Default Section")
        self.material_button = QPushButton("Default Material")
        self.apply_button = QPushButton("Apply")
        self.apply_button.setShortcut("ctrl+return")
        
        self.bend_checkbox = QCheckBox("Automatic Bending")
        self.elbow_checkbox = QCheckBox("Elbow")
        self.flange_checkbox = QCheckBox("Flange")
        self.bend_checkbox.setChecked(True)

        deltas_layout = QGridLayout()
        deltas_layout.addWidget(QLabel("ΔX"), 0, 0)
        deltas_layout.addWidget(self.dx_box, 0, 1)
        deltas_layout.addWidget(QLabel("ΔY"), 1, 0)
        deltas_layout.addWidget(self.dy_box, 1, 1)
        deltas_layout.addWidget(QLabel("ΔZ"), 2, 0)
        deltas_layout.addWidget(self.dz_box, 2, 1)

        config_pipes_layout = QHBoxLayout()
        config_pipes_layout.addWidget(self.section_button)
        config_pipes_layout.addWidget(self.material_button)

        acessories_layout = QVBoxLayout()
        acessories_layout.addWidget(self.bend_checkbox)
        # acessories_layout.addWidget(self.elbow_checkbox)
        # acessories_layout.addWidget(self.flange_checkbox)

        layout = QVBoxLayout()
        layout.addLayout(deltas_layout)
        layout.addLayout(acessories_layout)
        layout.addLayout(config_pipes_layout)
        # layout.addStretch()
        layout.addWidget(self.apply_button)
        layout.setSpacing(20)
        self.setLayout(layout)

        self.dx_box.textEdited.connect(self.coords_modified_callback)
        self.dy_box.textEdited.connect(self.coords_modified_callback)
        self.dz_box.textEdited.connect(self.coords_modified_callback)
        self.section_button.clicked.connect(self.section_callback)
        self.bend_checkbox.stateChanged.connect(self.auto_bend_callback)
        self.apply_button.clicked.connect(self.apply_callback)

    def get_displacement(self):
        dx = self.dx_box.text() or 0
        dy = self.dy_box.text() or 0
        dz = self.dz_box.text() or 0
        dx = float(dx)
        dy = float(dy)
        dz = float(dz)
        return dx, dy, dz

    def coords_modified_callback(self):
        try:
            dx, dy, dz = self.get_displacement()
            auto_bend = self.bend_checkbox.isChecked()
            self.render_widget.stage_pipe_deltas(dx, dy, dz, auto_bend)
        except ValueError:
            pass

    def add_flange_callback(self):
        self.render_widget.add_flange()
        self.coords_modified_callback()

    def section_callback(self):
        bla = CrossSectionWidget()
        bla.exec()

        if bla.selected_cross_section is not None:
            diameter = bla.selected_cross_section["diameter"]
            self.render_widget.update_diameter(diameter)

    def auto_bend_callback(self, checked):
        self.render_widget.unstage_structure()
        self.coords_modified_callback()

    def apply_callback(self):
        dx, dy, dz = self.get_displacement()
        if (dx, dy, dz) == (0, 0, 0):
            return
        self.render_widget.commit_structure()
        self.coords_modified_callback()

    def configure_window(self):
        self.setWindowTitle("Add Structures")
        self.setGeometry(200, 200, 400, 400)

        self.setWindowFlags(
            Qt.Window
            | Qt.CustomizeWindowHint
            | Qt.WindowTitleHint
            | Qt.WindowCloseButtonHint
            | Qt.FramelessWindowHint
            | Qt.WindowShadeButtonHint
        )

    def closeEvent(self, a0) -> None:
        self.render_widget.unstage_structure()
        return super().closeEvent(a0)

    def separator(self):
        s = QFrame()
        s.setFrameShape(QFrame.Shape.HLine)
        s.setFrameShadow(QFrame.Shadow.Sunken)
        return s
