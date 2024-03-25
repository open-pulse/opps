import numpy as np
from opps.model import Point, Pipe, Bend, Flange

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from opps.model import Pipeline


class MainEditor:
    def __init__(self, pipeline: 'Pipeline') -> None:
        self.pipeline = pipeline
        self.current_point = Point(0,0,0)

    def add_pipe(self, deltas):
        if not self.pipeline.selected_points:
            return

        *_, point = self.pipeline.selected_points
        next_point = Point(*(point.coords() + deltas))
        self.current_point = next_point

        pipe = Pipe(point, next_point)
        self.pipeline.add_structure(pipe)
        return pipe

    def add_bend(self, curvature_radius, allow_dangling=True) -> Bend | None:
        connected_points = self.pipeline._connected_points(self.current_point)
        if len(connected_points) <= 1:
            if allow_dangling:
                return self.add_dangling_bend(curvature_radius)
            else:
                return None

        vec_a = self.current_point - connected_points[0]
        vec_b = self.current_point - connected_points[1]
        vec_a_size = np.linalg.norm(vec_a)
        vec_b_size = np.linalg.norm(vec_b)
        if vec_a_size == 0 or vec_b_size == 0:
            return None

        vec_a /= vec_a_size
        vec_b /= vec_b_size

        # The vectors are parallel
        if np.dot(vec_a, vec_b) == 1:
            return None

        start_point = self.current_point
        corner_point = start_point.copy()
        end_point = start_point.copy()
        self.current_point = end_point

        bend = Bend(start_point, end_point, corner_point)
        bend.normalize_values_vector(vec_a, vec_b)
        self.pipeline.add_structure(bend)
        return Bend




        # bend = Bend(start_point, end_point, corner_point, curvature_radius)
        # self.pipeline.add_structure(bend)
        # return bend

    def add_dangling_bend(self, curvature_radius, direction=None):
        return None

    def add_bent_pipe(self, deltas, curvature_radius):
        bend = self.add_bend(curvature_radius)
        pipe = self.add_pipe(deltas)
        return bend, pipe


        # bend = self.add_bend(curvature_radius)

        # connected_points = self.pipeline._connected_points(bend.start)
        # if connected_points == 1:
        #     pipe = self.add_pipe(deltas)
        #     bend.normalize_values(connected_points[0], pipe.end)
        #     return bend, pipe
        # else:
        #     pass 

        # connected_points = (
        #     self.pipeline._connected_points(bend.start)
        #     + self.pipeline._connected_points(bend.end))
    
        # if len(connected_points) == 2:
        #     bend.colapse()
        #     bend.normalize_values(*connected_points)
        
        # return bend, pipe

    def get_point_directions(self, point: Point):
        directions = []

        for structure in self.pipeline.structures:
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