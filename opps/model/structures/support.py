from dataclasses import dataclass

import numpy as np

from .point import Point
from .structure import Structure
import vtk


class Support(Structure):
    def __init__(self, start: Point, **kwargs) -> None:
        super().__init__(**kwargs)

        self.start = start

    def get_points(self):
        return [
            self.start,
        ]

    def replace_point(self, old, new):
        if self.start == old:
            self.start = new

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "start": self.start
        }

    def as_vtk(self):
        return vtk.vtkActor(mapper=vtk.vtkPolyDataMapper())
    
    def __hash__(self) -> int:
        return id(self)
