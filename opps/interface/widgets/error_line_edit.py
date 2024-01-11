import re

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFrame, QLabel, QLineEdit, QVBoxLayout


class ErrorLineEdit(QFrame):
    def __init__(self, title="", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.error_color = QColor(224, 73, 70)
        self.title_label = QLabel(title)
        self.line_edit = QLineEdit()
        self.error_label = QLabel()
        self.error_label.setStyleSheet(f"color: {self.error_color.name()}")

        self.error_checks = []

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.error_label)
        self.setLayout(layout)

    def text(self) -> str:
        return self.line_edit.text()

    def validate(self):
        text = self.line_edit.text()
        for validator, error_message in self.error_checks:
            if not validator(text):
                self.error_label.setText(error_message)
                self.line_edit.setStyleSheet(f"border: 0.5px solid {self.error_color.name()};")
                return False
        self.error_label.setText("")
        self.line_edit.setStyleSheet("border: 0px solid None")
        return True

    def add_error_check(self, validator, error_message):
        self.error_checks.append((validator, error_message))

    def add_regex_check(self, regex, error_message):
        validator = re.compile(regex).match
        self.add_error_check(validator, error_message)
