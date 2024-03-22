from itertools import pairwise

import numpy as np

from .bend import Bend
from .elbow import Elbow
from .flange import Flange
from .pipe import Pipe
from .point import Point
from .structure import Structure
from .beam import Beam


class Pipeline(Structure):
    def __init__(self):
        self.origin = Point(0, 0, 0)
        self.structures: list[Structure] = []
        self.points: list[Point] = []
        self.control_points: list[Point] = []

    # Essential functions
    def add_point(self, point: Point):
        self.points.append(point)

    def add_structure(self, structure: Structure):
        self.structures.append(structure)

    def remove_point(self, point: Point):
        for i in self.get_point_indexes(point):
            self.points.pop(i)

    def remove_structure(self, structure: Structure):
        for i in self.get_structure_indexes(structure):
            self.structures.pop(i)

    # Essential functions plural
    def add_points(self, points: list[Point]):
        for point in points:
            self.add_point(point)

    def add_structures(self, structures: list[Structure]):
        for structure in structures:
            self.add_structure(structure)

    def remove_points(self, points: list[Point]):
        for point in points:
            self.remove_point(point)

    def remove_structures(self, structures: list[Structure]):
        for structure in structures:
            self.remove_structure(structure)

    def get_point_indexes(self, point: Point):
        indexes = []
        for i, s in enumerate(self.points):
            if id(s) == id(point):
                indexes.append(i)
        indexes.reverse()
        return indexes

    def get_structure_indexes(self, structure: Structure):
        indexes = []
        for i, s in enumerate(self.structures):
            if id(s) == id(structure):
                indexes.append(i)
        indexes.reverse()
        return indexes
    
    # Utils
    def as_vtk(self):
        from opps.interface.viewer_3d.actors.pipeline_actor import (
            PipelineActor,
        )

        return PipelineActor(self)

    def __hash__(self) -> int:
        return id(self)






    def _update_flanges(self):
        for flange in self.structures:
            if not isinstance(flange, Flange):
                continue

            if not flange.auto:
                continue

            connected_points = self._connected_points(flange.position)
            if not connected_points:
                continue

            oposite_a, *_ = connected_points
            flange.normal = flange.position.coords() - oposite_a.coords()

    def _update_curvatures(self):
        # First colapse all joint that can be colapsed.
        # This prevents cases were a normalization of a
        # joint disturbs the normalization of others.
        for joint in self.structures:
            if not isinstance(joint, Bend | Elbow):
                continue

            if not joint.auto:
                continue

            joint.colapse()

        for joint in self.structures:
            if not isinstance(joint, Bend | Elbow):
                continue

            if not joint.auto:
                continue

            connected_points = (
                self._connected_points(joint.start)
                + self._connected_points(joint.end)
                + self._connected_points(joint.corner)
            )

            if len(connected_points) != 2:
                continue

            oposite_a, oposite_b, *_ = connected_points
            joint.normalize_values(oposite_a, oposite_b)

    def _update_points(self):
        points = list()
        control_points = list()
        for structure in self.structures:
            points.extend(structure.get_points())
            if not isinstance(structure, Pipe | Beam):
                continue
            control_points.extend(structure.get_points())

        point_to_index = {v: i for i, v in enumerate(control_points)}
        indexes_to_remove = []

        for structure in self.structures:
            if not isinstance(structure, Bend | Elbow):
                continue

            if not structure.auto:
                control_points.append(structure.corner)
                control_points.append(structure.end)
                control_points.append(structure.start)
                continue

            control_points.append(structure.corner)
            if structure.start in point_to_index:
                indexes_to_remove.append(point_to_index[structure.start])

            if structure.end in point_to_index:
                indexes_to_remove.append(point_to_index[structure.end])

        for i in sorted(indexes_to_remove, reverse=True):
            control_points.pop(i)

        if not control_points and not points:
            control_points.append(self.origin)
            points.append(self.origin)

        self.control_points = list(control_points)
        self.points = list(points)

    def _connected_points(self, point):
        oposite_points = []
        for pipe in self.structures:
            if not isinstance(pipe, Pipe):
                continue

            if id(pipe.start) == id(point):
                oposite_points.append(pipe.end)

            elif id(pipe.end) == id(point):
                oposite_points.append(pipe.start)

        return oposite_points

