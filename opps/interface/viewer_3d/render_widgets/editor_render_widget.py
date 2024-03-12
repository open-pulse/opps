from dataclasses import dataclass
from enum import Enum
from itertools import chain

import numpy as np
import vtk
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication

from opps.interface.viewer_3d.actors import ControlPointsActor, PassivePointsActor, SelectedPointsActor

from vtkat.interactor_styles import BoxSelectionInteractorStyle
from vtkat.render_widgets import CommonRenderWidget
from vtkat.pickers import CellPropertyAreaPicker, CellAreaPicker


class EditorRenderWidget(CommonRenderWidget):
    selection_changed = pyqtSignal()

    def __init__(self, editor, parent=None):
        super().__init__(parent)
        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)
        self.editor = editor

        self.interactor_style = BoxSelectionInteractorStyle()
        self.render_interactor.SetInteractorStyle(self.interactor_style)

        self.selected_structure = None
        self.pipeline_actor = None
        self.control_points_actor = None
        self.passive_points_actor = None
        self.selected_points_actor = None
        self.coords = np.array([0, 0, 0])

        self.renderer.GetActiveCamera().SetParallelProjection(True)
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

    def stage_pipe_deltas(self, dx, dy, dz, radius=0.3):
        self.editor.dismiss()
        self.editor.clear_selection()
        self.editor.add_bent_pipe((dx,dy,dz), radius)
        self.update_plot()

    def update_default_diameter(self, initial_diameter, final_diameter=0):
        self.editor.change_diameter(initial_diameter, final_diameter)
        for structure in self.editor.staged_structures:
            structure.set_diameter(initial_diameter, final_diameter)
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

    def click_callback(self, x, y):
        self.mouse_click = x, y

    def selection_callback(self, x, y):
        modifiers = QApplication.keyboardModifiers()
        ctrl_pressed = bool(modifiers & Qt.ControlModifier)
        shift_pressed = bool(modifiers & Qt.ShiftModifier)
        alt_pressed = bool(modifiers & Qt.AltModifier)

        picked_points = self._pick_points(x, y)
        picked_structures = self._pick_structures(x, y)

        # give selection priority to points 
        if len(picked_points) == 1 and len(picked_structures) <= 1:
            picked_structures.clear()

        if picked_points:
            self.editor.select_points(
                picked_points,
                join=ctrl_pressed | shift_pressed,
                remove=alt_pressed
            )

        if picked_structures is not None:
            self.editor.select_structures(
                picked_structures,
                join=ctrl_pressed | shift_pressed,
                remove=alt_pressed
            )

        if (not picked_points) and (not picked_structures):
            self.editor.clear_selection() 

        self.update_selection()

    def _pick_points(self, x, y):
        pipeline = self.editor.pipeline

        picked = self._pick_actor(x, y, self.control_points_actor)
        indexes = picked.get(self.control_points_actor, [])
        control_points = [pipeline.control_points[i] for i in  indexes]

        picked = self._pick_actor(x, y, self.passive_points_actor)
        indexes = picked.get(self.passive_points_actor, [])
        passive_points = [pipeline.points[i] for i in  indexes]
        
        combined_points = set(control_points + passive_points)
        return list(combined_points)

    def _pick_structures(self, x, y):
        pipeline = self.editor.pipeline
        indexes = self._pick_property(x, y, "cell_identifier", self.pipeline_actor)
        return [pipeline.structures[i] for i in indexes]

    def _pick_actor(self, x, y, actor_to_select):
        selection_picker = CellAreaPicker()
        pickability = dict()

        for actor in self.renderer.GetActors():
            pickability[actor] = actor.GetPickable()
            if actor == actor_to_select:
                actor.PickableOn()
            else:
                actor.PickableOff()

        x0, y0 = self.mouse_click
        mouse_moved = (abs(x0 - x) > 10) or (abs(y0 - y) > 10)
        if mouse_moved:
            selection_picker.area_pick(x0, y0, x, y, self.renderer)
        else:
            selection_picker.pick(x, y, 0, self.renderer)

        for actor in self.renderer.GetActors():
            actor.SetPickable(pickability[actor])

        return selection_picker.get_picked()

    def _pick_property(self, x, y, property_name, desired_actor):
        selection_picker = CellPropertyAreaPicker(property_name, desired_actor)
        pickability = dict()

        for actor in self.renderer.GetActors():
            pickability[actor] = actor.GetPickable()
            if actor == desired_actor:
                actor.PickableOn()
            else:
                actor.PickableOff()

        x0, y0 = self.mouse_click
        mouse_moved = (abs(x0 - x) > 10) or (abs(y0 - y) > 10)
        if mouse_moved:
            selection_picker.area_pick(x0, y0, x, y, self.renderer)
        else:
            selection_picker.pick(x, y, 0, self.renderer)

        for actor in self.renderer.GetActors():
            actor.SetPickable(pickability[actor])

        return selection_picker.get_picked()

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
