from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QAction,
    QCheckBox,
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

    def _define_qt_variables(self):
        self.teste = QAction("Connect", self)
        self.teste.setShortcut("ctrl+n")
        self.teste.triggered.connect(self.test_callback)
        self.addAction(self.teste)

        self.dx_box: QLineEdit
        self.dy_box: QLineEdit
        self.dz_box: QLineEdit

        self.bend_checkbox: QCheckBox

        self.section_button: QPushButton
        self.material_button: QPushButton
        self.apply_button: QPushButton

    def test_callback(self):
        pipeline = self.render_widget.pipeline

        pipeline.dismiss()
        pipes = pipeline.connect_i_beams()
        pipeline.commit()
        self.render_widget.update_plot()

    def _create_connections(self):
        self.dx_box.textEdited.connect(self.coords_modified_callback)
        self.dy_box.textEdited.connect(self.coords_modified_callback)
        self.dz_box.textEdited.connect(self.coords_modified_callback)
        self.section_button.clicked.connect(self.section_callback)
        self.bend_checkbox.stateChanged.connect(self.auto_bend_callback)
        self.apply_button.clicked.connect(self.apply_callback)
        self.render_widget.selection_changed.connect(self.selection_callback)

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

        auto_bend = self.bend_checkbox.isChecked()
        radius = 0.3 if auto_bend else 0
        pipeline = self.render_widget.pipeline

        pipeline.dismiss()
        pipeline.add_bent_pipe((dx, dy, dz), radius)
        self.render_widget.update_plot()

    def add_flange_callback(self):
        pass

    def section_callback(self):
        return

    def auto_bend_callback(self, checked):
        pipeline = self.render_widget.pipeline
        pipeline.dismiss()
        self.coords_modified_callback()

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
