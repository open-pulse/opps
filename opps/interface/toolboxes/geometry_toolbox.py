from PyQt5.QtCore import QObject, pyqtSignal
from opps.model import Pipeline

from pathlib import Path
from typing import Generator

from PyQt5.QtCore import pyqtSignal

from opps.io.cad_file.cad_handler import *
from opps.model import Pipeline
from opps.model import Structure, Point
from opps.io.cad_file.step_handler import StepHandler
from opps.io.pcf.pcf_handler import PCFHandler
from opps.io.pcf.pcf_exporter import PCFExporter
from opps.interface import main_window
from opps.model import RectangularBeam


class GeometryToolbox(QObject):
    selection_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.save_path = None

        self.selected_points = set()
        self.selected_structures = set()

        self.pipeline = Pipeline()

    def new(self):
        self.pipeline.structures.clear()
        self.update()

    def open(self, path):
        path = Path(path)
        file_format = path.suffix.lower().strip()

        if file_format == ".pcf":
            self._open_pcf(path)
        else:
            self._open_cad(path)
        
        # self.editor.merge_coincident_points()

    def save(self, path):
        path = Path(path)
        self.save_path = path
        file_format = path.suffix.lower().strip()

        if file_format == ".pcf":
            self._save_pcf(path)
        else:
            self._save_cad(path)

    def _open_cad(self, path):
        StepHandler().open(path, self.editor)
        self.update()

    def _open_pcf(self, path):
        self.pcf_handler = PCFHandler()
        self.pcf_handler.load(path,self.pipeline)
        self.update()

    def _save_cad(self, path):
        step_handler = StepHandler()
        step_handler.save(path, self.editor)

    def _save_pcf(self, path):
        self.pcf_exporter = PCFExporter()
        self.pcf_exporter.save(path,self.pipeline)

    def get_point(self, point_index) -> Point:
        return self.pipeline.points[point_index]

    def get_structure(self, structure_index) -> Structure:
        return self.pipeline.structures[structure_index]

    def get_selected_points(self) -> Generator[Point, None, None]:
        return self.selected_points

    def get_selected_structures(self) -> Generator[Structure, None, None]:
        return self.selected_structures

    def delete_selection(self):
        return 
        for structure in self.get_selected_structures():
            self.editor.remove_structure(structure, rejoin=True)

        for point in self.get_selected_points():
            self.editor.remove_point(point, rejoin=False)

        self.clear_selection()
        self.update()

    # def select_points(self, points, join=False, remove=False):
    #     points = set(points)

    #     if join and remove:
    #         self.selected_points ^= points
    #     elif join:
    #         self.selected_points |= points
    #     elif remove:
    #         self.selected_points -= points
    #     else:
    #         self.clear_selection()
    #         self.selected_points = points

    #     self.selection_changed.emit()

    # def select_structures(self, structures, join=False, remove=False):
    #     structures = set(structures)

    #     # clear all the selected flags
    #     for structure in self.pipeline.structures:
    #         structure.selected = False

    #     # handle the selection according to modifiers like ctrl, shift, etc.
    #     if join and remove:
    #         self.selected_structures ^= structures
    #     elif join:
    #         self.selected_structures |= structures
    #     elif remove:
    #         self.selected_structures -= structures
    #     else:
    #         self.clear_selection()
    #         self.selected_structures = structures

    #     # apply the selection flag again for selected structures
    #     for structure in self.selected_structures:
    #         structure.selected = True

    #     self.selection_changed.emit()

    # def clear_selection(self):
    #     for structure in self.pipeline.structures:
    #         structure.selected = False
    #     self.selected_points.clear()
    #     self.selected_structures.clear()
    #     self.selection_changed.emit()

    def update(self):
        return
        self.editor.update()
