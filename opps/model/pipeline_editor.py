from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass, fields

import numpy as np

from opps.model import Bend, Elbow, Flange, Pipe, Pipeline, Point
from opps.model.structure import Structure


class PipelineEditor:
    def __init__(self, pipeline: Pipeline, origin=(0.0, 0.0, 0.0)):
        self.pipeline = pipeline
        self.pipeline._update_points()

        self.deltas = np.array([0, 0, 0])
        self.anchor = self.pipeline.points[0]

        self.default_diameter = 0.2
        self.selected_points = []
        self.selected_structures = []
        self.staged_structures = []

    def set_anchor(self, point):
        self.anchor = point

    def set_deltas(self, deltas):
        self.deltas = np.array(deltas)

    def move_point(self, position):
        if self.anchor not in self.pipeline.control_points:
            return
        self.anchor.set_coords(*position)

    def remove_point(self, point, rejoin=True):
        if not isinstance(point, Point):
            return

        structures_to_remove = []
        for structure in self.pipeline.structures:
            if point in structure.get_points():
                structures_to_remove.append(structure)

        for structure in structures_to_remove:
            self.remove_structure(structure, rejoin)

    def remove_structure(self, structure, rejoin=True):
        if not isinstance(structure, Structure):
            return

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
        self.update()
        for structure in self.pipeline.structures:
            structure.staged = False
        self.staged_structures.clear()

    def dismiss(self):
        staged_points = []
        for structure in self.staged_structures:
            staged_points.extend(structure.get_points())
            self.remove_structure(structure)
        self.staged_structures.clear()
        self.update()

        control_hashes = set(self.pipeline.control_points)
        if self.anchor in control_hashes:
            return

        for point in staged_points:
            if point in control_hashes:
                self.anchor = point
                break
        else:
            self.set_anchor(self.pipeline.control_points[-1])

    def change_diameter(self, diameter):
        self.default_diameter = diameter

    def get_diameters_at_point(self):
        diameters = []
        for structure in self.pipeline.structures:
            if self.anchor in structure.get_points():
                diameters.extend(structure.get_diameters())
        return diameters

    def add_pipe(self, deltas=None):
        if deltas != None:
            self.deltas = deltas

        if self.anchor not in self.pipeline.control_points:
            return

        current_point = self.anchor
        next_point = Point(*(current_point.coords() + self.deltas))

        new_pipe = Pipe(current_point, next_point)
        new_pipe.set_diameter(self.default_diameter)

        self.add_structure(new_pipe)
        self.anchor = next_point
        return new_pipe

    def add_bend(self, curvature_radius=0.3):
        start_point = self.anchor
        end_point = deepcopy(start_point)
        corner_point = deepcopy(start_point)

        # If a joint already exists morph it into a Bend
        for joint in self.pipeline.structures:
            if not isinstance(joint, Bend | Elbow):
                continue
            if start_point in joint.get_points():
                new_bend = self.morph(joint, Bend)

                if not self.pipeline._connected_points(joint.start):
                    self.anchor = joint.start
                elif not self.pipeline._connected_points(joint.end):
                    self.anchor = joint.end
                else:
                    self.anchor = joint.corner

                return new_bend

        new_bend = Bend(start_point, end_point, corner_point, curvature_radius)
        new_bend.set_diameter(self.default_diameter)
        self.add_structure(new_bend)
        self.anchor = end_point
        return new_bend

    def add_elbow(self, curvature_radius=0.3):
        start_point = self.anchor
        end_point = deepcopy(start_point)
        corner_point = deepcopy(start_point)

        # If a joint already exists morph it into an Elbow
        for joint in self.pipeline.structures:
            if not isinstance(joint, Bend | Elbow):
                continue
            if joint.corner == start_point:
                new_elbow = self.morph(joint, Elbow)
            
                if not self.pipeline._connected_points(joint.start):
                    self.anchor = joint.start
                elif not self.pipeline._connected_points(joint.end):
                    self.anchor = joint.end
                else:
                    self.anchor = joint.corner

                return new_elbow

        new_elbow = Elbow(start_point, end_point, corner_point, curvature_radius)
        new_elbow.set_diameter(self.default_diameter)
        self.add_structure(new_elbow)
        self.anchor = end_point
        return new_elbow

    def add_flange(self):
        # If a flange already exists return it
        for flange in self.pipeline.structures:
            if not isinstance(flange, Flange):
                continue
            if flange.position == self.anchor:
                return flange

        # It avoids the placement of a flange in the middle of a bend.
        for joint in self.pipeline.structures:
            if not isinstance(joint, Bend | Elbow):
                continue
            if joint.corner == self.anchor:
                new_flange = Flange(joint.start, normal=np.array([1, 0, 0]))
                new_flange.set_diameter(self.default_diameter)
                self.add_structure(new_flange)
                return new_flange

        new_flange = Flange(self.anchor, normal=np.array([1, 0, 0]))
        new_flange.set_diameter(self.default_diameter)
        self.add_structure(new_flange)
        return new_flange

    def add_delta_pipe(self, deltas=None, curvature_radius=0.3):
        self.dismiss()

        if deltas != None:
            self.deltas = deltas

        if self.anchor not in self.pipeline.control_points:
            return

        if curvature_radius:
            self.add_bend(curvature_radius)
        self.add_pipe()

    def add_bent_pipe(self, deltas=None, curvature_radius=0.3):
        if self.anchor not in self.pipeline.control_points:
            return

        self.add_bend(curvature_radius)
        return self.add_pipe(deltas)

    def add_structure(self, structure):
        structure.staged = True
        self.pipeline.add_structure(structure)
        self.staged_structures.append(structure)
        self.update()
        return structure

    def update(self):
        self.pipeline._update_curvatures()
        self.pipeline._update_flanges()
        self.pipeline._update_points()

    def _structure_params(self, structure):
        """
        Get the params that can create a similar structure.
        It only works if the structure is a dataclass.
        """
        return {field.name: getattr(structure, field.name) for field in fields(structure)}
