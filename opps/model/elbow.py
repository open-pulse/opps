from dataclasses import dataclass

import numpy as np

from opps.model.bend import Bend
from opps.model.point import Point


def normalize(vector):
    return vector / np.linalg.norm(vector)


@dataclass
class Elbow(Bend):
    start: Point
    end: Point
    corner: Point
    curvature: float
    start_diameter: float = 0.1
    end_diameter: float = 0.1
    color: tuple = (255, 255, 255)

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.elbow_actor import ElbowActor

        return ElbowActor(self)
