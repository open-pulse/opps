import numpy as np
from opps.model import Point, Pipe, Bend, Flange

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from opps.model import Pipeline


class MainEditor:
    def __init__(self, pipeline: 'Pipeline') -> None:
        self.pipeline = pipeline
        self.next_border = list()

    def add_pipe(self, deltas):
        pipes = list()
 
        for point in self.pipeline.selected_points:
            next_point = Point(*(point.coords() + deltas))
            self.next_border.append(next_point)
            pipe = Pipe(point, next_point)
            self.pipeline.add_structure(pipe)
            pipes.append(pipe)

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
        for structure in self.pipeline.all_structures():
            if not isinstance(structure, Bend):
                continue
            if not structure.auto:
                continue
            structure.colapse()

        to_remove = []

        # get vectors and update the curvatures
        # not working yet =)
        for structure in self.pipeline.all_structures():
            if not isinstance(structure, Bend):
                continue

            a_vectors = self._get_point_vectors(structure.start)
            b_vectors = self._get_point_vectors(structure.end)

            if (not a_vectors) or  (not b_vectors):
                to_remove.append(structure)
                continue

            vec_a, vec_b = a_vectors[0], b_vectors[0]
            if abs(np.dot(vec_a, vec_b)) == 1:
                return None

            structure.normalize_values_vector(vec_a, vec_b)

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

        for structure in self.pipeline.all_structures():
            if not point in structure.get_points():
                continue

            size = 0
            if isinstance(structure, Pipe):
                if id(structure.start) == id(point):
                    vector = structure.end.coords() - point.coords()
                    size = np.linalg.norm(vector)
                elif id(structure.end) == id(point):
                    vector = structure.start.coords() - point.coords()
                    size = np.linalg.norm(vector)
            
            elif isinstance(structure, Bend):
                if (id(structure.start) == id(point)) or (id(structure.end) == id(point)) :
                    vector = structure.corner.coords() - point.coords()
                    size = np.linalg.norm(vector)

            if size:
                directions.append(vector / size)

        return directions