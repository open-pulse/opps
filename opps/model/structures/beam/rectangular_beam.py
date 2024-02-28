from dataclasses import dataclass
from opps.model.structures.point import Point
from .beam import Beam


@dataclass
class RectangularBeam(Beam):
    start: Point
    end: Point
    width: float = 0.1
    height: float = 0.1    
