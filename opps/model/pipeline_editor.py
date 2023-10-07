from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass

import numpy as np

from opps.model import Bend, Flange, Pipe, Pipeline


class PipelineEditor:
    def __init__(self, origin=(0, 0, 0)):
        self.control_points_to_structure = defaultdict(list)
        self.structure_to_control_points = defaultdict(list)

        self.current_point = np.array(origin)
        self.deltas = np.array(origin)

        self.pipeline = Pipeline()
        self.staged_structure = []

    def set_deltas(self, deltas):
        self.deltas = np.array(deltas)

    def add_pipe(self):    
        for structure in self.staged_structure:
            self.pipeline.remove_structure(structure)

        if (self.deltas == (0,0,0)).all():
            return
    
        new_pipe = Pipe(self.current_point, self.current_point + self.deltas)
        self.control_points_to_structure[tuple(self.current_point)].append(new_pipe)
        self.structure_to_control_points[id(new_pipe)].append(new_pipe)
        self.pipeline.add_structure(new_pipe)
        self.staged_structure.append(new_pipe)

    def add_flange(self):
        new_flange = Flange(self.current_point)
        # self.control_points_to_structure[tuple(self.current_point)].append(new_flange)
        # self.structure_to_control_points[new_flange].append(new_flange)
    
    def commit(self):
        self.current_point = self.current_point + self.deltas
        self.staged_structure.clear()

    def reposition_structure(self, obj):
        if isinstance(obj, Pipe):
            self.reposition_pipe(obj)
        elif isinstance(obj):
            self.reposition_flange(obj)
        else:
            raise ValueError("OPSI")

    def reposition_pipe(self, pipe: Pipe):
        pipe.start = self.current_point
        pipe.end = pipe.start + self.deltas

    def reposition_flange(self, flange: Flange):
        flange.position = flange

    def move_control_point(self, origin, target):
        origin_structures = self.control_points_to_structure[origin]
        # do stuff...

    def recalculate_control_points(self):
        pass
