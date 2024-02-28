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

    def set_diameter(self, diameter, point=None):
        if point is None:
            self.start_diameter = diameter
            self.end_diameter = diameter
            return

        if point == self.start:
            self.start_diameter = diameter

        if point == self.end:
            self.end_diameter = diameter

    def get_diameters(self):
        return [self.start_diameter, self.end_diameter]

    def get_points(self):
        return [
            self.start,
            self.end,
        ]

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.pipe_actor import PipeActor

        return PipeActor(self)

    def __hash__(self) -> int:
        return id(self)
    
    def replace_point(self, old, new):
        if self.start == old:
            self.start = new
        
        elif self.end == old:
            self.end = new
        
