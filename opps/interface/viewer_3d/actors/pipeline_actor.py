import vtk

from opps.interface.viewer_3d.actors.pipe_actor import PipeActor
from opps.model.pipe import Pipe
from opps.model.pipeline import Pipeline


class PipelineActor(vtk.vtkActor):
    def __init__(self, pipeline: Pipeline):
        super().__init__()

        self.pipeline = pipeline
        self.create_geometry()

    def create_geometry(self):
        append_filter = vtk.vtkAppendPolyData()

        for shape in self.pipeline.components:
            actor = shape.as_vtk()
            append_filter.AddInputData(actor.GetMapper().GetInput())
        append_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(append_filter.GetOutput())
        self.SetMapper(mapper)
