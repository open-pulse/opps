from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opps.model import Pipeline

import numpy as np

from opps.model import (
    Bend,
    CBeam,
    CircularBeam,
    ExpansionJoint,
    Flange,
    IBeam,
    Pipe,
    Point,
    RectangularBeam,
    ReducerEccentric,
    Structure,
    TBeam,
    Valve,
)


class MainEditor:
    def __init__(self, pipeline: "Pipeline") -> None:
        self.pipeline = pipeline
        self.next_border = list()

    def add_pipe(self, deltas, **kwargs) -> list[Pipe]:
        return self._add_generic_line_structure(Pipe, deltas, **kwargs)

    def add_bend(self, curvature_radius: float, allow_dangling=False, **kwargs) -> list[Bend]:
        bends = list()

        if curvature_radius <= 0:
            return bends

        if not self.pipeline.selected_points:
            self.pipeline.select_last_point()

        for point in self.pipeline.selected_points:
            vec_a, vec_b, dangling = self._get_bend_vectors(point)
            if dangling and not allow_dangling:
                continue

            angle_between_pipes = np.arccos(np.dot(vec_a, vec_b))
            if angle_between_pipes == 0:
                continue

            if angle_between_pipes == np.pi:  # 180º
                continue

            bend_exists = False
            for bend in self.pipeline.structures_of_type(Bend):
                if point in bend.get_points():
                    bend_exists = True
                    break

            # Do not put a bend over another
            if bend_exists:
                continue

            start = point
            corner = point.copy()
            end = point.copy()

            # detatch the connection between pipes (if it exists)
            # to add the bend in between them
            detatched = self.pipeline.detatch_point(point)
            if len(detatched) >= 1:
                end = detatched[0]

            bend = Bend(start, end, corner, curvature_radius, **kwargs)
            bend.normalize_values_vector(vec_a, vec_b)
            self.pipeline.add_structure(bend)
            bends.append(bend)

        return bends

    def add_flange(self, deltas, **kwargs) -> list[Flange]:
        return self._add_generic_line_structure(Flange, deltas, **kwargs)

        flanges = list()

        if not self.pipeline.selected_points:
            self.pipeline.select_last_point()

        for point in self.pipeline.selected_points:
            vectors = self._get_point_vectors(point)
            vectors.append(np.array([1, 0, 0]))  # the default flange points to the right

            normal, *_ = vectors
            flange = Flange(point, normal=normal, **kwargs)
            self.pipeline.add_structure(flange)
            flanges.append(flange)

        return flanges

    def add_bent_pipe(self, deltas, curvature_radius: float, **kwargs) -> list[Pipe | Bend]:
        pipes = self.add_pipe(deltas, **kwargs)
        bends = self.add_bend(curvature_radius, **kwargs)
        return bends + pipes

    def add_expansion_joint(self, deltas, **kwargs) -> list[ExpansionJoint]:
        return self._add_generic_line_structure(ExpansionJoint, deltas, **kwargs)

    def add_valve(self, deltas, **kwargs) -> list[Valve]:
        return self._add_generic_line_structure(Valve, deltas, **kwargs)

    def add_reducer_eccentric(self, deltas, **kwargs) -> list[ReducerEccentric]:
        return self._add_generic_line_structure(ReducerEccentric, deltas, **kwargs)

    def add_circular_beam(self, deltas, **kwargs) -> list[CircularBeam]:
        return self._add_generic_line_structure(CircularBeam, deltas, **kwargs)

    def add_rectangular_beam(self, deltas, **kwargs) -> list[RectangularBeam]:
        return self._add_generic_line_structure(RectangularBeam, deltas, **kwargs)

    def add_i_beam(self, deltas, **kwargs) -> list[IBeam]:
        return self._add_generic_line_structure(IBeam, deltas, **kwargs)

    def add_c_beam(self, deltas, **kwargs) -> list[CBeam]:
        return self._add_generic_line_structure(CBeam, deltas, **kwargs)

    def add_t_beam(self, deltas, **kwargs) -> list[TBeam]:
        return self._add_generic_line_structure(TBeam, deltas, **kwargs)

    def recalculate_curvatures(self):
        # collapse all curvatures that are in between pipes
        for bend in self.pipeline.structures_of_type(Bend):
            a_vectors = self._get_point_vectors(bend.start)
            b_vectors = self._get_point_vectors(bend.end)

            if (not a_vectors) or (not b_vectors):
                continue

            if not bend.auto:
                continue

            bend.colapse()

        for bend in self.pipeline.structures_of_type(Bend):
            if not bend.auto:
                continue

            a_vectors = self._get_point_vectors(bend.start)
            b_vectors = self._get_point_vectors(bend.end)

            if (not a_vectors) or (not b_vectors):
                continue

            vec_a, vec_b = a_vectors[0], b_vectors[0]
            angle_between_pipes = np.arccos(np.dot(vec_a, vec_b))

            if angle_between_pipes == 0:
                continue

            if angle_between_pipes == np.pi:  # 180º
                continue

            bend.normalize_values_vector(vec_a, vec_b)

        # Removing collapsed bends feels weird for users.
        # If you still want this for some reason discomment
        # the following line:
        # self.remove_collapsed_bends()

    def remove_collapsed_bends(self):
        to_remove = []
        for bend in self.pipeline.structures_of_type(Bend):
            if bend.is_colapsed():
                to_remove.append(bend)
        self.pipeline.remove_structures(to_remove)
        return to_remove

    def _add_generic_line_structure(
        self, structure_type: type[Structure], deltas: tuple[float, float, float], **kwargs
    ):
        if not np.array(deltas).any():  # all zeros
            return []

        if not self.pipeline.selected_points:
            self.pipeline.select_last_point()

        structures = list()
        for point in self.pipeline.selected_points:
            next_point = Point(*(point.coords() + deltas))
            self.next_border.append(next_point)
            structure = structure_type(point, next_point, **kwargs)
            self.pipeline.add_structure(structure)
            structures.append(structure)
        self.pipeline.main_editor._colapse_overloaded_bends()
        return structures

    def _colapse_overloaded_bends(self):
        """
        If a bend, that should connect only two pipes, has a third connection
        or more, this function will colapse it.
        Then, during the commit, these colapsed bends can be safelly removed.
        """

        for point in self.pipeline.selected_points:
            for bend in self.pipeline.structures_of_type(Bend):
                if id(bend.corner) == id(point):
                    bend.colapse()

    def _get_bend_vectors(self, point: Point):
        directions = self._get_point_vectors(point)

        if len(directions) == 0:
            vec_a = np.array([-1, 0, 0])
            vec_b = np.array([0, 1, 0])
            dangling = True

        elif len(directions) == 1:
            vec_a = directions[0]
            if not np.allclose(vec_a, [0, 0, 1]):
                vec_b = np.cross(vec_a, [0, 0, 1])
            else:
                vec_b = np.cross(vec_a, [1, 0, 0])
            dangling = True

        else:
            vec_a, vec_b, *_ = directions
            dangling = False

        return vec_a, vec_b, dangling

    def _get_point_vectors(self, point: Point):
        directions = list()

        pipe_like_structure = Pipe | Flange | ReducerEccentric | ExpansionJoint | Valve
        for structure in self.pipeline.structures_of_type(pipe_like_structure):
            if not point in structure.get_points():
                continue

            if id(structure.start) == id(point):
                vector = structure.end.coords() - point.coords()
                size = np.linalg.norm(vector)
            elif id(structure.end) == id(point):
                vector = structure.start.coords() - point.coords()
                size = np.linalg.norm(vector)
            else:
                continue

            if size:
                directions.append(vector / size)

        return directions
