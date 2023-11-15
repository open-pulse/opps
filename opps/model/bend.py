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
    start_diameter: float = 0.1
    end_diameter: float = 0.1
    color: tuple = (255, 255, 255)

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
        return Point(*(self.corner.coords() + c_vector * center_distance))
    
    def normalize_values(self, start: Point, end: Point):
        if (start.coords() == self.corner.coords()).all():
            self.colapse()
            return

        if (end.coords() == self.corner.coords()).all():
            self.colapse()
            return

        a_vector = normalize(start.coords() - self.corner.coords())
        b_vector = normalize(end.coords() - self.corner.coords())

        if (a_vector == b_vector).all():
            self.colapse()
            return

        if np.dot(a_vector, b_vector) == 1:
            self.colapse()
            return

        sin_angle = np.linalg.norm(a_vector - b_vector) / 2
        angle = np.arcsin(sin_angle)

        corner_distance = np.cos(angle) * self.curvature / np.sin(angle)
        self.start.set_coords(*(self.corner.coords() + corner_distance * a_vector))
        self.end.set_coords(*(self.corner.coords() + corner_distance * b_vector))
    
    def colapse(self):
        self.start.set_coords(*self.corner.coords())
        self.end.set_coords(*self.corner.coords())

    def set_diameter(self, diameter, point=None):
        if point is None:
            self.start_diameter = diameter
            self.end_diameter = diameter
            return

        if point == self.start:
            self.start_diameter = diameter

        if point == self.end:
            self.end_diameter = diameter

        if point == self.corner:
            self.start_diameter = diameter
            self.end_diameter = diameter
    
    def get_diameters(self):
        return [self.start_diameter, self.end_diameter]

    def get_points(self):
        return [
            self.start,
            self.end,
            self.corner,
        ]

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.bend_actor import BendActor

        return BendActor(self)
