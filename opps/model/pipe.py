from dataclasses import dataclass

import numpy as np

from opps.model.point import Point

@dataclass
class Pipe:
    start: Point
    end: Point
    diameter: float = 0.1
    color: tuple = (255, 255, 255)

    def get_points(self):
        return [
            self.start,
            self.end,
        ]

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.pipe_actor import PipeActor

        return PipeActor(self)
