from dataclasses import dataclass

import numpy as np


@dataclass
class Flange:
    position: np.ndarray
    normal: np.ndarray
    start_radius: float = 0.1
    end_radius: float = 0.1

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.flange_actor import FlangeActor

        return FlangeActor(self)
