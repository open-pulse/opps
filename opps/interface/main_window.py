import qdarktheme
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import (
    QAction,
    QFileDialog,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from opps import app
from opps.interface.menus import ModeMenu, ProjectMenu
from opps.interface.viewer_3d.render_widgets.editor_render_widget import (
    EditorRenderWidget,
)
from opps.interface.widgets import AddStructuresWidget, EditStructuresWidget
from opps.interface.widgets.cross_section_widget import CrossSectionWidget
from opps.model import Pipe

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.floating_widget = None

        self.delete_action = QAction(self)
        self.delete_action.setShortcut("del")
        self.delete_action.triggered.connect(self.delete_selection_callback)
        self.addAction(self.delete_action)


        self._create_menu_bar()
        self._configure_window()
        self._create_central_widget()
        self.start_creation_mode()

        self.render_widget.selection_changed.connect(self.selection_callback)

    def open_dialog(self):
        path, check = QFileDialog.getOpenFileName(
            self,
            "Select Geometry",
            # filter="Piping Component File (*.pcf), Geometry Files (*.stp *.step *.iges)",
        )

        if not check:
            return

        app().geometry_toolbox.open(path)
        self.render_widget.update_plot()

    def save_dialog(self):
        if app().geometry_toolbox.save_path is None:
            self.save_as_dialog()
        else:
            app().geometry_toolbox.save(app().geometry_toolbox.save_path)

    def save_as_dialog(self):
        path, check = QFileDialog.getSaveFileName(
            self,
            "Save As",
            filter="Piping Component File (*.pcf), Geometry Files (*.stp *.step *.iges)",
        )

        if not check:
            return

        app().geometry_toolbox.save(path)

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
        editor = app().geometry_toolbox.editor
        self.render_widget = EditorRenderWidget(editor)
        self.render_widget.set_theme("dark")
        self.setCentralWidget(self.render_widget)

    def _create_periferic_widgets(self):
        pass

    def start_creation_mode(self):
        # If it is already in creation mode return
        if isinstance(self.floating_widget, AddStructuresWidget):
            if self.floating_widget.isVisible():
                return

        if self.floating_widget is not None:
            self.floating_widget.close()

        self.floating_widget = AddStructuresWidget(self.render_widget, self)
        self.floating_widget.show()

    def start_edition_mode(self):
        # If it is already in edition mode return
        if isinstance(self.floating_widget, EditStructuresWidget):
            if self.floating_widget.isVisible():
                return

        if self.floating_widget is not None:
            self.floating_widget.close()

        self.floating_widget = EditStructuresWidget(self.render_widget, self)
        self.floating_widget.show()

    def delete_selection_callback(self):
        editor = self.render_widget.editor
        editor.delete_selection()
        app().update()

    def selection_callback(self):
        if isinstance(self.floating_widget, AddStructuresWidget):
            if self.floating_widget.isVisible():
                return

        editor = self.render_widget.editor
        something_selected = editor.selected_points or editor.selected_structures
        if something_selected:
            self.start_edition_mode()
