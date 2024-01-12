from pathlib import Path
from typing import Generator

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication

from opps.interface.main_window import MainWindow
from opps.model import Pipeline
from opps.model.pipeline_editor import PipelineEditor
from opps.model.point import Point
from opps.model.structure import Structure
from opps.io.cad_file.step_exporter import *



class Application(QApplication):
    selection_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.save_path = None

        self.selected_points_index = set()
        self.selected_structures_index = set()

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

    def _open_pcf(self, path):
        self.pipeline.load(path)
        self.update()
         
    def _save_cad(self, path):
        exporter = StepExporter()
        exporter.save(path, self.pipeline)
        print("Saving CAD")

    def _save_pcf(self, path):
        print("Saving PCF")

    def get_point(self, point_index) -> Point:
        return self.editor.points[point_index]

    def get_structure(self, structure_index) -> Structure:
        return self.pipeline.structures[structure_index]

    def get_selected_points(self) -> Generator[Point, None, None]:
        for index in self.selected_points_index:
            point = self.get_point(index)
            if isinstance(point, Point):
                yield point

    def get_selected_structures(self) -> Generator[Structure, None, None]:
        for index in self.selected_structures_index:
            structure = self.get_structure(index)
            if isinstance(structure, Structure):
                yield structure

    def delete_selection(self):
        for structure in self.get_selected_structures():
            self.editor.remove_structure(structure, rejoin=True)

        for point in self.get_selected_points():
            self.editor.remove_point(point, rejoin=False)

        self.clear_selection()
        self.update()

    def select_points(self, points_index, join=False, remove=False):
        points_index = set(points_index)

        if join and remove:
            self.selected_points_index ^= points_index
        elif join:
            self.selected_points_index |= points_index
        elif remove:
            self.selected_points_index -= points_index
        else:
            self.clear_selection()
            self.selected_points_index = points_index

        self.selection_changed.emit()

    def select_structures(self, structures_index, join=False, remove=False):
        structures_index = set(structures_index)

        # clear all the selected flags
        for structure in self.pipeline.structures:
            structure.selected = False

        # handle the selection according to modifiers like ctrl, shift, etc.
        if join and remove:
            self.selected_structures_index ^= structures_index
        elif join:
            self.selected_structures_index |= structures_index
        elif remove:
            self.selected_structures_index -= structures_index
        else:
            self.clear_selection()
            self.selected_structures_index = structures_index

        # apply the selection flag again for selected structures
        for index in self.selected_structures_index:
            structure = self.get_structure(index)
            structure.selected = True

        self.selection_changed.emit()

    def clear_selection(self):
        for structure in self.pipeline.structures:
            structure.selected = False
        self.selected_points_index.clear()
        self.selected_structures_index.clear()
        self.selection_changed.emit()

    def update(self):
        self.editor._update_joints()
        self.editor._update_points()
        self.main_window.render_widget.update_plot(reset_camera=False)
