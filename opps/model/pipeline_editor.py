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

        self.staged_structures = []

    def set_active_point(self, index):
        self.active_point = self.control_points[index]

        print("points")
        for i, p in enumerate(self.control_points):
            bla = " "
            if id(p) == id(self.active_point):
                bla = "*"
            print(bla, i, p)
        print()


    def set_deltas(self, deltas):
        self.deltas = np.array(deltas)

    def move_point(self, index, position):
        if index < -len(self.control_points):
            return
        
        if index >= len(self.control_points):
            return

        self.control_points[index].set_coords(*position)

    def add_pipe(self, deltas=None):
        if deltas != None:
            self.deltas = deltas

        current_point = self.active_point
        next_point = Point(*(current_point.coords() + self.deltas))

        new_pipe = Pipe(
            current_point, 
            next_point,
            color=(255, 0, 0)
        )

        self.control_points.append(next_point)
        self.pipeline.add_structure(new_pipe)
        self.staged_structures.append(new_pipe)
        self.active_point = next_point
        return new_pipe

    def add_bend(self, curvature_radius=0.3):
        start_point = self.active_point
        end_point = deepcopy(start_point)
        corner_point = deepcopy(start_point)

        self.control_points.append(corner_point)
        self.control_points.append(end_point)

        # Reuse joints if it already exists
        for joint in self.pipeline.components:
            if not isinstance(joint, Bend):
                continue
            if joint.corner == start_point:
                return joint

        new_bend = Bend(
            start_point,
            end_point,
            corner_point,
            curvature_radius,
            color=(255, 0, 0)
        )
        self.pipeline.add_structure(new_bend)
        self.staged_structures.append(new_bend)
        self._update_joints() 
        self.active_point = end_point
        return new_bend
    
    def add_bent_pipe(self, deltas=None, curvature_radius=0.3):
        bend = self.add_bend(curvature_radius)
        # self.active_point = bend.end
        self.add_pipe(deltas)
        self._update_joints()
    
    def _update_joints(self):
        for joint in self.pipeline.components:
            if not isinstance(joint, Bend):
                continue
            
            connected_points = (
                self._connected_points(joint.start) 
                + self._connected_points(joint.end) 
                + self._connected_points(joint.corner)
            )

            print(len(connected_points))

            if len(connected_points) != 2:
                joint.colapse()
                continue

            oposite_a, oposite_b, *_ = connected_points
            joint.normalize_values_2(oposite_a, oposite_b)

    def _update_control_points(self):
        # It is leading a wrong behaviour
        # because sets aren't ordered

        control_points = set()
        for structure in self.pipeline.components:
            if isinstance(structure, Bend):
                continue
            control_points |= set(structure.get_points())

        for structure in self.pipeline.components:
            if not isinstance(structure, Bend):
                continue
            control_points.symmetric_difference_update([structure.start, structure.end])
            control_points.add(structure.corner)

        self.control_points = list(control_points)
        self.control_points.sort(key=tuple)

        print("Points")
        for i, p in enumerate(self.control_points):
            bla = " "
            if id(p) == id(self.active_point):
                bla = "*"
            print(bla, i, p)
        print()


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

    def commit(self):
        self._update_control_points()
        # self.set_active_point(-1)
        for structure in self.staged_structures:
            structure.color = (255, 255, 255)
        self.staged_structures.clear()

        # for i, p in enumerate(self.control_points):
        #     print(i, p)
        # print()

    def dismiss(self):
        for structure in self.staged_structures:
            index = self.pipeline.components.index(structure)
            if index >= 0:
                self.pipeline.components.pop(index)
        self.staged_structures.clear()
        self._update_control_points()

