from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opps.model import Pipeline

import vtk

from opps.interface.viewer_3d.actors.pipe_actor import PipeActor
from opps.interface.viewer_3d.utils.cell_utils import (
    fill_cell_identifier,
    paint_data,
)
from opps.model import Pipe


class PipelineActor(vtk.vtkActor):
    def __init__(self, pipeline: "Pipeline"):
        super().__init__()

        self.pipeline = pipeline
        self.create_geometry()
        self.configure_appearance()

    def create_geometry(self):
        append_filter = vtk.vtkAppendPolyData()
        selection_color = (255, 0, 50)

        for i, shape in enumerate(self.pipeline.all_structures()):
            shape_data = shape.as_vtk().GetMapper().GetInput()

            if shape.staged:
                paint_data(shape_data, selection_color)

            if shape.selected:
                paint_data(shape_data, selection_color)

            fill_cell_identifier(shape_data, i)
            append_filter.AddInputData(shape_data)

        if len(list(self.pipeline.all_structures())):
            append_filter.Update()
            appended_data = append_filter.GetOutput()
        else:
            appended_data = vtk.vtkPolyData()

        normals_filter = vtk.vtkPolyDataNormals()
        normals_filter.AddInputData(appended_data)
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
        self.GetProperty().SetSpecularPower(80)
        self.GetProperty().SetSpecularColor(1, 1, 1)
