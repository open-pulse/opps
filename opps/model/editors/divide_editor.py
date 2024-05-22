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
    Point, 
)


class DivideEditor(Editor):
    def divide_structure(self, t:float):
        for structure in self.pipeline.selected_structures:
            if isinstance(structure, LinearStructure):
                point = self._interpolate(structure, t)
                self._divide_on_point(structure, point)
        self.pipeline.commit()

    def divide_structure_evenly(self, divisions:int):
        pass

    def _divide_on_point(self, structure: Structure, point: Point):
        if isinstance(structure, LinearStructure):
            new_structure = structure.copy()
            structure.end = point
            new_structure.start = point
            self.pipeline.add_structure(new_structure)

    def _divide_evenly(self, strucutre: Structure, divisions: int):
        pass

    def _interpolate(self, structure: Structure, t: float) -> Point:
        if isinstance(structure, LinearStructure):
            a = structure.start
            b = structure.end
            return a + t * (b - a)

    def _interpolate_evenly(self, structure: Structure, divisions: int) -> list[Point]:
        subdivisions = []
        for i in range(divisions):
            t = (i + 1) / (divisions + 1)
            point = self._interpolate(structure, t)
            subdivisions.append(point)
        return subdivisions
