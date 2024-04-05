from dataclasses import KW_ONLY, dataclass

from opps.model.structures.point import Point

from .beam import Beam


@dataclass
class TBeam(Beam):
    def __init__(self, start: Point, end: Point, **kwargs) -> None:
        super().__init__(**kwargs)

        self.start = start
        self.end = end
        self.width = kwargs.get("width", 0.1)
        self.height = kwargs.get("height", 0.1)
        self.thickness_1 = kwargs.get("thickness_1", 0.01)
        self.thickness_2 = kwargs.get("thickness_2", 0.01)

    def get_points(self):
        return [self.start, self.end]

    def as_vtk(self):
        from opps.interface.viewer_3d.actors import TBeamActor

        return TBeamActor(self)

    def __hash__(self) -> int:
        return id(self)
