from dataclasses import dataclass

import numpy as np

from .point import Point
from .structure import Structure


@dataclass
class ExpansionJoint(Structure):
    start: Point
    end: Point
    diameter: float = 0.1
    thickness: float = 0

    def get_points(self) -> list[Point]:
        return [self.start, self.end]

    def as_vtk(self):
        from opps.interface.viewer_3d.actors import ExpansionJointActor

        return ExpansionJointActor(self)

    def __hash__(self) -> int:
        return id(self)
