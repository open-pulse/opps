from .point import Point
from .structure import Structure


class Valve(Structure):
    def __init__(self, start: Point, end: Point, **kwargs) -> None:
        super().__init__(**kwargs)

        self.start = start
        self.end = end
        self.diameter = kwargs.get("diameter", 0.1)
        self.thickness = kwargs.get("thickness", 0.01)

    def get_points(self) -> list[Point]:
        return [self.start, self.end]

    def as_vtk(self):
        from opps.interface.viewer_3d.actors import ValveActor

        return ValveActor(self)

    def __hash__(self) -> int:
        return id(self)
