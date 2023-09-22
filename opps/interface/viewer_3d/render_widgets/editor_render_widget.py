import vtk

from opps.interface.viewer_3d.actors.fixed_point_actor import FixedPointActor

from .common_render_widget import CommonRenderWidget


class EditorRenderWidget(CommonRenderWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.fixed_point_actor = None
        self.create_axes()
        self.update_plot()

    def update_plot(self):
        self.remove_actors()
        self.fixed_point_actor = FixedPointActor()
        self.renderer.AddActor(self.fixed_point_actor)
        self.renderer.ResetCamera()

    def remove_actors(self):
        self.renderer.RemoveActor(self.fixed_point_actor)
        self.fixed_point_actor = None
