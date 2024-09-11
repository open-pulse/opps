import numpy as np

from .bend import Bend
from .point import Point


class Elbow(Bend):
    def as_vtk(self):
        from opps.interface.viewer_3d.actors.elbow_actor import ElbowActor

        return ElbowActor(self)
