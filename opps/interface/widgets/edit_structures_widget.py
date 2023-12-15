from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QStackedLayout,
    QWidget,
)

from opps.interface.widgets.edit_bend_widget import EditBendWidget
from opps.interface.widgets.edit_pipe_widget import EditPipeWidget
from opps.model import Bend, Pipe
from opps import app


class EditStructuresWidget(QWidget):
    def __init__(self, parent, render_widget):
        super().__init__(parent)

        self.edit_pipe_widget = EditPipeWidget()
        self.edit_bend_widget = EditBendWidget()

        self.empty_text_widget = QLabel("Select an object.")
        self.empty_text_widget.setAlignment(Qt.AlignCenter)
        self.empty_text_widget.setStyleSheet("QLabel { color: grey; }")

        layout = QStackedLayout()
        layout.addWidget(self.empty_text_widget)
        layout.addWidget(self.edit_bend_widget)
        layout.addWidget(self.edit_pipe_widget)
        self.setLayout(layout)

        self.configure_window()

        app().selection_changed.connect(self.selection_callback)

    def configure_window(self):
        self.setWindowTitle("Edition Mode")
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

    def selection_callback(self):
        layout: QStackedLayout = self.layout()

        if not app().selected_structures:
            layout.setCurrentWidget(self.empty_text_widget)
            return
        
        index, *_ = app().selected_structures
        structure = app().get_structure(index)
        
        if isinstance(structure, Pipe):
            layout.setCurrentWidget(self.edit_pipe_widget)
        elif isinstance(structure, Bend):
            layout.setCurrentWidget(self.edit_bend_widget)
        else:
            layout.setCurrentWidget(self.empty_text_widget)
