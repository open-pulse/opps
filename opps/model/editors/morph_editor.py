from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opps.model import Pipeline

from itertools import pairwise

import numpy as np

from opps.model import (
    Bend, 
    Elbow,
    CBeam,
    CircularBeam,
    ExpansionJoint,
    Flange,
    IBeam,
    Pipe,
    RectangularBeam,
    ReducerEccentric,
    TBeam,
    Valve,
    Structure,
    Beam,
)


class MorphEditor:
    def __init__(self, pipeline: "Pipeline") -> None:
        self.pipeline = pipeline

    def morph_into(self, structure, structure_class):
        if isinstance(structure, Pipe):
            return self.morph_pipe(structure, structure_class)
    
        elif isinstance(structure, CircularBeam):
            return self.morph_circular_beam(structure, structure_class)

        elif isinstance(structure, RectangularBeam):
            pass 

        elif isinstance(structure, IBeam | CBeam):
            pass

        elif isinstance(structure, TBeam | CBeam):
            pass

        else:
            pass

    def morph_pipe(self, pipe: Pipe, structure_class):
        if issubclass(structure_class, Beam):
            kwargs = {
                "diameter": pipe.diameter,
                "height": pipe.diameter,
                "width": pipe.diameter,
                "width_1": pipe.diameter,
                "width_2": pipe.diameter,
                "thickness": pipe.thickness,
                "thickness_1": pipe.thickness,
                "thickness_2": pipe.thickness,
                "thickness_3": pipe.thickness,
            }
            return structure_class(pipe.start, pipe.end, **kwargs)

    def morph_circular_beam(self, structure_a: CircularBeam, structure_b: Structure):
        if isinstance(structure_b, Pipe):
            pass

        elif isinstance(structure_b, RectangularBeam):
            pass