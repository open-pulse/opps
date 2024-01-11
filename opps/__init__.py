from PyQt5.QtWidgets import QApplication


def app() -> "Application":
    return QApplication.instance()
