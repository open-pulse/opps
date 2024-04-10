from dataclasses import KW_ONLY, dataclass

from opps.model.structures.point import Point

from .beam import Beam


class IBeam(Beam):
    def __init__(self, start: Point, end: Point, **kwargs) -> None:
        super().__init__(**kwargs)

        self.start = start
        self.end = end
        self.height = kwargs.get("height", 0.1)
        self.width_1 = kwargs.get("width_1", 0.1)
        self.width_2 = kwargs.get("width_2", 0.1)
        self.thickness_1 = kwargs.get("thickness_1", 0.01)
        self.thickness_2 = kwargs.get("thickness_2", 0.01)
        self.thickness_3 = kwargs.get("thickness_3", 0.01)

    def get_points(self):
        return [self.start, self.end]

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "start": self.start,
            "end": self.end,
            "height": self.height,
            "width_1": self.width_1,
            "width_2": self.width_2,
            "thickness_1": self.thickness_1,
            "thickness_2": self.thickness_2,
            "thickness_3": self.thickness_3,
        }

    def as_vtk(self):
        from opps.interface.viewer_3d.actors import IBeamActor

        return IBeamActor(self)

    def __hash__(self) -> int:
        return id(self)
