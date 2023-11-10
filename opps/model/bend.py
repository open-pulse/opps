from dataclasses import dataclass
from opps.model.point import Point

import numpy as np

def normalize(vector):
    return vector / np.linalg.norm(vector)
@dataclass
class Bend:
    start: Point
    end: Point
    corner: Point
    curvature: float
    diameter: float = 0.1
    color: tuple = (255, 255, 255)

    # def __post_init__(self):
    #     self.start = np.array(self.start)
    #     self.end = np.array(self.end)
    #     self.corner = np.array(self.corner)
    #     self.normalize_values()

    def normalize_values(self):
        a_vector = normalize(self.start - self.corner)
        b_vector = normalize(self.end - self.corner)

        if (a_vector == b_vector).all():
            return

        if np.dot(a_vector, b_vector) == 1:
            return

        sin_angle = np.linalg.norm(a_vector - b_vector) / 2
        angle = np.arcsin(sin_angle)

        corner_distance = np.cos(angle) * self.curvature / np.sin(angle)
        self.start = self.corner + corner_distance * a_vector
        self.end = self.corner + corner_distance * b_vector
    
    def normalize_values_2(self, start, end):
        a_vector = normalize(start.coords() - self.corner.coords())
        b_vector = normalize(end.coords() - self.corner.coords())

        if (a_vector == b_vector).all():
            self.start.set_coords(*self.corner.coords())
            self.end.set_coords(*self.corner.coords())
            return

        if np.dot(a_vector, b_vector) == 1:
            self.start.set_coords(*self.corner.coords())
            self.end.set_coords(*self.corner.coords())
            return

        sin_angle = np.linalg.norm(a_vector - b_vector) / 2
        angle = np.arcsin(sin_angle)

        corner_distance = np.cos(angle) * self.curvature / np.sin(angle)
        self.start.set_coords(*(self.corner.coords() + corner_distance * a_vector))
        self.end.set_coords(*(self.corner.coords() + corner_distance * b_vector))
    
    @property
    def center(self):
        a_vector = normalize(self.start.coords() - self.corner.coords())
        b_vector = normalize(self.end.coords() - self.corner.coords())

        if (a_vector == b_vector).all():
            return self.corner * np.nan
        
        if np.dot(a_vector, b_vector) == 1:
            return self.corner * np.nan

        sin_angle = np.linalg.norm(a_vector - b_vector) / 2
        angle = np.arcsin(sin_angle)
        center_distance = self.curvature / np.sin(angle)

        c_vector = normalize(a_vector + b_vector)
        return self.corner.coords() + c_vector * center_distance

    def get_points(self):
        return [
            self.start,
            self.end,
            self.corner,
        ]
    
    def move_corner(self, new_corner):
        self.corner = new_corner
        self.normalize_values()

    def map_coords(self, coords_map):
        self.start = np.array(coords_map.get(tuple(self.start), self.start))
        self.end = np.array(coords_map.get(tuple(self.end), self.end))
        self.corner = np.array(coords_map.get(tuple(self.corner), self.corner))

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.bend_actor import BendActor

        return BendActor(self)
