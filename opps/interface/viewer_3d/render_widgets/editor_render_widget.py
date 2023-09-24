import vtk

from opps.interface.viewer_3d.actors.fixed_point_actor import FixedPointActor
from opps.interface.viewer_3d.actors.pipeline_actor import PipelineActor
from opps.interface.viewer_3d.render_widgets.common_render_widget import (
    CommonRenderWidget,
)
from opps.model.pipeline import Pipeline


class EditorRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pipeline = Pipeline()
        self.pipeline.add_pipe_from_deltas(
            (236, 0, 0),
            (118, 0, 0),
            (123, 0, -123),
            (0, 380, 0),
            (0, 0, 307),
            (0, 0, 801),
        )
        self.pipeline.add_flange((0,0,0), (0,1,0))
        # self.pipeline.add_pipe_from_points(
        #     (0,0,0),
        #     (1,0,0),
        #     (2,1,0),
        #     (2,1,-1),
        # )
        # self.pipeline.add_pipe((0, 0, 0), (0, 1, 0))
        # self.pipeline.add_pipe((1, 2, 0), (2, 2, 0))
        # self.pipeline.add_bend((0, 1, 0), (1, 2, 0), (1, 1, 0))

        self.fixed_point_actor = None
        self.pipeline_actor = None

        self.create_axes()
        self.update_plot()

    def update_plot(self):
        self.remove_actors()
        # self.fixed_point_actor = FixedPointActor()
        self.pipeline_actor = self.pipeline.as_vtk()

        self.renderer.AddActor(self.fixed_point_actor)
        self.renderer.AddActor(self.pipeline_actor)
        self.renderer.ResetCamera()
        self.set_isometric_view()

    def remove_actors(self):
        self.renderer.RemoveActor(self.fixed_point_actor)
        self.fixed_point_actor = None
