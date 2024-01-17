from pathlib import Path
from typing import Generator

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication

from opps.interface.main_window import MainWindow
from opps.interface.toolboxes import GeometryToolbox
from opps.io.cad_file.cad_handler import *
from opps.model import Pipeline
from opps.model.pipeline_editor import PipelineEditor
from opps.model.point import Point
from opps.model.structure import Structure

class Application(QApplication):
    selection_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.geometry_toolbox = GeometryToolbox()

        self.main_window = MainWindow()
        self.main_window.show()

    def update(self):
        self.geometry_toolbox.update()
        self.main_window.render_widget.update_plot(reset_camera=False)
