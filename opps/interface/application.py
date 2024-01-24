from pathlib import Path

from PyQt5.QtWidgets import QApplication

from opps.interface.main_window import MainWindow
from opps.model import Pipeline
from opps.model.pipeline_editor import PipelineEditor
from opps.io.cad_file.step_handler import StepHandler



class Application(QApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.save_path = None

        self.pipeline = Pipeline()
        self.editor = PipelineEditor(self.pipeline)

        self.main_window = MainWindow()
        self.main_window.show()

    def new(self):
        self.pipeline = Pipeline()
        self.editor = PipelineEditor(self.pipeline)
        self.main_window.render_widget.update_plot()

    def open(self, path):
        path = Path(path)
        file_format = path.suffix.lower().strip()

        if file_format == ".pcf":
            self._open_pcf(path)
        else:
            self._open_cad(path)

    def save(self, path):
        path = Path(path)
        self.save_path = path
        file_format = path.suffix.lower().strip()

        if file_format == ".pcf":
            self._save_pcf(path)
        else:
            self._save_cad(path)

    def _open_cad(self, path):
        print("Oppening CAD")
        StepHandler.open(self, path)

    def _open_pcf(self, path):
        print("Oppening PCF")

    def _save_cad(self, path):
        StepHandler.save(path, self.pipeline)
        print("Saving CAD")

    def _save_pcf(self, path):
        print("Saving PCF")
