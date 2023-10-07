from dataclasses import dataclass

import numpy as np


@dataclass
class Elbow:
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

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.elbow_actor import ElbowActor

        return ElbowActor(self)