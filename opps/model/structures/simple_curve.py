import numpy as np

from .point import Point
from .structure import Structure


def normalize(vector):
    return vector / np.linalg.norm(vector)


class SimpleCurve(Structure):
    def __init__(self, start: Point, end: Point, corner: Point, curvature: float, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start = start
        self.end = end
        self.corner = corner
        self.curvature = curvature
        self.auto = True

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

    def get_points(self):
        return [
            self.start,
            self.end,
            self.corner,
        ]

    def replace_point(self, old, new):
        if self.start == old:
            self.start = new

        elif self.end == old:
            self.end = new

    def normalize_values_vector(self, vec_a: np.ndarray, vec_b: np.ndarray):
        sin_angle = np.linalg.norm(vec_a - vec_b) / 2
        angle = np.arcsin(sin_angle)
        corner_distance = np.cos(angle) * self.curvature / np.sin(angle)
        self.start.set_coords(*(self.corner.coords() + corner_distance * vec_a))
        self.end.set_coords(*(self.corner.coords() + corner_distance * vec_b))

    def colapse(self):
        self.start.set_coords(*self.corner.coords())
        self.end.set_coords(*self.corner.coords())

    def is_colapsed(self):
        a = np.allclose(self.start.coords(), self.corner.coords())
        b = np.allclose(self.corner.coords(), self.end.coords())
        return a and b

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "start": self.start,
            "end": self.end,
            "corner": self.corner,
            "curvature": self.curvature,
            "auto": self.auto,
        }
