from itertools import pairwise

import numpy as np

from opps.model.bend import Bend
from opps.model.flange import Flange
from opps.model.pipe import Pipe
from opps.io.pcf.pcf_reader import *


class Pipeline:
    def __init__(self):
        self.components = []

    def load(self, path):
        with open(path) as c2:
            lines = c2.readlines()
        groups = group_structures(lines)    
        self.components = create_classes(groups)
        print(self.components)

    def add_pipe(self, *args, **kwargs) -> Pipe:
        pipe = Pipe(*args, **kwargs)
        self.add_structure(pipe)
        return pipe

    def add_bend(self, *args, **kwargs) -> Bend:
        bend = Bend(*args, **kwargs)
        self.add_structure(bend)
        return bend

    def add_flange(self, *args, **kwargs) -> Flange:
        flange = Flange(*args, **kwargs)
        self.add_structure(flange)
        return flange

    def add_oriented_flange(self, position, *args, **kwargs):
        pipes_connected = self.find_pipes_at(position)
        if pipes_connected:
            pipe = pipes_connected[0]
            normal = pipe.end - pipe.start
        else:
            normal = (0, 1, 0)

        flange = Flange(position, normal, *args, **kwargs)
        self.add_structure(flange)

    def add_connected_pipe(self, *args, **kwargs):
        pipe = Pipe(*args, **kwargs)
        pipes = self.find_pipes_at(pipe.start)
        pipes.extend(self.find_pipes_at(pipe.end))
        existing_pipe, *_ = pipes

        bend = self.connect_pipes_with_bend(pipe, existing_pipe)
        if bend is not None:
            self.add_structure(pipe)
            self.add_structure(bend)

        return pipe, bend

    def add_structure(self, structure, *, auto_connect=False):
        self.components.append(structure)

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.pipeline_actor import (
            PipelineActor,
        )

        return PipelineActor(self)
