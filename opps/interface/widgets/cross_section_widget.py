from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QAbstractItemView, QPushButton
from .filtrable_table import FiltrableTableWidget


class CrossSectionWidget(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.selected_cross_section = None
        self.header = ["shape", "diameter", "wall_thickness"]

        self.text_filter = QLineEdit()

        self.table = FiltrableTableWidget()
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.set_header(self.header)
        self.table.add_row([1,2,3])
        self.table.add_row([4,5,6])
        self.table.add_row([6,7,8])
        self.table.add_row([6,7,9])
        self.table.add_row([5,4,6])
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
        selected_rows_indexes = {i.row() for i in self.table.selectedIndexes()}
        if selected_rows_indexes:
            row_index, *_ = selected_rows_indexes
            
            self.selected_cross_section = {
                key:val for key, val 
                in zip(self.header, self.table.filtered_content[row_index])
            }
        self.close()