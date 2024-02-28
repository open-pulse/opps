from dataclasses import dataclass, KW_ONLY
from opps.model.point import Point
from opps.model.beam.beam import Beam


@dataclass
class TBeam(Beam):
    start: Point
    end: Point
    _:KW_ONLY
    height: float = 0.1    
    width: float = 0.1
    thickness_1: float = 0.01
    thickness_2: float = 0.01
