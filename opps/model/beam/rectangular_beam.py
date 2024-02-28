from dataclasses import dataclass
from opps.model.point import Point
from opps.model.beam.beam import Beam


@dataclass
class RectangularBeam(Beam):
    start: Point
    end: Point
    width: float = 0.1
    height: float = 0.1    
