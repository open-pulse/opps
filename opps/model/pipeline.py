from itertools import chain

import numpy as np

from .structures.bend import Bend
from .structures.elbow import Elbow
from .structures.flange import Flange
from .structures.pipe import Pipe
from .structures.point import Point
from .structures.structure import Structure
from .structures.beam import Beam

from opps.model.editors.main_editor import MainEditor
from opps.model.editors.selection_editor import SelectionEditor


class Pipeline(Structure):
    def __init__(self):
        self.points: list[Point] = list()
        self.structures: list[Structure] = list()

        self.staged_points: list[Point] = list()
        self.staged_structures: list[Structure] = list()

        self.selected_points: list[Point] = list()
        self.selected_structures: list[Structure] = list()

        # tmp
        p = Point(0, 0, 0)
        self.points.append(p)
        self.selected_points.append(p)

        self.main_editor = MainEditor(self)
        self.selection_editor = SelectionEditor(self)

    def all_points(self):
        return chain(self.points, self.staged_points)

    def all_structures(self):
        return chain(self.structures, self.staged_structures)

    # Essential functions
    def commit(self):
        for structure in self.staged_structures:
            structure.staged = False

        self.points.extend(self.staged_points)
        self.structures.extend(self.staged_structures)

        # select the points to continue the creation
        self.select_points(self.main_editor.next_border)
        self.main_editor.next_border.clear()

        self.staged_points.clear()
        self.staged_structures.clear()
        self.main_editor.next_border.clear()

    def dismiss(self):
        for structure in self.staged_structures:
            if isinstance(structure, Bend):
                structure.colapse()
        self.staged_points.clear()
        self.staged_structures.clear()
        self.main_editor.next_border.clear()

    def add_point(self, point: Point):
        self.staged_points.append(point)

    def add_structure(self, structure: Structure):
        structure.staged = True
        self.staged_structures.append(structure)
        self.add_points(structure.get_points())

    def remove_point(self, point: Point):
        for i in self.get_point_indexes(point):
            self.points.pop(i)

    def remove_structure(self, structure: Structure):
        for i in self.get_structure_indexes(structure):
            self.structures.pop(i)
    
    def detatch_point(self, point: Point):
        detatched = []
        first_point = True
        for structure in self.all_structures():
            if point not in structure.get_points():
                continue

            # we still want to keep this point in the pipeline
            # so we only substitute the next ones.
            if first_point:
                first_point = False
                continue

            new_point = point.copy()
            detatched.append(new_point)
            structure.replace_point(point, new_point)

        self.add_points(detatched)
        return detatched

    def attatch_point(self, point: Point):
        for structure in self.structures:
            for p in structure.get_points():
                if np.allclose(p.coords(), point.coords()):
                    structure.replace_point(p, point)

    # Essential functions plural
    def add_points(self, points: list[Point]):
        for point in points:
            self.add_point(point)

    def add_structures(self, structures: list[Structure]):
        for structure in structures:
            self.add_structure(structure)

    def remove_points(self, points: list[Point]):
        for point in points:
            self.remove_point(point)

    def remove_structures(self, structures: list[Structure]):
        for structure in structures:
            self.remove_structure(structure)

    def get_point_indexes(self, point: Point):
        indexes = []
        for i, s in enumerate(self.points):
            if id(s) == id(point):
                indexes.append(i)
        indexes.reverse()
        return indexes

    def get_structure_indexes(self, structure: Structure):
        indexes = []
        for i, s in enumerate(self.structures):
            if id(s) == id(structure):
                indexes.append(i)
        indexes.reverse()
        return indexes

    # Main Editor
    def add_pipe(self, deltas):
        self.main_editor.add_pipe(deltas)

    def add_bend(self, curvature_radius):
        self.main_editor.add_bend(curvature_radius)
    
    def add_bent_pipe(self, deltas, curvature_radius):
        self.main_editor.add_bent_pipe(deltas, curvature_radius)

    def recalculate_curvatures(self):
        self.main_editor.recalculate_curvatures()

    # Selection Editor
    def select_points(self, points, join=False, remove=False):
        self.selection_editor.select_points(points, join, remove)

    def select_structures(self, structures, join=False, remove=False):
        self.selection_editor.select_structures(structures, join, remove)

    def clear_selection(self):
        self.selection_editor.clear_selection()
    
    # Common
    def as_vtk(self):
        from opps.interface.viewer_3d.actors.pipeline_actor import (
            PipelineActor,
        )

        return PipelineActor(self)

    def __hash__(self) -> int:
        return id(self)






    def _update_flanges(self):
        return
        for flange in self.structures:
            if not isinstance(flange, Flange):
                continue

            if not flange.auto:
                continue

            connected_points = self._connected_points(flange.position)
            if not connected_points:
                continue

            oposite_a, *_ = connected_points
            flange.normal = flange.position.coords() - oposite_a.coords()

    def _update_curvatures(self):
        return
        # First colapse all joint that can be colapsed.
        # This prevents cases were a normalization of a
        # joint disturbs the normalization of others.
        for joint in self.structures:
            if not isinstance(joint, Bend | Elbow):
                continue

            if not joint.auto:
                continue

            joint.colapse()

        for joint in self.structures:
            if not isinstance(joint, Bend | Elbow):
                continue

            if not joint.auto:
                continue

            connected_points = (
                self._connected_points(joint.start)
                + self._connected_points(joint.end)
                + self._connected_points(joint.corner)
            )

            if len(connected_points) != 2:
                continue

            oposite_a, oposite_b, *_ = connected_points
            joint.normalize_values(oposite_a, oposite_b)

    def _update_points(self):
        return
        points = list()
        control_points = list()
        for structure in self.structures:
            points.extend(structure.get_points())
            if not isinstance(structure, Pipe | Beam):
                continue
            control_points.extend(structure.get_points())

        point_to_index = {v: i for i, v in enumerate(control_points)}
        indexes_to_remove = []

        for structure in self.structures:
            if not isinstance(structure, Bend | Elbow):
                continue

            if not structure.auto:
                control_points.append(structure.corner)
                control_points.append(structure.end)
                control_points.append(structure.start)
                continue

            control_points.append(structure.corner)
            if structure.start in point_to_index:
                indexes_to_remove.append(point_to_index[structure.start])

            if structure.end in point_to_index:
                indexes_to_remove.append(point_to_index[structure.end])

        for i in sorted(indexes_to_remove, reverse=True):
            control_points.pop(i)

        if not control_points and not points:
            control_points.append(self.origin)
            points.append(self.origin)

        self.control_points = list(control_points)
        self.points = list(points)

    def _connected_points(self, point):
        oposite_points = []
        for pipe in self.structures:
            if not isinstance(pipe, Pipe):
                continue

            if id(pipe.start) == id(point):
                oposite_points.append(pipe.end)

            elif id(pipe.end) == id(point):
                oposite_points.append(pipe.start)

        return oposite_points

