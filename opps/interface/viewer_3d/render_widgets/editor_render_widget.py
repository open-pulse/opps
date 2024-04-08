from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opps.model import Pipeline

import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication
from vtkat.interactor_styles import BoxSelectionInteractorStyle
from vtkat.pickers import CellAreaPicker, CellPropertyAreaPicker
from vtkat.render_widgets import CommonRenderWidget

from opps.interface.viewer_3d.actors import (
    ControlPointsActor,
    PassivePointsActor,
    SelectedPointsActor,
)


class EditorRenderWidget(CommonRenderWidget):
    selection_changed = pyqtSignal()

    def __init__(self, pipeline: "Pipeline", parent=None):
        super().__init__(parent)
        self.interactor_style = BoxSelectionInteractorStyle()
        self.render_interactor.SetInteractorStyle(self.interactor_style)

        self.pipeline = pipeline
        self.pipeline_actor = None
        self.control_points_actor = None
        self.passive_points_actor = None
        self.selected_points_actor = None

        self.renderer.GetActiveCamera().SetParallelProjection(True)
        self.create_axes()
        self.update_plot()
        self.left_clicked.connect(self.click_callback)
        self.left_released.connect(self.selection_callback)

    def update_plot(self, reset_camera=True):
        self.remove_actors()

        self.pipeline_actor = self.pipeline.as_vtk()
        self.control_points_actor = ControlPointsActor(self.pipeline.points)
        self.passive_points_actor = PassivePointsActor(self.pipeline.points)
        self.selected_points_actor = SelectedPointsActor(self.pipeline.selected_points)

        # The order matters. It defines wich points will appear first.
        self.renderer.AddActor(self.pipeline_actor)
        self.renderer.AddActor(self.passive_points_actor)
        self.renderer.AddActor(self.control_points_actor)
        self.renderer.AddActor(self.selected_points_actor)

        if reset_camera:
            self.renderer.ResetCamera()
        self.update()

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

        join = ctrl_pressed | shift_pressed
        remove = alt_pressed

        if not (join or remove):
            self.pipeline.clear_selection()

        picked_points = self._pick_points(x, y)
        picked_structures = self._pick_structures(x, y)

        # give selection priority to points
        if len(picked_points) == 1 and len(picked_structures) <= 1:
            picked_structures.clear()

        if picked_points:
            self.pipeline.select_points(picked_points, join=join, remove=remove)

        if picked_structures:
            self.pipeline.select_structures(picked_structures, join=join, remove=remove)

        # Only dismiss structure creation if something was actually selected
        something_selected = self.pipeline.selected_points or self.pipeline.selected_structures
        something_staged = self.pipeline.staged_points or self.pipeline.staged_structures
        if something_selected and something_staged:
            self.pipeline.dismiss()

        self.update_selection()

    def _pick_points(self, x, y):
        picked = self._pick_actor(x, y, self.control_points_actor)
        indexes = picked.get(self.control_points_actor, [])
        control_points = [self.pipeline.points[i] for i in indexes]

        return control_points

    def _pick_structures(self, x, y):
        try:
            indexes = self._pick_property(x, y, "cell_identifier", self.pipeline_actor)
            return [self.pipeline.structures[i] for i in indexes]
        except IndexError:
            return list()

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
        self.selection_changed.emit()
        self.update_plot(reset_camera=False)
