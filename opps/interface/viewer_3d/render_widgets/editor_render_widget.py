import vtk

from opps.interface.viewer_3d.actors.fixed_point_actor import FixedPointActor
from opps.interface.viewer_3d.actors.pipeline_actor import PipelineActor
from opps.interface.viewer_3d.render_widgets.common_render_widget import (
    CommonRenderWidget,
)
from opps.model import Pipeline, Pipe


class EditorRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pipeline = Pipeline()
        self.tmp_structure = None

        self.pipeline_actor = None
        self.tmp_structure_actor = None

        self.pipeline.add_pipe_from_deltas(
            (236, 0, 0),
            (118, 0, 0),
            (123, 0, -123),
            (0, 380, 0),
            (0, 0, 307),
            (0, 0, 801),
        )

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

    def update_plot(self):
        self.remove_actors()

        self.pipeline_actor = self.pipeline.as_vtk()
        self.renderer.AddActor(self.pipeline_actor)

        if self.tmp_structure is not None:
            self.tmp_structure_actor = self.tmp_structure.as_vtk()
            self.tmp_structure_actor.GetProperty().SetOpacity(0.6)
            self.tmp_structure_actor.GetProperty().SetColor(1, 1, 0.5)
            self.tmp_structure_actor.GetProperty().LightingOff()
            self.renderer.AddActor(self.tmp_structure_actor)

        self.renderer.ResetCamera()
        # self.set_isometric_view()

    def stage_structure(self, structure):
        self.tmp_structure = structure
        self.update_plot()
    
    def commit_structure(self):
        self.pipeline.add_structure(self.tmp_structure)
        self.tmp_structure = None
        self.update_plot()

    def remove_actors(self):
        self.renderer.RemoveActor(self.pipeline_actor)
        self.renderer.RemoveActor(self.tmp_structure_actor)
        self.pipeline_actor = None
        self.tmp_structure_actor = None
