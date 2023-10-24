from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass

import numpy as np

from opps.model import Bend, Elbow, Flange, Pipe, Pipeline


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
        self.staged_structures.extend(connected_pipes_copy)
        bends = self.add_joints(self.staged_structures)
        for bend in bends:
            bend.color = (255, 0, 0)

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
        self.control_points_to_structure.clear()
        pipes = [i for i in self.pipeline.components if isinstance(i, Pipe)]
        joints = [i for i in self.pipeline.components if isinstance(i, Bend)]

        for pipe in pipes:
            self.control_points_to_structure[tuple(pipe.start)].append(pipe)
            self.control_points_to_structure[tuple(pipe.end)].append(pipe)

        for joint in joints:
            start_structures = self.control_points_to_structure.pop(tuple(joint.start), None)
            end_structures = self.control_points_to_structure.pop(tuple(joint.end), None)
            merged_structures = [joint] + start_structures + end_structures
            self.control_points_to_structure[tuple(joint.get_corner())] = merged_structures
        
    def add_joints(self, structures):
        pipe_groups = defaultdict(list)
        pipes = [i for i in structures if isinstance(i, Pipe)]
        bends = []

        for pipe in pipes:
            pipe_groups[tuple(pipe.start)].append(pipe)
            pipe_groups[tuple(pipe.end)].append(pipe)

        for pipe_group in pipe_groups.values():
            if len(pipe_group) != 2:
                continue
            bend = self.connect_pipes_with_bend(*pipe_group)
            if bend is not None:
                bends.append(bend)

        structures.extend(bends)

        return bends
    
    def connect_pipes_with_bend(self, pipe_a, pipe_b):
        # avoid configurations like ← → or → ←
        if (pipe_a.start == pipe_b.end).all():
            pipe_a, pipe_b = pipe_b, pipe_a
        elif (pipe_a.end == pipe_b.end).all():
            pipe_b.start, pipe_b.end = pipe_b.end, pipe_b.start
        elif (pipe_a.start == pipe_b.start).all():
            pipe_a.start, pipe_a.end = pipe_a.end, pipe_a.start

        bend = Bend(start=pipe_a.start, 
                    end=pipe_b.end, 
                    corner=pipe_a.end,
                    curvature=pipe_a.radius)

        if np.isnan(bend.center).any():
            return None

        pipe_a.end = bend.start
        pipe_b.start = bend.end
        return bend

    def remove_joints(self, structures):
        joints = [i for i in structures if isinstance(i, Bend)]
        pipes = [i for i in structures if isinstance(i, Pipe)]

        indexes_to_remove = []
        for i, s in enumerate(structures):
            if isinstance(s, Bend):
                indexes_to_remove.append(i)
        indexes_to_remove.sort(reverse=True)

        for i in indexes_to_remove:
            structures.pop(i)

        replace_dict = dict()
        for joint in joints:
            replace_dict[tuple(joint.start)] = joint.get_corner()
            replace_dict[tuple(joint.end)] = joint.get_corner()

        for pipe in pipes:
            pipe.start = np.array(replace_dict.get(tuple(pipe.start), pipe.start))
            pipe.end = np.array(replace_dict.get(tuple(pipe.end), pipe.end))