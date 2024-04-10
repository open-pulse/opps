from dataclasses import dataclass

from opps.model.structures.point import Point

from .beam import Beam


class CircularBeam(Beam):
    def __init__(self, start: Point, end: Point, **kwargs) -> None:
        super().__init__(**kwargs)

        self.start = start
        self.end = end
        self.diameter = kwargs.get("diameter", 0.1)
        self.thickness = kwargs.get("thickness", 0.1)

    def get_points(self):
        return [self.start, self.end]

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "start": self.start,
            "end": self.end,
            "diameter": self.diameter,
            "thickness": self.thickness,
        }

    def as_vtk(self):
        from opps.interface.viewer_3d.actors import CircularBeamActor

        return CircularBeamActor(self)

    def __hash__(self) -> int:
        return id(self)
