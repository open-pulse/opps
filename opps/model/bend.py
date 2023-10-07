from dataclasses import dataclass

import numpy as np


@dataclass
class Bend:
    start: np.ndarray
    end: np.ndarray
    center: np.ndarray
    start_radius: float = 0.1
    end_radius: float = 0.1
    color: tuple = (255, 255, 255)

    def __post_init__(self):
        self.start = np.array(self.start)
        self.end = np.array(self.end)
        self.center = np.array(self.center)

    def get_bend_corner(self):
        """
        Get the corner from center is the same procedure
        as getting the center from corner.
        """
        r = np.linalg.norm(self.start - self.center)
        return get_bend_points(self.start, self.end, self.center, r)

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.bend_actor import BendActor

        return BendActor(self)


def get_bend_points(
    point_a: np.ndarray, point_b: np.ndarray, corner: np.ndarray, bend_radius: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    def normalize(vector):
        return vector / np.linalg.norm(vector)

    a_vector = normalize(corner - point_a)
    b_vector = normalize(corner - point_b)
    c_vector = normalize(b_vector + a_vector)

    if np.dot(a_vector, b_vector) == 1:
        return None

    sin_angle = np.linalg.norm(a_vector - b_vector) / np.linalg.norm(a_vector) / 2
    angle = np.arcsin(sin_angle)
    center_distance = bend_radius / np.sin(angle)
    reduction_distance = center_distance * np.cos(angle)

    return (
        corner - a_vector * reduction_distance,
        corner - b_vector * reduction_distance,
        corner - c_vector * center_distance,
    )
