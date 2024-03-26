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
            pipes.append(pipe)
            self.pipeline.add_structure(pipe)
        return pipes

    def add_bend(self, curvature_radius, allow_dangling=False) -> Bend | None:        
        bends = list()

        for point in self.pipeline.selected_points:    
            vec_a, vec_b, dangling = self._get_bend_vectors(point)
            if dangling and not allow_dangling:
                return None

            if abs(np.dot(vec_a, vec_b)) == 1:
                return None

            detatched = self.pipeline.detatch_point(point)
            if len(detatched) == 0:
                start = point.copy()
                end = point.copy()
            elif len(detatched) == 1:
                start = detatched[0]
                end = point.copy()
            else:
                start, end, *_ = detatched

            bend = Bend(start, end, point, curvature_radius)
            bend.normalize_values_vector(vec_a, vec_b, curvature_radius)
            self.pipeline.add_structure(bend)
            bends.append(bend)

        return bends

    def add_bent_pipe(self, deltas, curvature_radius):
        pipe = self.add_pipe(deltas)
        bend = self.add_bend(curvature_radius)
        return bend, pipe

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
        directions = []

        for structure in self.pipeline.all_structures():
            if not point in structure.get_points():
                continue

            if isinstance(structure, Pipe):
                if structure.start == point:
                    vector = structure.end.coords() - point.coords()
                    size = np.linalg.norm(vector)
                    if size:
                        directions.append(vector / size)
                elif structure.end == point:
                    vector = structure.start.coords() - point.coords()
                    size = np.linalg.norm(vector)
                    if size:
                        directions.append(vector / size)
            
            elif isinstance(structure, Bend):
                if (structure.start == point) or (structure.end == point) :
                    vector = structure.corner.coords() - point.coords()
                    size = np.linalg.norm(vector)
                    if size:
                        directions.append(vector / size)

        return directions