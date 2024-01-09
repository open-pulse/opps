from dataclasses import dataclass
from enum import Enum

import numpy as np
import vtk

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

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

        self.selected_structure = None

        self.pipeline_actor = None
        self.control_points_actor = None
        self.selected_points = None
        self.coords = np.array([0, 0, 0])

        self.create_axes()
        self.update_plot()

    def update_plot(self, reset_camera=True):
        self.remove_actors()

        self.pipeline_actor = app().pipeline.as_vtk()

        self.control_points_actor = PointsActor(app().editor.control_points)
        self.control_points_actor.set_color((255, 178, 51))

        list_points = [app().get_point(i) for i in app().selected_points_index]
        self.selected_points = PointsActor(list_points)
        self.selected_points.GetProperty().SetColor(1, 0, 0)
        self.selected_points.GetProperty().LightingOff()

        self.renderer.AddActor(self.pipeline_actor)
        self.renderer.AddActor(self.control_points_actor)
        self.renderer.AddActor(self.selected_points)

        if reset_camera:
            self.renderer.ResetCamera()
        self.update()

    def change_index(self, i):
        if not app().editor.control_points:
            return

        app().editor.dismiss()
        if i >= len(app().editor.control_points):
            i = len(app().editor.control_points) - 1

        self.coords = app().editor.control_points[i].coords()
        app().editor.set_active_point(i)
        self.update_plot(reset_camera=False)

    def stage_pipe_deltas(self, dx, dy, dz, auto_bend=True):
        app().clear_selection()

        if (dx, dy, dz) == (0, 0, 0):
            self.unstage_structure()
            return

        if not app().editor.staged_structures:
            self.coords = app().editor.active_point.coords()
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

    def stage_structure(self, structure):
        self.tmp_structure = structure
        self.update_plot()

    def commit_structure(self):
        self.coords = app().editor.active_point.coords()
        app().editor.commit()
        self.update_plot()

    def unstage_structure(self):
        app().editor.dismiss()
        self.update_plot()

    def remove_actors(self):
        self.renderer.RemoveActor(self.pipeline_actor)
        self.renderer.RemoveActor(self.control_points_actor)
        self.renderer.RemoveActor(self.selected_points)

        self.pipeline_actor = None
        self.control_points_actor = None
        self.selected_points = None

    def selection_callback(self, x, y):
        self.selection_picker = vtk.vtkCellPicker()
        self.selection_picker.SetTolerance(0.005)

        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = bool(modifiers & Qt.ControlModifier)
        shift_pressed = bool(modifiers & Qt.ShiftModifier)
        alt_pressed = bool(modifiers & Qt.AltModifier)

        # First try to select points
        point_index = self._pick_point(x, y)
        if point_index is not None:
            app().select_points(
                [point_index],
                join=ctrl_pressed|shift_pressed,
                remove=alt_pressed
            )
            return

        # If no points were found try structures
        structure_index = self._pick_structure(x, y)
        if structure_index is not None:
            app().select_structures(
                [structure_index],
                join=ctrl_pressed|shift_pressed,
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
        if clicked_actor == self.control_points_actor:
            return clicked_cell

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
        if app().selected_points_index:
            # the last point selected is the one that will 
            # be the "anchor" to continue the pipe creation
            *_, point_index = app().selected_points_index
            self.change_index(point_index)

        # Only dismiss structure creation if something was actually selected
        if app().selected_points_index or app().selected_structures_index:
            app().editor.dismiss()

        self.update_plot(reset_camera=False)
