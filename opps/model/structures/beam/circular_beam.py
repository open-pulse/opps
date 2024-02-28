from dataclasses import dataclass
from opps.model.structures.point import Point
from .beam import Beam


@dataclass
class CircularBeam(Beam):
    start: Point
    end: Point
    diameter: float = 0.1
