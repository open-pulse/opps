from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opps.model import Pipeline

import numpy as np

from opps.model import Point, CircularBeam, RectangularBeam, CBeam, TBeam, IBeam


class BeamEditor:
    def __init__(self, pipeline: "Pipeline") -> None:
        self.pipeline = pipeline
        self.next_border = list()

    def add_circular_beam(self, deltas: tuple[float, float, float], **kwargs) -> list[CircularBeam]:
        if not np.array(deltas).any():  # all zeros
            return []

        beams = list()

        for point in self.pipeline.selected_points:
            next_point = Point(*(point.coords() + deltas))
            self.next_border.append(next_point)
            beam = CircularBeam(point, next_point, **kwargs)
            self.pipeline.add_structure(beam)
            beams.append(beam)

        self.pipeline.main_editor._colapse_overloaded_bends()

        return beams

    def add_rectangular_beam(self, deltas: tuple[float, float, float], **kwargs) -> list[RectangularBeam]:
        if not np.array(deltas).any():  # all zeros
            return []

        beams = list()

        for point in self.pipeline.selected_points:
            next_point = Point(*(point.coords() + deltas))
            self.next_border.append(next_point)
            beam = RectangularBeam(point, next_point, **kwargs)
            self.pipeline.add_structure(beam)
            beams.append(beam)

        self.pipeline.main_editor._colapse_overloaded_bends()

        return beams

    def add_i_beam(self, deltas: tuple[float, float, float], **kwargs) -> list[IBeam]:
        if not np.array(deltas).any():  # all zeros
            return []

        beams = list()

        for point in self.pipeline.selected_points:
            next_point = Point(*(point.coords() + deltas))
            self.next_border.append(next_point)
            beam = IBeam(point, next_point, **kwargs)
            self.pipeline.add_structure(beam)
            beams.append(beam)

        self.pipeline.main_editor._colapse_overloaded_bends()

        return beams

    def add_c_beam(self, deltas: tuple[float, float, float], **kwargs) -> list[CBeam]:
        if not np.array(deltas).any():  # all zeros
            return []

        beams = list()

        for point in self.pipeline.selected_points:
            next_point = Point(*(point.coords() + deltas))
            self.next_border.append(next_point)
            beam = CBeam(point, next_point, **kwargs)
            self.pipeline.add_structure(beam)
            beams.append(beam)

        self.pipeline.main_editor._colapse_overloaded_bends()

        return beams

    def add_t_beam(self, deltas: tuple[float, float, float], **kwargs) -> list[TBeam]:
        if not np.array(deltas).any():  # all zeros
            return []

        beams = list()

        for point in self.pipeline.selected_points:
            next_point = Point(*(point.coords() + deltas))
            self.next_border.append(next_point)
            beam = TBeam(point, next_point, **kwargs)
            self.pipeline.add_structure(beam)
            beams.append(beam)

        self.pipeline.main_editor._colapse_overloaded_bends()

        return beams
