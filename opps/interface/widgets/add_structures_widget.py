from functools import partial
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QAction,
    QCheckBox,
    QComboBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from opps import UI_DIR, app
from opps.interface.viewer_3d.render_widgets.editor_render_widget import (
    EditorRenderWidget,
)


class AddStructuresWidget(QWidget):
    # index_changed = pyqtSignal(int)
    # modified = pyqtSignal(float, float, float)
    # applied = pyqtSignal(float, float, float)
    on_close = pyqtSignal()

    def __init__(self, render_widget: EditorRenderWidget, parent):
        super().__init__(parent)
        uic.loadUi(UI_DIR / "add_structure.ui", self)

        self.render_widget = render_widget
        self.render_widget.show_passive_points = False

        self.configure_window()
        self._define_qt_variables()
        self._create_connections()

        self.structure_combobox_callback(self.structure_combobox.currentText())

    def _define_qt_variables(self):
        self.dx_box: QLineEdit
        self.dy_box: QLineEdit
        self.dz_box: QLineEdit

        self.structure_combobox: QComboBox
        self.connect_button: QPushButton

        self.section_button: QPushButton
        self.material_button: QPushButton
        self.apply_button: QPushButton

    def _create_connections(self):
        self.dx_box.textEdited.connect(self.coords_modified_callback)
        self.dy_box.textEdited.connect(self.coords_modified_callback)
        self.dz_box.textEdited.connect(self.coords_modified_callback)
        self.structure_combobox.currentTextChanged.connect(self.structure_combobox_callback)
        self.connect_button.clicked.connect(self.connect_selection_callback)
        self.section_button.clicked.connect(self.section_callback)
        self.apply_button.clicked.connect(self.apply_callback)
        self.render_widget.selection_changed.connect(self.selection_callback)

    def structure_combobox_callback(self, text: str):
        pipeline = self.render_widget.pipeline

        text = text.lower().strip()

        if text == "pipe":
            self.current_add_function = pipeline.add_pipe
            self.current_connect_function = pipeline.connect_pipes

        elif text == "pipe + bend":
            self.current_add_function = partial(pipeline.add_bent_pipe, curvature_radius=0.3)
            self.current_connect_function = partial(
                pipeline.connect_bent_pipes, curvature_radius=0.3
            )

        elif text == "flange":
            self.current_add_function = pipeline.add_flange
            self.current_connect_function = pipeline.connect_flanges

        elif text == "valve":
            self.current_add_function = pipeline.add_valve
            self.current_connect_function = pipeline.connect_valves

        elif text == "expansion joint":
            self.current_add_function = pipeline.add_expansion_joint
            self.current_connect_function = pipeline.connect_expansion_joints

        elif text == "reducer":
            self.current_add_function = pipeline.add_reducer_eccentric
            self.current_connect_function = pipeline.connect_reducer_eccentrics

        elif text == "circular beam":
            self.current_add_function = pipeline.add_circular_beam
            self.current_connect_function = pipeline.connect_circular_beams

        elif text == "rectangular beam":
            self.current_add_function = pipeline.add_rectangular_beam
            self.current_connect_function = pipeline.connect_rectangular_beams

        elif text == "i beam":
            self.current_add_function = pipeline.add_i_beam
            self.current_connect_function = pipeline.connect_i_beams

        elif text == "t beam":
            self.current_add_function = pipeline.add_t_beam
            self.current_connect_function = pipeline.connect_t_beams

        elif text == "c beam":
            self.current_add_function = pipeline.add_c_beam
            self.current_connect_function = pipeline.connect_c_beams

        else:
            self.current_add_function = None
            self.current_connect_function = None

        if pipeline.staged_structures:
            self.coords_modified_callback()

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
        except ValueError:
            return

        pipeline = self.render_widget.pipeline
        pipeline.dismiss()

        if callable(self.current_add_function):
            self.current_add_function((dx, dy, dz))

        self.render_widget.update_plot()

    def connect_selection_callback(self):
        pipeline = self.render_widget.pipeline
        pipeline.dismiss()
        if callable(self.current_connect_function):
            self.current_connect_function()
        pipeline.commit()
        self.render_widget.update_plot()

    def add_flange_callback(self):
        pass

    def section_callback(self):
        pipeline = self.render_widget.pipeline
        pipeline.dismiss()
        pipeline.divide_structures_evenly(1)
        pipeline.clear_selection()
        self.render_widget.update_plot(reset_camera=False)

    def apply_callback(self):
        try:
            dx, dy, dz = self.get_displacement()
        except ValueError:
            return

        if (dx, dy, dz) == (0, 0, 0):
            return

        pipeline = self.render_widget.pipeline
        pipeline.commit()
        self.coords_modified_callback()

    def configure_window(self):
        self.setGeometry(200, 200, 400, 400)

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
        self.render_widget.pipeline.dismiss()
        return super().closeEvent(a0)

    def selection_callback(self):
        points = list(app().geometry_toolbox.get_selected_points())
        if not points:
            return

        *_, last_point = points
        enable = last_point in app().geometry_toolbox.pipeline.control_points
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
