from dataclasses import dataclass

import numpy as np

from .point import Point
from .structure import Structure


class Flange(Structure):
    def __init__(self, position: Point, normal: np.ndarray, **kwargs) -> None:
        super().__init__(**kwargs)

        self.position = position
        self.normal = normal
        self.diameter = kwargs.get("diameter", 0.1)
        self.thickness = kwargs.get("thickness", 0.01)
        self.auto = kwargs.get("auto", True)

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
        if self.position == old:
            self.start = new
