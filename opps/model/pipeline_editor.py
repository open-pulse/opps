from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass

import numpy as np

from opps.model import Bend, Elbow, Flange, Pipe, Pipeline, Point


class PipelineEditor:
    def __init__(self, origin=(0, 0, 0)):
        self.pipeline = Pipeline()
        self.deltas = np.array([0,0,0])
        self.control_points = [Point(0,0,0)]
        self.active_point = self.control_points[0]

        self.default_diameter = 0.2
        self.selection_color = (247, 0, 20)

        self.staged_structures = []

    def set_active_point(self, index):
        self.active_point = self.control_points[index]

    def set_deltas(self, deltas):
        self.deltas = np.array(deltas)

    def move_point(self, position):
        self.active_point.set_coords(*position)

    def change_diameter(self, diameter):
        self.default_diameter = diameter
        for structure in self.pipeline.components:
            structure.set_diameter(diameter, point=self.active_point)

    def add_pipe(self, deltas=None):
        if deltas != None:
            self.deltas = deltas

        current_point = self.active_point
        next_point = Point(*(current_point.coords() + self.deltas))

        new_pipe = Pipe(
            current_point, 
            next_point,
            color=self.selection_color
        )
        new_pipe.set_diameter(self.default_diameter)

        self.add_structure(new_pipe)
        self.active_point = next_point
        return new_pipe

    def add_bend(self, curvature_radius=0.3):
        start_point = self.active_point
        end_point = deepcopy(start_point)
        corner_point = deepcopy(start_point)

        # Reuse joints if it already exists
        # Actually it should replace the existing joint
        for joint in self.pipeline.components:
            if not isinstance(joint, Bend | Elbow):
                continue
            if joint.corner == start_point:
                return joint

        new_bend = Bend(
            start_point,
            end_point,
            corner_point,
            curvature_radius,
            color=self.selection_color
        )
        new_bend.set_diameter(self.default_diameter)
        self.add_structure(new_bend)
        self.active_point = end_point
        return new_bend

    def add_elbow(self, curvature_radius=0.3):
        start_point = self.active_point
        end_point = deepcopy(start_point)
        corner_point = deepcopy(start_point)

        # Reuse joints if it already exists
        # Actually it should replace the existing joint
        for joint in self.pipeline.components:
            if not isinstance(joint, Bend | Elbow):
                continue
            if joint.corner == start_point:
                return joint

        new_elbow = Elbow(
            start_point,
            end_point,
            corner_point,
            curvature_radius,
            color=self.selection_color
        )
        new_elbow.set_diameter(self.default_diameter)
        self.add_structure(new_elbow)
        self.active_point = end_point
        return new_elbow
    
    def add_flange(self):
        for flange in self.pipeline.components:
            if not isinstance(flange, Flange):
                continue
            if flange.position == self.active_point:
               return flange

        new_flange = Flange(
            self.active_point,
            normal=np.array([1,0,0]),
            color=self.selection_color
        )
        new_flange.set_diameter(self.default_diameter)
        self.add_structure(new_flange)
        return new_flange

    def add_bent_pipe(self, deltas=None, curvature_radius=0.3):
        self.add_bend(curvature_radius)
        return self.add_pipe(deltas)
    
    def add_structure(self, structure):
        self.pipeline.add_structure(structure)
        self.staged_structures.append(structure)
        self._update_joints() 
        self._update_control_points()
        return structure

    def _update_joints(self):
        self._update_curvatures()
        self._update_flanges()

    def _update_curvatures(self):
        for joint in self.pipeline.components:
            if not isinstance(joint, Bend | Elbow):
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
        for flange in self.pipeline.components:
            if not isinstance(flange, Flange):
                continue
            
            connected_points = self._connected_points(flange.position) 
            if not connected_points:
                continue

            oposite_a, *_ = connected_points
            flange.normal = flange.position.coords() - oposite_a.coords()

    def _update_control_points(self):
        control_points = list()
        for structure in self.pipeline.components:
            if isinstance(structure, Bend | Elbow):
                control_points.append(structure.corner)
                continue
            control_points.extend(structure.get_points())

        point_to_index = {v:i for i, v in enumerate(control_points)}
        indexes_to_remove = []

        for structure in self.pipeline.components:
            if not isinstance(structure, Bend | Elbow):
                continue

            if structure.start in point_to_index:
                indexes_to_remove.append(point_to_index[structure.start])
            else:
                control_points.append(structure.start)

            if structure.end in point_to_index:
                indexes_to_remove.append(point_to_index[structure.end])
            else:
                control_points.append(structure.end)

        for i in sorted(indexes_to_remove, reverse=True):
            control_points.pop(i)

        self.control_points = list(control_points)

    def _connected_points(self, point):
        oposite_points = []
        for pipe in self.pipeline.components:
            if not isinstance(pipe, Pipe):
                continue

            if id(pipe.start) == id(point):
                oposite_points.append(pipe.end)

            elif id(pipe.end) == id(point):
                oposite_points.append(pipe.start)
        
        return oposite_points

    def remove_structure(self, structure):
        if isinstance(structure, Bend | Elbow):
            structure.colapse()
        index = self.pipeline.components.index(structure)
        if index >= 0:
            self.pipeline.components.pop(index)

    def commit(self):
        self._update_control_points()
        for structure in self.staged_structures:
            structure.color = (255, 255, 255)
        self.staged_structures.clear()

    def dismiss(self):
        for structure in self.staged_structures:
            self.remove_structure(structure)
        self.staged_structures.clear()
        self._update_control_points()
