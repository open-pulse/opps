from PyQt5.QtWidgets import QApplication
from opps.interface.main_window import MainWindow

from opps.model import Pipeline
from opps.model.pipeline_editor import PipelineEditor


class Application(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.pipeline = Pipeline()
        self.editor = PipelineEditor(self.pipeline)

        self.main_window = MainWindow()
        self.main_window.show()

    def new(self):
        self.pipeline = Pipeline()
        self.editor = PipelineEditor(self.pipeline)

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
