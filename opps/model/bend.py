from dataclasses import dataclass

import numpy as np


@dataclass
class Bend:
    start: np.ndarray
    end: np.ndarray
    center: np.ndarray
    radius: float = 0.1

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.bend_actor import BendActor

        return BendActor(self)
