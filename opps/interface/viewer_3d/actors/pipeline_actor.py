import vtk

from opps.interface.viewer_3d.actors.pipe_actor import PipeActor
from opps.model.pipe import Pipe
from opps.model.pipeline import Pipeline
from .utils import paint_data


class PipelineActor(vtk.vtkActor):
    def __init__(self, pipeline: Pipeline):
        super().__init__()

        self.pipeline = pipeline
        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        append_filter = vtk.vtkAppendPolyData()

        for shape in self.pipeline.components:
            actor = shape.as_vtk()
            append_filter.AddInputData(actor.GetMapper().GetInput())
        append_filter.Update()

        normals_filter = vtk.vtkPolyDataNormals()
        normals_filter.AddInputData(append_filter.GetOutput())
        normals_filter.Update()

        data = normals_filter.GetOutput()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)

    def configure_appearance(self):
        self.GetProperty().SetInterpolationToPhong()
        self.GetProperty().SetDiffuse(0.8)
        self.GetProperty().SetSpecular(1.5)
        self.GetProperty().SetSpecularPower(60)
        self.GetProperty().SetSpecularColor(1, 1, 1)
