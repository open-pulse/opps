from dataclasses import dataclass, KW_ONLY

from .beam import Beam
from opps.model.structures.point import Point


@dataclass
class CBeam(Beam):
    start: Point
    end: Point
    _:KW_ONLY
    height: float = 0.1    
    width_1: float = 0.1
    width_2: float = 0.1
    thickness_1: float = 0.01
    thickness_2: float = 0.01
    thickness_3: float = 0.01
