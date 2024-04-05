from dataclasses import dataclass

import numpy as np

from .point import Point
from .structure import Structure


@dataclass
class Pipe(Structure):
    start: Point
    end: Point
    diameter: float = 0.1
    thickness: float = 0

    def set_diameter(self, diameter, *args):
        self.diameter = diameter

    def get_diameters(self):
        return [self.diameter]

    def get_points(self):
        return [
            self.start,
            self.end,
        ]

    def replace_point(self, old, new):
        if self.start == old:
            self.start = new

        elif self.end == old:
            self.end = new

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.pipe_actor import PipeActor

        return PipeActor(self)

    def __hash__(self) -> int:
        return id(self)
