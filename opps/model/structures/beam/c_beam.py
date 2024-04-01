from dataclasses import KW_ONLY, dataclass

from opps.model.structures.point import Point

from .beam import Beam


@dataclass
class CBeam(Beam):
    start: Point
    end: Point
    _: KW_ONLY
    height: float = 0.1
    width_1: float = 0.1
    width_2: float = 0.1
    thickness_1: float = 0.01
    thickness_2: float = 0.01
    thickness_3: float = 0.01

    def get_points(self):
        return [self.start, self.end]

    def as_vtk(self):
        from opps.interface.viewer_3d.actors import CBeamActor

        return CBeamActor(self)

    def __hash__(self) -> int:
        return id(self)
