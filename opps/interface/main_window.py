import qdarktheme
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from opps.interface.viewer_3d.render_widgets.common_render_widget import (
    CommonRenderWidget,
)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.configure_window()
        self.create_central_widget()

    def sizeHint(self) -> QSize:
        return QSize(800, 600)

    def configure_window(self):
        qdarktheme.setup_theme("dark")
        self.showMaximized()
        self.setWindowTitle("OPPS")

    def create_central_widget(self):
        self.render_widget = CommonRenderWidget()
        self.render_widget.set_theme("dark")
        self.setCentralWidget(self.render_widget)
