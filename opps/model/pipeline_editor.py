from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, fields

import numpy as np

from opps.model import Bend, Elbow, Flange, Pipe, Pipeline, Point


class PipelineEditor:
    def __init__(self, pipeline: Pipeline, origin=(0.0, 0.0, 0.0)):
        self.pipeline = pipeline

        self.origin = Point(*origin)
        self.control_points = [self.origin]
        self.deltas = np.array([0, 0, 0])
        self.active_point = self.control_points[0]

        self.default_diameter = 0.2
        self.staged_structures = []

    def set_active_point(self, index):
        self.active_point = self.control_points[index]

    def set_deltas(self, deltas):
        self.deltas = np.array(deltas)

    def move_point(self, position):
        self.active_point.set_coords(*position)

    def remove_structure(self, structure, rejoin=True):
        if rejoin and isinstance(structure, Bend | Elbow):
            structure.colapse()

        index = self.pipeline.structures.index(structure)
        if index >= 0:
            self.pipeline.structures.pop(index)

    def morph(self, structure, new_type):
        params = self._structure_params(structure)
        new_structure = new_type(**params)

        self.remove_structure(structure)
        self.pipeline.add_structure(new_structure)
        return new_structure

    def commit(self):
        self._update_control_points()
        for structure in self.pipeline.structures:
            structure.staged = False
        self.staged_structures.clear()

    def dismiss(self):
        staged_points = []
        for structure in self.staged_structures:
            staged_points.extend(structure.get_points())
            self.remove_structure(structure)
        self.staged_structures.clear()
        self._update_joints()
        self._update_control_points()

        control_hashes = set(self.control_points)
        if self.active_point in control_hashes:
            return

        for point in staged_points:
            if point in control_hashes:
                self.active_point = point
                break
        else:
            self.set_active_point(-1)

    def change_diameter(self, diameter):
        self.default_diameter = diameter

    def get_diameters_at_point(self):
        diameters = []
        for structure in self.pipeline.structures:
            if self.active_point in structure.get_points():
                diameters.extend(structure.get_diameters())
        return diameters

    def add_pipe(self, deltas=None):
        if deltas != None:
            self.deltas = deltas

        current_point = self.active_point
        next_point = Point(*(current_point.coords() + self.deltas))

        new_pipe = Pipe(current_point, next_point)
        new_pipe.set_diameter(self.default_diameter)

        self.add_structure(new_pipe)
        self.active_point = next_point
        return new_pipe

    def add_bend(self, curvature_radius=0.3):
        start_point = self.active_point
        end_point = deepcopy(start_point)
        corner_point = deepcopy(start_point)

        # If a joint already exists morph it into a Bend
        for joint in self.pipeline.structures:
            if not isinstance(joint, Bend | Elbow):
                continue
            if joint.corner == start_point:
                return self.morph(joint, Bend)

        new_bend = Bend(start_point, end_point, corner_point, curvature_radius)
        new_bend.set_diameter(self.default_diameter)
        self.add_structure(new_bend)
        self.active_point = end_point
        return new_bend

    def add_elbow(self, curvature_radius=0.3):
        start_point = self.active_point
        end_point = deepcopy(start_point)
        corner_point = deepcopy(start_point)

        # If a joint already exists morph it into an Elbow
        for joint in self.pipeline.structures:
            if not isinstance(joint, Bend | Elbow):
                continue
            if joint.corner == start_point:
                return self.morph(joint, Elbow)

        new_elbow = Elbow(start_point, end_point, corner_point, curvature_radius)
        new_elbow.set_diameter(self.default_diameter)
        self.add_structure(new_elbow)
        self.active_point = end_point
        return new_elbow

    def add_flange(self):
        for flange in self.pipeline.structures:
            if not isinstance(flange, Flange):
                continue
            if flange.position == self.active_point:
                return flange

        new_flange = Flange(self.active_point, normal=np.array([1, 0, 0]))
        new_flange.set_diameter(self.default_diameter)
        self.add_structure(new_flange)
        return new_flange

    def add_bent_pipe(self, deltas=None, curvature_radius=0.3):
        self.add_bend(curvature_radius)
        return self.add_pipe(deltas)

    def add_structure(self, structure):
        structure.staged = True
        self.pipeline.add_structure(structure)
        self.staged_structures.append(structure)
        self._update_joints()
        self._update_control_points()
        return structure

    def _update_joints(self):
        self._update_curvatures()
        self._update_flanges()

    def _update_curvatures(self):
        for joint in self.pipeline.structures:
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
                joint.colapse()
                continue

            oposite_a, oposite_b, *_ = connected_points
            joint.normalize_values(oposite_a, oposite_b)

    def _update_flanges(self):
        for flange in self.pipeline.structures:
            if not isinstance(flange, Flange):
                continue

            if not flange.auto:
                continue

            connected_points = self._connected_points(flange.position)
            if not connected_points:
                continue

            oposite_a, *_ = connected_points
            flange.normal = flange.position.coords() - oposite_a.coords()

    def _update_control_points(self):
        control_points = list()
        for structure in self.pipeline.structures:
            if isinstance(structure, Bend | Elbow):
                continue
            control_points.extend(structure.get_points())

        point_to_index = {v: i for i, v in enumerate(control_points)}
        indexes_to_remove = []

        for structure in self.pipeline.structures:
            if not isinstance(structure, Bend | Elbow):
                continue

            if (structure.start in point_to_index) and (structure.end in point_to_index):
                indexes_to_remove.append(point_to_index[structure.start])
                indexes_to_remove.append(point_to_index[structure.end])
                control_points.append(structure.corner)

            elif structure.start in point_to_index:
                indexes_to_remove.append(point_to_index[structure.start])
                control_points.append(structure.end)

            elif structure.end in point_to_index:
                indexes_to_remove.append(point_to_index[structure.end])
                control_points.append(structure.start)

            else:
                control_points.append(structure.end)
                control_points.append(structure.start)
                control_points.append(structure.corner)

        for i in sorted(indexes_to_remove, reverse=True):
            control_points.pop(i)

        if not control_points:
            control_points.append(self.origin)

        self.control_points = list(control_points)

    def _connected_points(self, point):
        oposite_points = []
        for pipe in self.pipeline.structures:
            if not isinstance(pipe, Pipe):
                continue

            if id(pipe.start) == id(point):
                oposite_points.append(pipe.end)

            elif id(pipe.end) == id(point):
                oposite_points.append(pipe.start)

        return oposite_points

    def _structure_params(self, structure):
        """
        Get the params that can create a similar structure.
        It only works if the structure is a dataclass.
        """
        return {field.name: getattr(structure, field.name) for field in fields(structure)}
