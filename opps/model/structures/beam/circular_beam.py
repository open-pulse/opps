from dataclasses import dataclass

from opps.model.structures.point import Point

from .beam import Beam


@dataclass
class CircularBeam(Beam):
    start: Point
    end: Point
    diameter: float = 0.1
    thickness: float = 0.01

    def get_points(self):
        return [self.start, self.end]

    def as_vtk(self):
        from opps.interface.viewer_3d.actors import CircularBeamActor

        return CircularBeamActor(self)

    def __hash__(self) -> int:
        return id(self)
