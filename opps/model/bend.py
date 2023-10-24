from dataclasses import dataclass

import numpy as np

def normalize(vector):
    return vector / np.linalg.norm(vector)
@dataclass
class Bend:
    start: np.ndarray
    end: np.ndarray
    corner: np.ndarray
    curvature: float
    diameter: float = 0.1
    color: tuple = (255, 255, 255)

    def __post_init__(self):
        self.start = np.array(self.start)
        self.end = np.array(self.end)
        self.corner = np.array(self.corner)
        self.normalize_values()

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
    
    @property
    def center(self):
        a_vector = normalize(self.start - self.corner)
        b_vector = normalize(self.end - self.corner)

        if (a_vector == b_vector).all():
            return self.corner * np.nan
        
        if np.dot(a_vector, b_vector) == 1:
            return self.corner * np.nan

        sin_angle = np.linalg.norm(a_vector - b_vector) / 2
        angle = np.arcsin(sin_angle)
        center_distance = self.curvature / np.sin(angle)
        
        # print(angle)
        # print(center_distance)
        # print()

        c_vector = normalize(a_vector + b_vector)
        return self.corner + c_vector * center_distance

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.bend_actor import BendActor

        return BendActor(self)
