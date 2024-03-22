from dataclasses import dataclass

import numpy as np

from .point import Point
from .structure import Structure


@dataclass
class Flange(Structure):
    position: Point
    normal: np.ndarray
    diameter: float = 0.1
    auto: bool = True

    def get_points(self):
        return [self.position]

    def set_diameter(self, diameter, *args):
        self.diameter = diameter

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.flange_actor import FlangeActor

        return FlangeActor(self)

    def __hash__(self) -> int:
        return id(self)
    
    def replace_point(self, old, new):
        if self.start == old:
            self.start = new

        elif self.end == old:
            self.end = new


