from .beam import Beam


class RectangularBeam(Beam):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.width = kwargs.get("width", 0.1)
        self.height = kwargs.get("height", 0.1)
        self.thickness = kwargs.get("thickness", 0.01)

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "height": self.height,
            "width": self.width,
            "thickness": self.thickness,
        }

    def as_vtk(self):
        from opps.interface.viewer_3d.actors import RectangularBeamActor

        return RectangularBeamActor(self)

    def __hash__(self) -> int:
        return id(self)
