from dataclasses import dataclass
import numpy as np


@dataclass
class Point:
    coords: np.ndarray

    def __iter__(self):
        yield from self.coords