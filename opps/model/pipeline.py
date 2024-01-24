from itertools import pairwise

import numpy as np

from opps.io.pcf.pcf_handler import *
from opps.model.bend import Bend
from opps.model.flange import Flange
from opps.model.pipe import Pipe
from opps.model.structure import Structure


class Pipeline(Structure):
    def __init__(self):
        self.structures: list[Structure] = []
        self.points: list[Point] = []
        self.control_points: list[Point] = []

    def load(self, path):
        with open(path, "r", encoding="iso_8859_1") as c2:
            lines = c2.readlines()
        groups = group_structures(lines)
        self.structures = create_classes(groups)

    def add_structure(self, structure, *, auto_connect=False):
        self.structures.append(structure)

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.pipeline_actor import (
            PipelineActor,
        )

        return PipelineActor(self)

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
            if not isinstance(structure, Pipe):
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

        if not control_points:
            origin = Point(0,0,0)
            control_points.append(origin)
            points.append(origin)

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

    def __hash__(self) -> int:
        return id(self)
