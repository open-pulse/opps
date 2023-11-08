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


class EditorRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.style = SelectionInteractor()
        # self.render_interactor.SetInteractorStyle(self.style)

        self.editor = PipelineEditor()
        self.editor.set_deltas((1, 0, 0))
        self.editor.add_pipe()
        self.editor.commit()

        self.bla = True
        # self.editor.set_deltas((0, 1, 0))
        # self.editor.add_pipe()
        # self.editor.commit()
        # bend = self.editor.pipeline.components[-1]
        # bend.corner = np.array([1.3, 0, 0])

        # self.editor.update_joints(self.editor.pipeline.components)

        # self.pipeline = Pipeline()
        # self.tmp_structure = None

        self.pipeline_actor = None
        # self.tmp_structure_actor = None

        # self.bla = False

        # self._previous_point = np.array([0, 0, 0])
        # self._current_point = np.array([0, 0, 0])
        # self.pipeline.add_pipe_from_deltas(
        #     (236, 0, 0),
        #     (118, 0, 0),
        #     (123, 0, -123),
        #     (0, 380, 0),
        #     (0, 0, 307),
        #     (0, 0, 801),
        # )

        # self.pipeline.add_flange((0,0,0), (1,1,1))
        # self.pipeline.add_pipe_from_points(
        #     (0,0,0),
        #     (1,0,0),
        #     (2,1,0),
        #     (2,1,-1),
        # )

        # self.pipeline.add_pipe((0, 0, 0), (0, 1, 0))
        # self.pipeline.add_pipe((1, 2, 0), (2, 2, 0))
        # self.pipeline.add_bend((0, 1, 0), (1, 2, 0), (1, 1, 0))

        self.create_axes()
        self.update_plot()

    def update_plot(self, reset_camera=True):
        self.remove_actors()

        self.pipeline_actor = self.editor.pipeline.as_vtk()
        self.renderer.AddActor(self.pipeline_actor)

        if reset_camera:
            self.renderer.ResetCamera()
        self.update()

    def stage_pipe_deltas(self, dx, dy, dz):
        if (dx, dy, dz) == (0, 0, 0):
            return
        
        if self.bla: 
            self.editor.add_bend()
        self.bla = not self.bla

        self.editor.set_deltas((dx, dy, dz))
        self.editor.add_pipe()

        # self.editor.move_control_point(
        #     self.editor.current_point, 
        #     self.editor.current_point + (dx, dy, dz)
        # )
        # self.editor.move_control_point((dx, dy, dz))
        self.update_plot()

        # self._current_point = self._previous_point + (dx, dy, dz)
        # pipe = Pipe(self._previous_point, self._current_point)
        # self.stage_structure(pipe)

    def add_flange(self):
        self._current_point = self._previous_point
        self.pipeline.add_oriented_flange(self._current_point)
        self.tmp_structure = None
        self.update_plot()

    def stage_structure(self, structure):
        self.tmp_structure = structure
        self.update_plot()

    def commit_structure(self):
        self.editor.commit()
        self.editor.add_pipe()
        # self.pipeline.add_structure(self.tmp_structure, auto_connect=True)
        # self.tmp_structure = None
        # self._previous_point = self._current_point
        # self.update_plot()

    def unstage_structure(self):
        return
        self.editor.dismiss()
        self.tmp_structure = None
        self._current_point = self._previous_point
        self.update_plot(reset_camera=False)

    def remove_actors(self):
        self.renderer.RemoveActor(self.pipeline_actor)
        # self.renderer.RemoveActor(self.tmp_structure_actor)
        self.pipeline_actor = None
        self.tmp_structure_actor = None
