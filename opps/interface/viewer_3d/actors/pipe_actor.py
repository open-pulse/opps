import numpy as np
import vtk

from opps.interface.viewer_3d.utils.cell_utils import paint_data
from opps.interface.viewer_3d.utils.cross_section_sources import pipe_data
from opps.interface.viewer_3d.utils.rotations import align_y_rotations
from opps.model import Pipe


class PipeActor(vtk.vtkActor):
    def __init__(self, pipe: Pipe):
        self.pipe = pipe
        self.create_geometry()

    def create_geometry(self):
        vector = self.pipe.end.coords() - self.pipe.start.coords()
        length = np.linalg.norm(vector)
        source = pipe_data(length, self.pipe.diameter, self.pipe.thickness)

        x, y, z = self.pipe.start.coords()
        rx, ry, rz = align_y_rotations(vector)

        transform = vtk.vtkTransform()
        transform.Translate(x, y, z)
        transform.RotateZ(-np.degrees(rz))
        transform.RotateY(-np.degrees(ry))
        transform.RotateX(-np.degrees(rx))
        transform.Update()

        transform_filter = vtk.vtkTransformFilter()
        transform_filter.SetInputData(source)
        transform_filter.SetTransform(transform)
        transform_filter.Update()

        data = transform_filter.GetOutput()
        color = self.pipe.color
        paint_data(data, color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
