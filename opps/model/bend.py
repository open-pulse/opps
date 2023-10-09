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

    def get_corner(self):
        """
        Get the corner from center is the same procedure
        as getting the center from corner.
        """
        def normalize(vector):
          return vector / np.linalg.norm(vector)

        bend_radius = np.linalg.norm(self.end - self.center)
        a_vector = normalize(self.center - self.start)
        b_vector = normalize(self.center - self.end)
        c_vector = normalize(b_vector + a_vector)

        if np.dot(a_vector, b_vector) == 1:
            return None

        sin_angle = np.linalg.norm(a_vector - b_vector) / 2
        angle = np.arcsin(sin_angle)
        center_distance = bend_radius / np.cos(angle)
        corner = self.center - c_vector * center_distance         
        return np.round(corner, 10)

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.bend_actor import BendActor

        return BendActor(self)
