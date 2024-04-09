from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opps.model import Pipeline

from itertools import pairwise

import numpy as np

from opps.model import (
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
)


class ConnectionEditor:
    def __init__(self, pipeline: "Pipeline") -> None:
        self.pipeline = pipeline

    def connect_pipes(self, **kwargs):
        self._generic_structure_connection(Pipe, **kwargs)

    def connect_expansion_joints(self, **kwargs):
        self._generic_structure_connection(ExpansionJoint, **kwargs)

    def connect_flanges(self, **kwargs):
        self._generic_structure_connection(Flange, **kwargs)

    def connect_valves(self, **kwargs):
        self._generic_structure_connection(Valve, **kwargs)

    def connect_reducer_eccentrics(self, **kwargs):
        self._generic_structure_connection(ReducerEccentric, **kwargs)

    def connect_circular_beams(self, **kwargs):
        self._generic_structure_connection(CircularBeam, **kwargs)

    def connect_rectangular_beams(self, **kwargs):
        self._generic_structure_connection(RectangularBeam, **kwargs)

    def connect_i_beams(self, **kwargs):
        self._generic_structure_connection(IBeam, **kwargs)

    def connect_c_beams(self, **kwargs):
        self._generic_structure_connection(CBeam, **kwargs)

    def connect_t_beams(self, **kwargs):
        self._generic_structure_connection(TBeam, **kwargs)

    def _generic_structure_connection(self, structure_type, **kwargs):
        structures = []
        for point_a, point_b in pairwise(self.pipeline.selected_points):
            structure = structure_type(point_a, point_b, **kwargs)
            self.pipeline.add_structure(structure)
            structures.append(structure)
        return structures
