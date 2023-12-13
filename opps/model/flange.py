from dataclasses import dataclass

import numpy as np


@dataclass
class Flange:
    position: np.ndarray
    normal: np.ndarray
    radius: float = 0.1
    color: tuple = (255, 255, 255)

    def __post_init__(self):
        self.position = np.array(self.position)
        self.normal = np.array(self.normal)
        self.normal = self.normal / np.linalg.norm(self.normal)

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.flange_actor import FlangeActor

        return FlangeActor(self)
