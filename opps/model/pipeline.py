from opps.model.bend import Bend
from opps.model.pipe import Pipe


class Pipeline:
    def __init__(self):
        self.components = []

    def add_pipe(self, *args, **kwargs):
        self.components.append(Pipe(*args, **kwargs))

    def add_bend(self, *args, **kwargs):
        self.components.append(Bend(*args, **kwargs))

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.pipeline_actor import (
            PipelineActor,
        )

        return PipelineActor(self)
