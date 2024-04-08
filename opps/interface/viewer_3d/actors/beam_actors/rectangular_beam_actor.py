import numpy as np
import vtk

from opps.interface.viewer_3d.utils.cell_utils import paint_data
from opps.interface.viewer_3d.utils.cross_section_sources import (
    rectangular_beam_data,
)
from opps.interface.viewer_3d.utils.rotations import align_y_rotations
from opps.model import RectangularBeam


class RectangularBeamActor(vtk.vtkActor):
    def __init__(self, beam: RectangularBeam):
        self.beam = beam
        self.create_geometry()

    def create_geometry(self):
        vector = self.beam.end.coords() - self.beam.start.coords()
        length = np.linalg.norm(vector)
        source = rectangular_beam_data(
            length, self.beam.width, self.beam.height, self.beam.thickness
        )

        x, y, z = self.beam.start.coords()
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
        color = self.beam.color
        paint_data(data, color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
