from .bend import Bend


class Elbow(Bend):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.elbow_actor import ElbowActor

        return ElbowActor(self)
