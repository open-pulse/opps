from dataclasses import dataclass

import numpy as np

from opps.model.bend import Bend
from opps.model.point import Point


def normalize(vector):
    return vector / np.linalg.norm(vector)


@dataclass
class Elbow(Bend):
    def as_vtk(self):
        from opps.interface.viewer_3d.actors.elbow_actor import ElbowActor

        return ElbowActor(self)

    def __hash__(self) -> int:
        return id(self)
