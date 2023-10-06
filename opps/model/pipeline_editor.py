from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass

import numpy as np

from opps.model import Bend, Flange, Pipe, Pipeline


class PipelineEditor:
    def __init__(self, origin=(0, 0, 0)):
        self.control_points_to_structure = defaultdict(list)
        self.structure_to_control_points = defaultdict(list)

        self.origin = np.array(origin)
        self.current_point = np.array(origin)
        self.next_point = np.array(origin)

        self.pipeline = Pipeline()
        self.staged_structure = None

    def set_deltas(self, deltas):
        self.next_point = self.current_point + deltas

    def add_pipe(self):
        new_pipe = Pipe(self.current_point, self.next_point)
        self.control_points_to_structure[self.current_point].append(new_pipe)
        self.structure_to_control_points[new_pipe].append(new_pipe)

    def add_flange(self):
        new_flange = Flange(self.current_point)
        self.control_points_to_structure[self.current_point].append(new_flange)
        self.structure_to_control_points[new_flange].append(new_flange)

    def reposition_structure(self, obj):
        if isinstance(obj, Pipe):
            self.reposition_pipe(obj)
        elif isinstance(obj):
            self.reposition_flange(obj)
        else:
            raise ValueError("OPSI")

    def reposition_pipe(self, pipe: Pipe):
        pipe.start = self.current_point
        pipe.end = self.next_point

    def reposition_flange(self, flange: Flange):
        flange.position = flange

    def move_control_point(self, origin, target):
        origin_structures = self.control_points_to_structure[origin]
        # do stuff...

    def recalculate_control_points(self):
        pass
