from dataclasses import dataclass

import numpy as np

from opps.model.point import Point


@dataclass
class Flange:
    position: Point
    normal: np.ndarray
    diameter: float = 0.1
    color: tuple = (255, 255, 255)

    def get_points(self):
        return [self.position]

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.flange_actor import FlangeActor

        return FlangeActor(self)
