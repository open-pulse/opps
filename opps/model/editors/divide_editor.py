from itertools import pairwise
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
    def divide_structures(self, t: float):
        for structure in self.pipeline.selected_structures:
            point = self._interpolate(structure, t)
            self._divide_on_point(structure, point)
        self.pipeline.commit()

    def divide_structures_evenly(self, divisions: int):
        for structure in self.pipeline.selected_structures:
            self._divide_evenly(structure, divisions)
        self.pipeline.commit()
    
    def preview_divide_structures(self, t: float):
        all_points = []
        for structure in self.pipeline.selected_structures:
            point = self._interpolate(structure, t)
            if point is not None:
                all_points.append(point)
        self.pipeline.add_points(all_points)

    def preview_divide_structures_evenly(self, divisions: int):
        all_points = []
        for structure in self.pipeline.selected_structures:
            points = self._interpolate_evenly(structure, divisions)
            all_points.extend(points)
        self.pipeline.add_points(all_points)

    def _divide_on_point(self, structure: Structure, point: Point):
        if isinstance(structure, LinearStructure):
            new_structure = structure.copy()
            structure.end = point
            new_structure.start = point
            self.pipeline.add_structure(new_structure)

    def _divide_evenly(self, structure: Structure, divisions: int):
        structures = [structure] + [structure.copy() for i in range(divisions)]
        points = self._interpolate_evenly(structure, divisions)

        for i, (a, b) in enumerate(pairwise(structures)):
            if isinstance(structure, LinearStructure):
                a: LinearStructure
                b: LinearStructure
                point = points[i]

                a.end = point
                b.start = point
        
        self.pipeline.add_structures(structures)

    def _interpolate(self, structure: Structure, t: float) -> Point | None:
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
