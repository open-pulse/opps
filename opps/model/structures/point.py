from dataclasses import dataclass

import numpy as np


@dataclass
class Point:
    x: float
    y: float
    z: float

    def coords(self):
        return np.array([self.x, self.y, self.z])

    def set_coords(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def copy(self):
        return Point(self.x, self.y, self.z)

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __hash__(self) -> int:
        return id(self)
