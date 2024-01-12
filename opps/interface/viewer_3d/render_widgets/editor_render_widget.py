from dataclasses import dataclass
from enum import Enum

import numpy as np
import vtk
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from opps import app
from opps.interface.viewer_3d.actors.fixed_point_actor import FixedPointActor
from opps.interface.viewer_3d.actors.pipeline_actor import PipelineActor
from opps.interface.viewer_3d.actors.points_actor import PointsActor
from opps.interface.viewer_3d.interactor_styles.selection_interactor import (
    SelectionInteractor,
)
from opps.interface.viewer_3d.render_widgets.common_render_widget import (
    CommonRenderWidget,
)
from opps.model import Flange, Pipe, Pipeline
from opps.model.pipeline_editor import PipelineEditor


class EditorRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.left_clicked.connect(self.selection_callback)
        app().selection_changed.connect(self.update_selection)

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

        self.pipeline_actor = app().pipeline.as_vtk()

        self.control_points_actor = PointsActor(app().editor.control_points)
        self.control_points_actor.set_color((255, 180, 50))
        self.control_points_actor.PickableOff()

        self.passive_points_actor = PointsActor(app().editor.points)
        self.passive_points_actor.set_color((255, 200, 1101))
        self.passive_points_actor.GetProperty().RenderPointsAsSpheresOff()
        self.passive_points_actor.GetProperty().SetPointSize(12)
        self.passive_points_actor.set_visibility_offset(-10000)

        list_points = list(app().get_selected_points())
        self.selected_points = PointsActor(list_points)
        self.selected_points.GetProperty().SetColor(1, 0, 0)
        self.selected_points.GetProperty().LightingOff()

        self.renderer.AddActor(self.pipeline_actor)
        self.renderer.AddActor(self.control_points_actor)
        self.renderer.AddActor(self.passive_points_actor)
        self.renderer.AddActor(self.selected_points)

        if reset_camera:
            self.renderer.ResetCamera()
        self.update()

    def change_anchor(self, point):
        # if not app().editor.points:
        #     return

        app().editor.dismiss()
        # if i >= len(app().editor.points):
        #     i = len(app().editor.points) - 1

        self.coords = point.coords()
        app().editor.set_anchor(point)
        self.update_plot(reset_camera=False)

    def stage_pipe_deltas(self, dx, dy, dz, auto_bend=True):
        app().clear_selection()

        if (dx, dy, dz) == (0, 0, 0):
            self.unstage_structure()
            return

        if not app().editor.staged_structures:
            self.coords = app().editor.anchor.coords()
            if auto_bend:
                app().editor.add_bent_pipe()
            else:
                app().editor.add_pipe()

        app().editor.set_deltas((dx, dy, dz))
        new_position = self.coords + (dx, dy, dz)
        app().editor.move_point(new_position)
        app().editor._update_joints()
        self.update_plot()

    def update_default_diameter(self, d):
        app().editor.change_diameter(d)
        for structure in app().editor.staged_structures:
            structure.set_diameter(d)
        self.update_plot()

    def add_flange(self):
        self.unstage_structure()
        app().editor.add_flange()
        app().editor.add_bent_pipe()

    def commit_structure(self):
        self.coords = app().editor.anchor.coords()
        app().editor.commit()
        self.update_plot()

    def unstage_structure(self):
        app().editor.dismiss()
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
        self.selection_picker = vtk.vtkCellPicker()
        self.selection_picker.SetTolerance(0.005)

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = bool(modifiers & Qt.ControlModifier)
        shift_pressed = bool(modifiers & Qt.ShiftModifier)
        alt_pressed = bool(modifiers & Qt.AltModifier)

        # First try to select points
        selected_point = self._pick_point(x, y)
        if selected_point is not None:
            app().select_points(
                [selected_point], 
                join=ctrl_pressed | shift_pressed, 
                remove=alt_pressed
            )
            return

        # If no points were found try structures
        structure_index = self._pick_structure(x, y)
        if structure_index is not None:
            app().select_structures(
                [structure_index], 
                join=ctrl_pressed | shift_pressed, 
                remove=alt_pressed
            )
            return

        app().clear_selection()

    def _pick_point(self, x, y):
        # save pickability
        pickable = self.pipeline_actor.GetPickable()

        # Disable pipeline actor pickability to only select points
        self.pipeline_actor.PickableOff()
        self.selection_picker.Pick(x, y, 0, self.renderer)

        # restore pickability
        self.pipeline_actor.SetPickable(pickable)

        clicked_actor = self.selection_picker.GetActor()
        clicked_cell = self.selection_picker.GetCellId()
        if clicked_actor == self.passive_points_actor:
            return app().editor.points[clicked_cell]
        elif clicked_actor == self.control_points_actor:
            return app().editor.control_points[clicked_cell]

    def _pick_structure(self, x, y):
        self.selection_picker.Pick(x, y, 0, self.renderer)
        clicked_actor = self.selection_picker.GetActor()
        clicked_cell = self.selection_picker.GetCellId()

        if clicked_actor == self.pipeline_actor:
            data: vtk.vtkPolyData = clicked_actor.GetMapper().GetInput()
            cell_identifier = data.GetCellData().GetArray("cell_identifier")
            if cell_identifier is None:
                return
            structure_index = cell_identifier.GetValue(clicked_cell)
            return structure_index

    def update_selection(self):
        if app().selected_points:
            # the last point selected is the one that will
            # be the "anchor" to continue the pipe creation
            *_, point = app().selected_points
            self.change_anchor(point)

        # Only dismiss structure creation if something was actually selected
        something_selected = app().selected_points or app().selected_structures_index
        if something_selected:
            app().editor.dismiss()

        self.update_plot(reset_camera=False)
