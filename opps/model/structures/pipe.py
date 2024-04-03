from dataclasses import dataclass

import numpy as np

from .point import Point
from .structure import Structure


@dataclass
class Pipe(Structure):
    start: Point
    end: Point
    start_diameter: float = 0.1
    end_diameter: float = 0.1
    thickness: float = 0

    def set_diameter(self, start_diameter, final_diameter, *args):
        self.start_diameter = start_diameter
        self.end_diameter = final_diameter

    def get_diameters(self):
        return [self.start_diameter, self.end_diameter]

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
