from dataclasses import dataclass, KW_ONLY
from opps.model.structures.point import Point
from .beam import Beam


@dataclass
class IBeam(Beam):
    start: Point
    end: Point
    _:KW_ONLY
    height: float = 0.1    
    width_1: float = 0.1
    width_2: float = 0.1
    thickness_1: float = 0.01
    thickness_2: float = 0.01
    thickness_3: float = 0.01
