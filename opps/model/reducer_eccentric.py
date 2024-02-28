from dataclasses import dataclass
from opps.model.structure import Structure
from opps.model.point import Point


@dataclass
class ReducerEccentric(Structure):
    start: Point
    end: Point
    offset_y: float = 0
    offset_z: float = 0
    start_diameter: float = 0.1
    end_diameter: float = 0.1
