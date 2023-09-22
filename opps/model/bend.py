from dataclasses import dataclass


@dataclass
class Bend:
    start: tuple[float, float, float]
    end: tuple[float, float, float]
    center: tuple[float, float, float]
    diameter: float = 0.1

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.bend_actor import BendActor

        return BendActor(self)
