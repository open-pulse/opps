from dataclasses import dataclass
from enum import Enum

import numpy as np
import vtk
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication

from opps.interface.viewer_3d.actors import ControlPointsActor, PassivePointsActor, SelectedPointsActor
from opps.model import Flange, Pipe, Pipeline
from opps.model.pipeline_editor import PipelineEditor

from vtkat.render_widgets import CommonRenderWidget


class EditorRenderWidget(CommonRenderWidget):
    selection_changed = pyqtSignal()

    def __init__(self, editor, parent=None):
        super().__init__(parent)
        self.left_released.connect(self.selection_callback)
        self.editor = editor

        self.selected_structure = None
        self.pipeline_actor = None
        self.control_points_actor = None
        self.passive_points_actor = None
        self.selected_points_actor = None
        self.coords = np.array([0, 0, 0])

        self.create_axes()
        self.update_plot()

    def update_plot(self, reset_camera=True):
        self.remove_actors()

        pipeline = self.editor.pipeline

        self.pipeline_actor = pipeline.as_vtk()
        self.control_points_actor = ControlPointsActor(pipeline.control_points)
        self.passive_points_actor = PassivePointsActor(pipeline.points)
        self.selected_points_actor = SelectedPointsActor(self.editor.selected_points)

        # The order matters. It defines wich points will appear first.
        self.renderer.AddActor(self.pipeline_actor)
        self.renderer.AddActor(self.passive_points_actor)
        self.renderer.AddActor(self.control_points_actor)
        self.renderer.AddActor(self.selected_points_actor)

        if reset_camera:
            self.renderer.ResetCamera()
        self.update()

    def change_anchor(self, point):
        self.editor.dismiss()
        self.editor.set_anchor(point)
        self.coords = point.coords()
        self.update_plot(reset_camera=False)

    def stage_pipe_deltas(self, dx, dy, dz, auto_bend=True):
        self.editor.dismiss()
        self.editor.clear_selection()
        radius = 0.3 if auto_bend else 0
        self.editor.add_bent_pipe((dx,dy,dz), radius)
        self.update_plot()

    def update_default_diameter(self, d):
        self.editor.change_diameter(d)
        for structure in self.editor.staged_structures:
            structure.set_diameter(d)
        self.update_plot()

    def add_flange(self):
        self.editor.dismiss()
        self.editor.add_flange()
        self.editor.add_bent_pipe()
        self.update()

    def commit_structure(self):
        self.coords = self.editor.anchor.coords()
        self.editor.commit()
        self.update_plot()

    def unstage_structure(self):
        self.update_plot()

    def remove_actors(self):
        self.renderer.RemoveActor(self.pipeline_actor)
        self.renderer.RemoveActor(self.control_points_actor)
        self.renderer.RemoveActor(self.passive_points_actor)
        self.renderer.RemoveActor(self.selected_points_actor)

        self.pipeline_actor = None
        self.control_points_actor = None
        self.passive_points_actor = None
        self.selected_points_actor = None

    def selection_callback(self, x, y):
        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = bool(modifiers & Qt.ControlModifier)
        shift_pressed = bool(modifiers & Qt.ShiftModifier)
        alt_pressed = bool(modifiers & Qt.AltModifier)

        # First try to select points
        selected_point = self._pick_point(x, y)
        if selected_point is not None:
            self.editor.select_points(
                [selected_point], join=ctrl_pressed | shift_pressed, remove=alt_pressed
            )
            self.update_selection()
            return

        # If no points were found try structures
        selected_structure = self._pick_structure(x, y)
        if selected_structure is not None:
            self.editor.select_structures(
                [selected_structure], join=ctrl_pressed | shift_pressed, remove=alt_pressed
            )
            self.update_selection()
            return

        self.editor.clear_selection()
        self.update_selection()

    def _pick_point(self, x, y):
        index = self._pick_actor(x, y, self.control_points_actor)
        pipeline = self.editor.pipeline
        if index >= 0:
            return pipeline.control_points[index]

        index = self._pick_actor(x, y, self.passive_points_actor)
        if index >= 0:
            return pipeline.points[index]

    def _pick_structure(self, x, y):
        pipeline = self.editor.pipeline
        index = self._pick_actor(x, y, self.pipeline_actor)
        if index >= 0:
            data: vtk.vtkPolyData = self.pipeline_actor.GetMapper().GetInput()
            cell_identifier = data.GetCellData().GetArray("cell_identifier")
            if cell_identifier is None:
                return
            structure_index = cell_identifier.GetValue(index)
            return pipeline.structures[structure_index]

    def _pick_actor(self, x, y, actor_to_select):
        selection_picker = vtk.vtkCellPicker()
        selection_picker.SetTolerance(0.005)
        pickability = dict()

        for actor in self.renderer.GetActors():
            pickability[actor] = actor.GetPickable()
            if actor == actor_to_select:
                actor.PickableOn()
            else:
                actor.PickableOff()

        selection_picker.Pick(x, y, 0, self.renderer)

        for actor in self.renderer.GetActors():
            actor.SetPickable(pickability[actor])

        return selection_picker.GetCellId()

    def update_selection(self):
        if self.editor.selected_points:
            # the last point selected is the one that will
            # be the "anchor" to continue the pipe creation
            *_, point = self.editor.selected_points
            self.change_anchor(point)

        # Only dismiss structure creation if something was actually selected
        something_selected = self.editor.selected_points or self.editor.selected_structures
        if something_selected:
            self.editor.dismiss()

        self.selection_changed.emit()
        self.update_plot(reset_camera=False)
