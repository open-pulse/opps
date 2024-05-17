from .linear_structure import LinearStructure


class Pipe(LinearStructure):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.diameter = kwargs.get("diameter", 0.1)
        self.thickness = kwargs.get("thickness", 0.01)

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "diameter": self.diameter,
            "thickness": self.thickness,
        }

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.pipe_actor import PipeActor

        return PipeActor(self)

    def __hash__(self) -> int:
        return id(self)
