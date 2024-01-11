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
    QWidget,
)


class EditStructuresWidget(QWidget):
    def __init__(self, parent, render_widget):
        super().__init__(parent)
        self.configure_window()

        empty_text = QLabel("Select an object.")
        empty_text.setAlignment(Qt.AlignCenter)
        empty_text.setStyleSheet("QLabel { color: grey; }")

        layout = QVBoxLayout()
        layout.addWidget(empty_text)
        self.setLayout(layout)

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
