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

    def set_active_point(self, index):
        self.active_point = self.control_points[index]

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

        current_point = self.control_points[-1]
        next_point = Point(*(current_point.coords() + self.deltas))

        new_pipe = Pipe(
            current_point, 
            next_point,
        )

        self.control_points.append(next_point)
        self.pipeline.add_structure(new_pipe)
        self._update_joints()

    def add_bend(self):
        start_point = self.control_points[-1]
        end_point = deepcopy(start_point)
        corner_point = deepcopy(start_point)

        self.control_points.append(corner_point)
        self.control_points.append(end_point)

        new_bend = Bend(
            start_point,
            end_point,
            corner_point,
            0.3
        )
        self.pipeline.add_structure(new_bend)
        self._update_joints() 
    
    def _update_joints(self):
        for joint in self.pipeline.components:
            if not isinstance(joint, Bend):
                continue
            
            connected_points = self._connected_points(joint.start) + self._connected_points(joint.end)
            if len(connected_points) < 2:
                continue

            oposite_a, oposite_b, *_ = connected_points
            # print(joint)
            joint.normalize_values_2(oposite_a, oposite_b)
            # print(joint)
            # print()

    def _connected_points(self, point):
        oposite_points = []
        for pipe in self.pipeline.components:
            if not isinstance(pipe, Pipe):
                continue

            if pipe.start == point:
                oposite_points.append(pipe.end)

            elif pipe.end == point:
                oposite_points.append(pipe.start)
        
        return oposite_points

    def commit(self):
        self.set_active_point(-1)
        for i, p in enumerate(self.control_points):
            print(i, p)
        print()

    def dismiss(self):
        pass
