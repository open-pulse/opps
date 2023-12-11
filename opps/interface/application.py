from PyQt5.QtWidgets import QApplication
from opps.interface.main_window import MainWindow

from opps.model import Pipeline
from opps.model.pipeline_editor import PipelineEditor


class Application(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pipeline = Pipeline()
        self.editor = PipelineEditor(self.pipeline)

        self.window = MainWindow()
        self.window.show()

    def open(self, path):
        pass

    def save(self, path):
        pass

    def _open_cad(self, path):
        pass

    def _open_pcf(self, path):
        pass

    def _save_cad(self, path):
        pass

    def _save_pcf(self, path):
        pass
