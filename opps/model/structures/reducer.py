from dataclasses import dataclass

from .point import Point
from .structure import Structure


@dataclass
class Reducer(Structure):
    def __init__(self, start: Point, end: Point, **kwargs) -> None:
        super().__init__(**kwargs)

        self.start = start
        self.end = end
        self.initial_diameter = kwargs.get("initial_diameter", 0.1)
        self.final_diameter = kwargs.get("final_diameter", 0.05)
        self.initial_offset_y = kwargs.get("initial_offset_y", 0)
        self.initial_offset_z = kwargs.get("initial_offset_z", 0)
        self.final_offset_y = kwargs.get("final_offset_y", 0)
        self.final_offset_z = kwargs.get("final_offset_z", 0)
        self.thickness = kwargs.get("thickness", 0.01)

    def get_points(self):
        return [self.start, self.end]

    def replace_point(self, old, new):
        if self.start == old:
            self.start = new

        elif self.end == old:
            self.end = new

    def as_vtk(self):
        from opps.interface.viewer_3d.actors import ReducerActor

        return ReducerActor(self)

    def __hash__(self) -> int:
        return id(self)