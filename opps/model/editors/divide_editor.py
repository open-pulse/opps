from itertools import pairwise

from opps.model import (
    Structure,
    LinearStructure,
    SimpleCurve,
    Point,
)

from .editor import Editor


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
        
        elif isinstance(structure, SimpleCurve):
            center = structure.center
            corner = structure.corner.copy()
            new_structure = structure.copy()

            structure.end = point
            structure.update_corner_from_center(center)

            new_structure.start = point
            new_structure.update_corner_from_center(center)

            self.pipeline.add_structure(new_structure)
            self.pipeline.add_point(corner)

    def _divide_evenly(self, structure: Structure, divisions: int):
        structures = [structure] + [structure.copy() for i in range(divisions)]
        points = self._interpolate_evenly(structure, divisions)

        corner = None
        if isinstance(structure, SimpleCurve):
            corner = structure.corner.copy()

        for i, (a, b) in enumerate(pairwise(structures)):
            if isinstance(structure, LinearStructure):
                a: LinearStructure
                b: LinearStructure
                point = points[i]

                a.end = point
                b.start = point
            
            elif isinstance(structure, SimpleCurve):
                a: SimpleCurve
                b: SimpleCurve
                point = points[i]

                center = a.center

                a.end = point
                a.update_corner_from_center(center)

                b.start = point
                b.update_corner_from_center(center)

        self.pipeline.add_structures(structures)
        if corner is not None:
            self.pipeline.add_point(corner)

    def _interpolate(self, structure: Structure, t: float) -> Point | None:
        if isinstance(structure, LinearStructure | SimpleCurve):
            return structure.interpolate(t)

    def _interpolate_evenly(self, structure: Structure, divisions: int) -> list[Point]:
        subdivisions = []
        for i in range(divisions):
            t = (i + 1) / (divisions + 1)
            point = self._interpolate(structure, t)
            if point is None:
                return []
            subdivisions.append(point)
        return subdivisions
