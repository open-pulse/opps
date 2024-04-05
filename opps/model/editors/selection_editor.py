from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opps.model import Pipeline

import numpy as np


class SelectionEditor:
    def __init__(self, pipeline: "Pipeline") -> None:
        self.pipeline = pipeline

    def select_last_point(self):
        point, *_ = self.pipeline.points
        self.pipeline.select_points([point])

    def select_last_structure(self):
        structure, *_ = self.pipeline.structures
        self.pipeline.select_structures([structure])

    def select_points(self, points, join=False, remove=False):
        points = set(points)

        if not points:
            return

        current_selection = set(self.pipeline.selected_points)

        if join and remove:
            current_selection ^= points
        elif join:
            current_selection |= points
        elif remove:
            current_selection -= points
        else:
            current_selection = points

        self.pipeline.selected_points = list(current_selection)

    def select_structures(self, structures, join=False, remove=False):
        structures = set(structures)

        if not structures:
            return

        current_selection = set(self.pipeline.selected_structures)

        # clear all the selected flags
        for structure in self.pipeline.structures:
            structure.selected = False

        # handle the selection according to modifiers like ctrl, shift, etc.
        if join and remove:
            current_selection ^= structures
        elif join:
            current_selection |= structures
        elif remove:
            current_selection -= structures
        else:
            current_selection = structures

        # apply the selection flag again for selected structures
        for structure in current_selection:
            structure.selected = True

        self.pipeline.selected_structures = list(current_selection)

    def clear_selection(self):
        for structure in self.pipeline.structures:
            structure.selected = False
        self.pipeline.selected_points.clear()
        self.pipeline.selected_structures.clear()
