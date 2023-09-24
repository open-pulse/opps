from dataclasses import dataclass

import numpy as np


@dataclass
class Pipe:
    start: np.ndarray
    end: np.ndarray
    radius: float = 0.1

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.pipe_actor import PipeActor

        return PipeActor(self)
