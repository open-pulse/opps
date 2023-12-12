from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt


from .filtrable_table import FiltrableTableWidget

from opps.properties import PipeCrossSection

# tmp structure
project_sections = [
    PipeCrossSection(0.1, 0.005),
    PipeCrossSection(0.2, 0.005),
    PipeCrossSection(0.5, 0.01),
    PipeCrossSection(1, 0.5),
    PipeCrossSection(2, 0.5),
    PipeCrossSection(5, 1),
]


class CrossSectionWidget(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure_window()

        self.selected_cross_section = None
        self.header = ["id", "Type", "Outside diameter (mm)", "Wall thickness (mm)"]

        self.text_filter = QLineEdit()
        self.text_filter.setPlaceholderText("Search a cross section.")

        self.table = FiltrableTableWidget()
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.set_header(self.header)

        for i, section in enumerate(project_sections):
            self.table.add_row([i, section.name(), section.diameter, section.thickness])
        self.table.update()

        self.apply_button = QPushButton("Apply")

        layout = QVBoxLayout()
        layout.addWidget(self.text_filter)
        layout.addWidget(self.table)
        layout.addWidget(self.apply_button)
        self.setLayout(layout)

        self.apply_button.clicked.connect(self.apply_callback)
        self.text_filter.textChanged.connect(self.table.filter)

    def apply_callback(self):
        if self.table.selectedIndexes():
            table_selected_content = self.table.filtered_content[self.table.currentRow()]
            sections_index = table_selected_content[0]  # index is in the first collumn
            self.selected_cross_section = project_sections[sections_index]
        self.close()

    def configure_window(self):
        self.setWindowTitle("Select Cross Section")
        self.setGeometry(300, 200, 700, 400)

        self.setWindowFlags(
            Qt.Window
            | Qt.CustomizeWindowHint
            | Qt.WindowTitleHint
            | Qt.WindowStaysOnTopHint
            | Qt.WindowCloseButtonHint
            | Qt.FramelessWindowHint
            | Qt.WindowShadeButtonHint
        )
