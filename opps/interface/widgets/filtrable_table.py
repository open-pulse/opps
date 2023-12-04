from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class FiltrableTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.content = []
        self.filtered_content = self.content

    def set_header(self, header):
        header = list(header)
        self.setColumnCount(len(header))
        self.setHorizontalHeaderLabels(header)
        self.resizeColumnsToContents()
        self.update()

    def add_row(self, row):
        if len(row) != self.columnCount():
            raise ValueError("Invalid row size")
        self.content.append(row)

    def remove_row(self, row_index):
        value = self.content.pop(row_index)
        self.update()
        return value

    def filter(self, string):
        if not string:
            self.filtered_content = self.content
            self.update()
            return

        self.filtered_content = []
        for row in self.content:
            for val in row:
                if string in str(val):
                    self.filtered_content.append(row)
                    break

        self.update()

    def update(self):
        self.setRowCount(len(self.filtered_content))
        for i, row in enumerate(self.filtered_content):
            for j, val in enumerate(row):
                self.setItem(i, j, QTableWidgetItem(str(val)))
        self.resizeColumnsToContents()
        self.horizontalHeader().setSectionResizeMode(0)
        self.horizontalHeader().setStretchLastSection(True)