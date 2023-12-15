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


class EditStructuresWidget(QWidget):
    def __init__(self, parent, render_widget):
        super().__init__(parent)

        self.edit_pipe = EditPipeWidget()
        self.edit_bend = EditBendWidget()

        self.empty_text = QLabel("Select an object.")
        self.empty_text.setAlignment(Qt.AlignCenter)
        self.empty_text.setStyleSheet("QLabel { color: grey; }")

        layout = QStackedLayout()
        layout.addWidget(self.edit_bend)
        layout.addWidget(self.edit_pipe)
        layout.addWidget(self.empty_text)
        self.setLayout(layout)

        self.configure_window()

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
