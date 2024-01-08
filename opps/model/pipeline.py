from itertools import pairwise

import numpy as np

from opps.model.bend import Bend
from opps.model.flange import Flange
from opps.model.pipe import Pipe
from opps.model.structure import Structure


class Pipeline(Structure):
    def __init__(self):
        self.structures = []

    def add_structure(self, structure, *, auto_connect=False):
        self.structures.append(structure)

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.pipeline_actor import (
            PipelineActor,
        )

        return PipelineActor(self)
