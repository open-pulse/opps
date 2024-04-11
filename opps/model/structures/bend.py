from dataclasses import dataclass

import numpy as np

from .point import Point
from .structure import Structure


def normalize(vector):
    return vector / np.linalg.norm(vector)


class Bend(Structure):
    def __init__(self, start: Point, end: Point, corner: Point, curvature: float, **kwargs):
        super().__init__(**kwargs)

        self.start = start
        self.end = end
        self.corner = corner
        self.curvature = curvature
        self.diameter = kwargs.get("diameter", 0.1)
        self.thickness = kwargs.get("thickness", 0.01)
        self.auto = True
        self.extra_points = {
            0.3 : Point(2,2,0)
        }
    @property
    def center(self):
        if self.is_colapsed():
            return self.corner

        a_vector = normalize(self.start.coords() - self.corner.coords())
        b_vector = normalize(self.end.coords() - self.corner.coords())

        if (a_vector == b_vector).all():
            return self.corner

        if np.dot(a_vector, b_vector) == 1:
            return self.corner

        sin_angle = np.linalg.norm(a_vector - b_vector) / 2
        angle = np.arcsin(sin_angle)
        center_distance = self.curvature / np.sin(angle)

        c_vector = normalize(a_vector + b_vector)
        return Point(*(self.corner.coords() + c_vector * center_distance))

    def normalize_values_vector(self, vec_a: np.ndarray, vec_b: np.ndarray):
        sin_angle = np.linalg.norm(vec_a - vec_b) / 2
        angle = np.arcsin(sin_angle)
        corner_distance = np.cos(angle) * self.curvature / np.sin(angle)
        self.start.set_coords(*(self.corner.coords() + corner_distance * vec_a))
        self.end.set_coords(*(self.corner.coords() + corner_distance * vec_b))

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

        # if the curve is beyond its limits ignore it
        if corner_distance >= np.linalg.norm(start.coords() - self.corner.coords()):
            self.colapse()
            return

        if corner_distance >= np.linalg.norm(end.coords() - self.corner.coords()):
            self.colapse()
            return

        self.start.set_coords(*(self.corner.coords() + corner_distance * a_vector))
        self.end.set_coords(*(self.corner.coords() + corner_distance * b_vector))

    def colapse(self):
        self.start.set_coords(*self.corner.coords())
        self.end.set_coords(*self.corner.coords())

    def is_colapsed(self):
        a = np.allclose(self.start.coords(), self.corner.coords())
        b = np.allclose(self.corner.coords(), self.end.coords())
        return a and b

    def set_diameter(self, start_diameter, final_diameter, *args):
        self.start_diameter = start_diameter
        self.end_diameter = final_diameter

    def get_diameters(self):
        return [self.start_diameter, self.end_diameter]

    def get_points(self):
        points = list(self.extra_points.values())
        return [
            self.start,
            self.end,
            self.corner,
        ] + points

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.bend_actor import BendActor

        return BendActor(self)

    def __hash__(self) -> int:
        return id(self)

    def replace_point(self, old, new):
        if self.start == old:
            self.start = new

        elif self.end == old:
            self.end = new
