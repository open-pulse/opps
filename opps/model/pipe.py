from dataclasses import dataclass

import numpy as np


@dataclass
class Pipe:
    start: np.ndarray
    end: np.ndarray
    radius: float = 0.1
    color: tuple = (255, 255, 255)

    def __post_init__(self):
        self.start = np.array(self.start)
        self.end = np.array(self.end)

    def map_coords(self, coords_map):
        self.start = np.array(coords_map.get(tuple(self.start), self.start))
        self.end = np.array(coords_map.get(tuple(self.end), self.end))

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.pipe_actor import PipeActor

        return PipeActor(self)
