import qdarktheme
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from opps.interface.viewer_3d.render_widgets.editor_render_widget import (
    EditorRenderWidget,
)
from opps.interface.widgets.add_structures_widget import AddStructuresWidget
from opps.model import Pipe


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.configure_window()
        self.create_central_widget()
        self.create_periferic_widgets()

    def sizeHint(self) -> QSize:
        return QSize(800, 600)

    def configure_window(self):
        qdarktheme.setup_theme("dark")
        self.showMaximized()
        self.setWindowTitle("OPPS")

    def create_central_widget(self):
        self.render_widget = EditorRenderWidget()
        self.render_widget.set_theme("dark")
        self.setCentralWidget(self.render_widget)

    def create_periferic_widgets(self):
        self.add_structures = AddStructuresWidget(self, self.render_widget)
        self.add_structures.show()

    def stage_structure_callback(self, dx, dy, dz):
        self.render_widget.stage_pipe_deltas(dx, dy, dz)

    def commit_structure_callback(self, *args, **kwargs):
        self.render_widget.commit_structure()
