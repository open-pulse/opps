from dataclasses import dataclass

import numpy as np

from .point import Point
from .structure import Structure


class Flange(Structure):
    def __init__(self, start: Point, end: Point, **kwargs) -> None:
        super().__init__(**kwargs)

        self.start = start
        self.end = end
        # I am adding 0.02 to the diameter just to appear nicer as
        # a default thickness in the presentation
        self.diameter = kwargs.get("diameter", 0.1 + 0.02)
        self.thickness = kwargs.get("thickness", 0.01 + 0.02)

    def get_points(self):
        return [self.start, self.end]

    def set_diameter(self, diameter, *args):
        self.diameter = diameter

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.flange_actor import FlangeActor

        return FlangeActor(self)

    def __hash__(self) -> int:
        return id(self)

    def replace_point(self, old, new):
        if self.position == old:
            self.start = new
