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
        self.staged_structures = []
        self.backup = []

    def set_deltas(self, deltas):
        self.deltas = np.array(deltas)

    def add_pipe(self):    
        self.dismiss()

        if (self.deltas == (0,0,0)).all():
            return
        
        connected_pipes = self.pipeline.find_pipes_at(self.current_point)
        self.backup.extend(connected_pipes)
        for structure in connected_pipes:
            self.pipeline.remove_structure(structure)
        
        new_pipe = Pipe(self.current_point, self.current_point + self.deltas)
        new_pipe.color = (255, 0, 0)
        self.staged_structures.append(new_pipe)
        
        connected_pipes_copy = deepcopy(connected_pipes)
        # connected_pipes_copy = connected_pipes
        if connected_pipes_copy:
            existing_pipe = connected_pipes_copy[0]
            bend = self.pipeline.connect_pipes_with_bend(new_pipe, existing_pipe, new_pipe.radius)
            if bend is not None:
                bend.color = (255, 0, 0)
                self.staged_structures.append(bend)
            self.staged_structures.append(existing_pipe)

        for structure in self.staged_structures:
            self.pipeline.add_structure(structure)

    def add_flange(self):
        new_flange = Flange(self.current_point)
        # self.control_points_to_structure[tuple(self.current_point)].append(new_flange)
        # self.structure_to_control_points[new_flange].append(new_flange)
    
    def dismiss(self):
        for structure in self.staged_structures:
            self.pipeline.remove_structure(structure)
        self.staged_structures.clear()
        
        for structure in self.backup:
            self.pipeline.add_structure(structure)
        self.backup.clear()

    def commit(self):
        self.current_point = self.current_point + self.deltas
        for structure in self.staged_structures:
            structure.color = (255, 255, 255)
        self.staged_structures.clear()
        self.backup.clear()

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
