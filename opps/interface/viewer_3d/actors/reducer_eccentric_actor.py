import numpy as np
import vtk

from opps.interface.viewer_3d.utils.cross_section_sources import (
    eccentric_reducer_data,
)
from opps.interface.viewer_3d.utils.cell_utils import paint_data
from opps.interface.viewer_3d.utils.rotations import align_y_rotations
from opps.model import ReducerEccentric


class ReducerEccentricActor(vtk.vtkActor):
    def __init__(self, reducer: ReducerEccentric):
        self.reducer = reducer
        self.create_geometry()

    def create_geometry(self):
        vector = self.reducer.end.coords() - self.reducer.start.coords()
        length = np.linalg.norm(vector)
        source = eccentric_reducer_data(
            length,
            self.reducer.start_diameter,
            self.reducer.end_diameter,
            self.reducer.offset_y,
            self.reducer.offset_z,
        )

        x, y, z = self.reducer.start.coords()
        rx, ry, rz = align_y_rotations(vector)

        transform = vtk.vtkTransform()
        transform.Translate(x, y, z)
        transform.RotateZ(-np.degrees(rz))
        transform.RotateY(-np.degrees(ry))
        transform.RotateX(-np.degrees(rx))
        transform.Translate(0, length / 2, 0)
        transform.Update()

        transform_filter = vtk.vtkTransformFilter()
        transform_filter.SetInputData(source)
        transform_filter.SetTransform(transform)
        transform_filter.Update()

        data = transform_filter.GetOutput()
        color = self.reducer.color
        paint_data(data, color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
