from dataclasses import dataclass

from opps.model.structures.point import Point

from .beam import Beam


class RectangularBeam(Beam):
    def __init__(self, start: Point, end: Point, **kwargs) -> None:
        super().__init__(**kwargs)

        self.start = start
        self.end = end
        self.width = kwargs.get("width", 0.1)
        self.height = kwargs.get("height", 0.1)
        self.thickness = kwargs.get("thickness", 0.01)

    def get_points(self):
        return [self.start, self.end]

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "start": self.start,
            "end": self.end,
            "height": self.height,
            "width": self.width,
            "thickness": self.thickness,
        }

    def as_vtk(self):
        from opps.interface.viewer_3d.actors import RectangularBeamActor

        return RectangularBeamActor(self)

    def __hash__(self) -> int:
        return id(self)
