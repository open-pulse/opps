from dataclasses import dataclass
from enum import Enum

import numpy as np
import vtk
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from opps import app
from opps.interface.viewer_3d.actors import ControlPointsActor, PassivePointsActor, SelectedPointsActor
from opps.model import Flange, Pipe, Pipeline
from opps.model.pipeline_editor import PipelineEditor

from vtkat.render_widgets import CommonRenderWidget


class EditorRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.left_clicked.connect(self.selection_callback)
        app().geometry_toolbox.selection_changed.connect(self.update_selection)

        self.show_passive_points = True
        self.selected_structure = None
        self.pipeline_actor = None
        self.control_points_actor = None
        self.passive_points_actor = None
        self.selected_points = None
        self.coords = np.array([0, 0, 0])

        self.create_axes()
        self.update_plot()

    def update_plot(self, reset_camera=True):
        self.remove_actors()

        self.pipeline_actor = app().geometry_toolbox.pipeline.as_vtk()
        self.control_points_actor = ControlPointsActor(app().geometry_toolbox.editor.control_points)
        self.passive_points_actor = PassivePointsActor(app().geometry_toolbox.editor.points)
        self.selected_points = SelectedPointsActor(app().geometry_toolbox.get_selected_points())

        # The order matters. It defines wich points will appear first.
        self.renderer.AddActor(self.pipeline_actor)
        self.renderer.AddActor(self.passive_points_actor)
        self.renderer.AddActor(self.control_points_actor)
        self.renderer.AddActor(self.selected_points)

        if reset_camera:
            self.renderer.ResetCamera()
        self.update()

    def change_anchor(self, point):
        editor = app().geometry_toolbox.editor
        editor.dismiss()
        editor.set_anchor(point)
        self.coords = point.coords()
        self.update_plot(reset_camera=False)

    def stage_pipe_deltas(self, dx, dy, dz, auto_bend=True):
        editor = app().geometry_toolbox.editor
        editor.dismiss()
        editor.set_deltas((dx, dy, dz))

        if auto_bend:
            editor.add_bend()
        editor.add_pipe()

        editor._update_joints()
        self.update_plot()

    def update_default_diameter(self, d):
        editor = app().geometry_toolbox.editor
        editor.change_diameter(d)
        for structure in editor.staged_structures:
            structure.set_diameter(d)
        self.update_plot()

    def add_flange(self):
        editor = app().geometry_toolbox.editor
        editor.dismiss()
        editor.add_flange()
        editor.add_bent_pipe()
        self.update()

    def commit_structure(self):
        editor = app().geometry_toolbox.editor
        self.coords = editor.anchor.coords()
        editor.commit()
        self.update_plot()

    def unstage_structure(self):
        app().geometry_toolbox.editor.dismiss()
        self.update_plot()

    def remove_actors(self):
        self.renderer.RemoveActor(self.pipeline_actor)
        self.renderer.RemoveActor(self.control_points_actor)
        self.renderer.RemoveActor(self.passive_points_actor)
        self.renderer.RemoveActor(self.selected_points)

        self.pipeline_actor = None
        self.control_points_actor = None
        self.passive_points_actor = None
        self.selected_points = None

    def selection_callback(self, x, y):
        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = bool(modifiers & Qt.ControlModifier)
        shift_pressed = bool(modifiers & Qt.ShiftModifier)
        alt_pressed = bool(modifiers & Qt.AltModifier)

        # First try to select points
        selected_point = self._pick_point(x, y)
        if selected_point is not None:
            app().geometry_toolbox.select_points(
                [selected_point], join=ctrl_pressed | shift_pressed, remove=alt_pressed
            )
            return

        # If no points were found try structures
        selected_structure = self._pick_structure(x, y)
        if selected_structure is not None:
            app().geometry_toolbox.select_structures(
                [selected_structure], join=ctrl_pressed | shift_pressed, remove=alt_pressed
            )
            return

        app().geometry_toolbox.clear_selection()

    def _pick_point(self, x, y):
        index = self._pick_actor(x, y, self.control_points_actor)
        if index >= 0:
            return app().geometry_toolbox.editor.control_points[index]

        index = self._pick_actor(x, y, self.passive_points_actor)
        if index >= 0:
            return app().geometry_toolbox.editor.points[index]

    def _pick_structure(self, x, y):
        index = self._pick_actor(x, y, self.pipeline_actor)
        if index >= 0:
            data: vtk.vtkPolyData = self.pipeline_actor.GetMapper().GetInput()
            cell_identifier = data.GetCellData().GetArray("cell_identifier")
            if cell_identifier is None:
                return
            structure_index = cell_identifier.GetValue(index)
            return app().geometry_toolbox.pipeline.structures[structure_index]

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
        if app().geometry_toolbox.selected_points:
            # the last point selected is the one that will
            # be the "anchor" to continue the pipe creation
            *_, point = app().geometry_toolbox.selected_points
            self.change_anchor(point)

        # Only dismiss structure creation if something was actually selected
        something_selected = app().geometry_toolbox.selected_points or app().geometry_toolbox.selected_structures
        if something_selected:
            app().geometry_toolbox.editor.dismiss()

        self.update_plot(reset_camera=False)
