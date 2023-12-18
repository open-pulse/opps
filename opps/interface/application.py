from pathlib import Path

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import pyqtSignal


from opps.interface.main_window import MainWindow
from opps.model import Pipeline
from opps.model.pipeline_editor import PipelineEditor


class Application(QApplication):
    selection_changed = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.save_path = None

        self.selected_points = set()
        self.selected_structures = set()

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
        print("Oppening PCF")

    def _save_cad(self, path):
        print("Saving CAD")

    def _save_pcf(self, path):
        print("Saving PCF")

    def get_point(self, point_index):
        return self.editor.control_points[point_index]

    def get_structure(self, structure_index):
        return self.pipeline.components[structure_index]
    
    def get_selected_point(self):
        if not self.selected_points:
            return
        first_index, *_ = self.selected_points
        return self.get_point(first_index)
    
    def get_selected_structure(self):
        if not self.selected_structures:
            return
        first_index, *_ = self.selected_structures
        return self.get_structure(first_index)

    def delete_selection(self):
        structures = [self.get_structure(i) for i in self.selected_structures]
        for structure in structures:
            self.editor.remove_structure(structure, rejoin=False)
        self.update()

    def select_points(self, points):
        self.clear_selection()
        self.selected_points |= set(points)
        self.selection_changed.emit()

    def select_structures(self, structures):
        self.clear_selection()
        self.selected_structures |= set(structures)
        self.selection_changed.emit()
    
    def clear_selection(self):
        self.selected_points.clear()
        self.selected_structures.clear()
        self.selection_changed.emit()

    def update(self):
        self.editor._update_joints()
        self.editor._update_control_points()
        self.main_window.render_widget.update_plot()
