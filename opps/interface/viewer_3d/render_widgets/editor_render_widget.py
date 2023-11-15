import numpy as np
import vtk

from opps.interface.viewer_3d.actors.fixed_point_actor import FixedPointActor
from opps.interface.viewer_3d.actors.pipeline_actor import PipelineActor
from opps.interface.viewer_3d.interactor_styles.selection_interactor import (
    SelectionInteractor,
)
from opps.interface.viewer_3d.render_widgets.common_render_widget import (
    CommonRenderWidget,
)
from opps.model import Flange, Pipe, Pipeline
from opps.model.pipeline_editor import PipelineEditor
from opps.interface.viewer_3d.actors.points_actor import PointsActor


class EditorRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.editor = PipelineEditor()
        self.current_pipe = self.editor.add_pipe()

        self.pipeline_actor = None
        self.control_points_actor = None
        self.coords = np.array([0,0,0])

        self.create_axes()
        self.update_plot()

    def update_plot(self, reset_camera=True):
        self.remove_actors()

        self.pipeline_actor = self.editor.pipeline.as_vtk()

        self.control_points_actor = PointsActor(self.editor.control_points)
        self.control_points_actor.GetProperty().SetColor(1, 0.7, 0.2)
        self.control_points_actor.GetProperty().LightingOff()

        self.renderer.AddActor(self.pipeline_actor)
        self.renderer.AddActor(self.control_points_actor)

        if reset_camera:
            self.renderer.ResetCamera()
        self.update()

    def change_index(self, i):
        if not self.editor.control_points:
            return

        self.editor.dismiss()
        if i >= len(self.editor.control_points):
            i = len(self.editor.control_points) - 1

        self.coords = self.editor.control_points[i].coords()
        self.editor.set_active_point(i)
        self.editor.add_bent_pipe()
        self.update_plot()

    def stage_pipe_deltas(self, dx, dy, dz):
        if (dx, dy, dz) == (0, 0, 0):
            self.unstage_structure()
            return

        if not self.editor.staged_structures:
            self.editor.add_bent_pipe()
            self.coords = self.editor.active_point.coords()

        self.editor.set_deltas((dx, dy, dz))
        new_position = self.coords + (dx, dy, dz)
        self.editor.move_point(new_position)
        self.editor._update_joints()
        self.update_plot()

    def update_diameter(self, d):
        self.editor.change_diameter(d)
        self.update_plot()

    def add_flange(self):
        self.editor.add_flange()

    def stage_structure(self, structure):
        self.tmp_structure = structure
        self.update_plot()

    def commit_structure(self):
        self.coords = self.editor.active_point.coords()
        self.editor.commit()
        self.update_plot()

    def unstage_structure(self):
        self.editor.dismiss()
        self.update_plot()

    def remove_actors(self):
        self.renderer.RemoveActor(self.pipeline_actor)
        self.renderer.RemoveActor(self.control_points_actor)

        self.pipeline_actor = None
        self.control_points_actor = None
