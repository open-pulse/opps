from dataclasses import dataclass
from opps.model.structures.point import Point
from .beam import Beam


@dataclass
class RectangularBeam(Beam):
    start: Point
    end: Point
    width: float = 0.1
    height: float = 0.1
    thickness: float = 0.01

    def get_points(self):
        return [self.start, self.end]

    def as_vtk(self):
        from opps.interface.viewer_3d.actors import RectangularBeamActor

        return RectangularBeamActor(self)

    def __hash__(self) -> int:
        return id(self)

