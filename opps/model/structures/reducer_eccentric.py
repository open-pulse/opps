from dataclasses import dataclass

from .point import Point
from .structure import Structure


@dataclass
class ReducerEccentric(Structure):
    def __init__(self, start: Point, end: Point, **kwargs) -> None:
        super().__init__(**kwargs)

        self.start = start
        self.end = end
        self.offset_y = kwargs.get("offset_y", 0.025)
        self.offset_z = kwargs.get("offset_z", 0)
        self.initial_diameter = kwargs.get("initial_diameter", 0.1)
        self.final_diameter = kwargs.get("final_diameter", 0.05)
        self.thickness = kwargs.get("thickness", 0.01)

    def get_points(self):
        return [self.start, self.end]

    def as_vtk(self):
        from opps.interface.viewer_3d.actors import ReducerEccentricActor

        return ReducerEccentricActor(self)

    def __hash__(self) -> int:
        return id(self)
