import qdarktheme
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QVBoxLayout, QWidget

from opps import app
from opps.interface.menus import ProjectMenu, ModeMenu
from opps.interface.viewer_3d.render_widgets.editor_render_widget import (
    EditorRenderWidget,
)
from opps.interface.widgets import AddStructuresWidget, EditStructuresWidget
from opps.interface.widgets.cross_section_widget import CrossSectionWidget
from opps.model import Pipe
from opps.model.pipeline_editor import PipelineEditor

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.floating_widget = None

        self._create_menu_bar()
        self._configure_window()
        self._create_central_widget()
        self.start_creation_mode()

    def open_dialog(self):
        path, check = QFileDialog.getOpenFileName(
            self,
            "Select Geometry",
            filter="Piping Component File (*.pcf), Geometry Files (*.stp *.step *.iges)",
        )

        if not check:
            return
        
        app().open(path, PipelineEditor.pipeline)

    def save_dialog(self):
        if app().save_path is None:
            self.save_as_dialog()
        else:
            app().save(app().save_path)

    def save_as_dialog(self):
        path, check = QFileDialog.getSaveFileName(
            self,
            "Save As",
            filter="Piping Component File (*.pcf), Geometry Files (*.stp *.step *.iges)",
        )

        if not check:
            return

        app().save(path)
    
    def sizeHint(self) -> QSize:
        return QSize(800, 600)

    def _configure_window(self):
        qdarktheme.setup_theme("dark")
        self.showMaximized()
        self.setWindowTitle("OPPS")

    def _create_menu_bar(self):
        self.menu_bar = self.menuBar()
        self.menu_bar.addMenu(ProjectMenu(self))
        self.menu_bar.addMenu(ModeMenu(self))

    def _create_central_widget(self):
        self.render_widget = EditorRenderWidget()
        self.render_widget.set_theme("dark")
        self.setCentralWidget(self.render_widget)

    def _create_periferic_widgets(self):
        pass 

    def start_creation_mode(self):
        if self.floating_widget is not None:
            self.floating_widget.close()

        self.floating_widget = AddStructuresWidget(self, self.render_widget)
        self.floating_widget.show()

    def start_edition_mode(self):
        if self.floating_widget is not None:
            self.floating_widget.close()

        self.floating_widget = EditStructuresWidget(self, self.render_widget)
        self.floating_widget.show()
