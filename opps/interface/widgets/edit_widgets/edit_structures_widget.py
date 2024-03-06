from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from opps import app
from opps.interface.widgets.edit_widgets import (
    EditBendWidget,
    EditPipeWidget,
    EditPointWidget,
)
from opps.model import Bend, Pipe


class EditStructuresWidget(QWidget):
    def __init__(self, render_widget, parent):
        super().__init__(parent)

        self.render_widget = render_widget
        self.render_widget.show_passive_points = True

        self.edit_pipe_widget = EditPipeWidget(self.render_widget, self)
        self.edit_bend_widget = EditBendWidget(self.render_widget, self)
        self.edit_point_widget = EditPointWidget(self.render_widget, self)

        self.empty_text_widget = QLabel("Select an object.")
        self.empty_text_widget.setAlignment(Qt.AlignCenter)
        self.empty_text_widget.setStyleSheet("QLabel { color: grey; }")

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.addWidget(self.empty_text_widget)
        self.stacked_layout.addWidget(self.edit_bend_widget)
        self.stacked_layout.addWidget(self.edit_pipe_widget)
        self.stacked_layout.addWidget(self.edit_point_widget)
        self.setLayout(self.stacked_layout)

        self.configure_window()

        self.render_widget.selection_changed.connect(self.selection_callback)
        self.selection_callback()

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
        editor = self.render_widget.editor

        if editor.selected_structures:
            self._structures_selection_callback()
        elif editor.selected_points:
            self.stacked_layout.setCurrentWidget(self.edit_point_widget)
        else:
            self.stacked_layout.setCurrentWidget(self.empty_text_widget)

        self.stacked_layout.currentWidget().update()

    def _structures_selection_callback(self):
        editor = self.render_widget.editor

        structure, *_ = editor.selected_structures

        if isinstance(structure, Pipe):
            self.stacked_layout.setCurrentWidget(self.edit_pipe_widget)
        elif isinstance(structure, Bend):
            self.stacked_layout.setCurrentWidget(self.edit_bend_widget)
        else:
            self.stacked_layout.setCurrentWidget(self.empty_text_widget)
