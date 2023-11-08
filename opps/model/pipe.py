from dataclasses import dataclass

import numpy as np

from opps.model.point import Point

@dataclass
class Pipe:
    start: Point
    end: Point
    diameter: float = 0.1
    color: tuple = (255, 255, 255)

    def map_coords(self, coords_map):
        self.start = np.array(coords_map.get(tuple(self.start), self.start))
        self.end = np.array(coords_map.get(tuple(self.end), self.end))

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.pipe_actor import PipeActor

        return PipeActor(self)
