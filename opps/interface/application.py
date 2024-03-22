from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication

from opps.interface.main_window import MainWindow
from opps.interface.toolboxes import GeometryToolbox


class Application(QApplication):
    selection_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry_toolbox = GeometryToolbox()


        self.main_window = MainWindow()
        self.main_window.show()

    def update(self):
        self.geometry_toolbox.update()
        self.main_window.render_widget.update_plot(reset_camera=False)
