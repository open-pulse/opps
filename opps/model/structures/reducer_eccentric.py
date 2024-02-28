from dataclasses import dataclass
from .structure import Structure
from .point import Point


@dataclass
class ReducerEccentric(Structure):
    start: Point
    end: Point
    offset_y: float = 0
    offset_z: float = 0
    start_diameter: float = 0.1
    end_diameter: float = 0.1
    thickness: float = 0.01

    def get_points(self):
        return [self.start, self.end]

    def as_vtk(self):
        from opps.interface.viewer_3d.actors import ReducerEccentricActor

        return ReducerEccentricActor(self)

    def __hash__(self) -> int:
        return id(self)
