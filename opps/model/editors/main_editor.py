from typing import TYPE_CHECKING

import numpy as np

from opps.model import Bend, Flange, Pipe, Point

if TYPE_CHECKING:
    from opps.model import Pipeline


class MainEditor:
    def __init__(self, pipeline: "Pipeline") -> None:
        self.pipeline = pipeline
        self.next_border = list()

    def add_pipe(self, deltas):
        if not np.array(deltas).any():  # all zeros
            return []

        pipes = list()

        for point in self.pipeline.selected_points:
            next_point = Point(*(point.coords() + deltas))
            self.next_border.append(next_point)
            pipe = Pipe(point, next_point)
            self.pipeline.add_structure(pipe)
            pipes.append(pipe)

        self._colapse_overloaded_bend()

        return pipes

    def add_bend(self, curvature_radius, allow_dangling=False) -> Bend | None:
        bends = list()
        for point in self.pipeline.selected_points:
            vec_a, vec_b, dangling = self._get_bend_vectors(point)
            if dangling and not allow_dangling:
                return None

            angle_between_pipes = np.arccos(np.dot(vec_a, vec_b))
            if angle_between_pipes == 0:
                return None

            if angle_between_pipes == np.pi:  # 180º
                return None

            start = point
            corner = point.copy()
            end = point.copy()

            # detatch the connection between pipes (if it exists)
            # to add the bend in between them
            detatched = self.pipeline.detatch_point(point)
            if len(detatched) >= 1:
                end = detatched[0]

            bend = Bend(start, end, corner, curvature_radius)
            bend.normalize_values_vector(vec_a, vec_b)
            self.pipeline.add_structure(bend)
            bends.append(bend)

        return bends

    def add_flange(self):
        flanges = list()

        for point in self.pipeline.selected_points:
            vectors = self._get_point_vectors(point)
            vectors.append(np.array([1, 0, 0]))  # the default flange points to the right

            normal, *_ = vectors
            flange = Flange(point, normal=normal)
            self.pipeline.add_structure(flange)
            flanges.append(flange)

        return flanges

    def add_bent_pipe(self, deltas, curvature_radius):
        pipe = self.add_pipe(deltas)
        bend = self.add_bend(curvature_radius)
        return bend, pipe

    def recalculate_curvatures(self):
        # collapse all curvatures
        for bend in self.pipeline.structures_of_type(Bend):
            if bend.auto:
                bend.colapse()

        for flange in self.pipeline.structures_of_type(Flange):
            if not flange.auto:
                continue

            vectors = self._get_point_vectors(flange.position)
            if not vectors:
                continue

            flange.normal = vectors[0]

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

    def _colapse_overloaded_bend(self):
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

        for pipe in self.pipeline.structures_of_type(Pipe):
            if not point in pipe.get_points():
                continue

            if id(pipe.start) == id(point):
                vector = pipe.end.coords() - point.coords()
                size = np.linalg.norm(vector)
            elif id(pipe.end) == id(point):
                vector = pipe.start.coords() - point.coords()
                size = np.linalg.norm(vector)
            else:
                continue

            directions.append(vector / size)

        # for structure in self.pipeline.structures_of_type(Bend):
        #     if (id(structure.start) == id(point)) or (id(structure.end) == id(point)) :
        #         vector = structure.corner.coords() - point.coords()
        #         size = np.linalg.norm(vector)
        #     directions.append(vector / size)

        return directions
