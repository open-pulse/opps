from .point import Point
from .structure import Structure


class Valve(Structure):
    def __init__(self, start: Point, end: Point, **kwargs) -> None:
        super().__init__(**kwargs)

        self.start = start
        self.end = end
        self.diameter = kwargs.get("diameter", 0.1)
        self.thickness = kwargs.get("thickness", 0.01)
        self.flange_outer_diameter = kwargs.get("flange_outer_diameter", 0.2)
        self.flange_length = kwargs.get("flange_length", 0.05)

    def get_points(self) -> list[Point]:
        return [self.start, self.end]

    def replace_point(self, old, new):
        if self.start == old:
            self.start = new

        elif self.end == old:
            self.end = new

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "start": self.start,
            "end": self.end,
            "diameter": self.diameter,
            "thickness": self.thickness,
        }

    def as_vtk(self):
        from opps.interface.viewer_3d.actors import ValveActor

        return ValveActor(self)

    def __hash__(self) -> int:
        return id(self)
