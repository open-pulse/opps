from dataclasses import dataclass
from opps.model.point import Point
from opps.model.beam.beam import Beam


@dataclass
class CircularBeam(Beam):
    start: Point
    end: Point
    diameter: float = 0.1
