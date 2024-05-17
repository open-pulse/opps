from .editor import Editor
from opps.model import (
    LinearStructure,
    Bend, 
    Elbow,
    CBeam,
    CircularBeam,
    ExpansionJoint,
    Flange,
    IBeam,
    Pipe,
    RectangularBeam,
    Reducer,
    TBeam,
    Valve,
    Structure,
    Beam,
    Pipeline,
    Point, 
)


class DivideEditor(Editor):
    def divide_on_point(self, structure: Structure, point: Point):        
        if isinstance(structure, LinearStructure):
            new_structure = structure.copy()
            structure.end = point
            new_structure.start = point
            self.pipeline.add_structure(new_structure)

    def divide_evenly(self, strucutre: Structure, divisions: int):
        pass

    def interpolate_point(self, a: Point, b: Point, t: float) -> Point:
        return a + t * (b - a)

    def interpolate_evenly(self, a: Point, b: Point, divisions: int) -> list[Point]:
        subdivisions = []
        for i in range(divisions):
            t = (i + 1) / (divisions + 1)
            point = self.interpolate_point(a, b, t)
            subdivisions.append(point)
        return subdivisions
