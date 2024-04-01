import numpy as np
import vtk

from opps.interface.viewer_3d.utils.cross_section_sources import t_beam_data
from opps.interface.viewer_3d.utils.rotations import align_y_rotations
from opps.model import TBeam


class TBeamActor(vtk.vtkActor):
    def __init__(self, beam: TBeam):
        self.beam = beam
        self.create_geometry()

    def create_geometry(self):
        vector = self.beam.end.coords() - self.beam.start.coords()
        length = np.linalg.norm(vector)
        source = t_beam_data(
            length,
            self.beam.height,
            self.beam.width,
            self.beam.thickness_1,
            self.beam.thickness_2,
        )

        rx, ry, rz = align_y_rotations(vector)
        transform = vtk.vtkTransform()
        transform.RotateZ(-np.degrees(rz))
        transform.RotateY(-np.degrees(ry))
        transform.RotateX(-np.degrees(rx))
        transform.Translate(0, length / 2, 0)
        transform.Update()

        transform_filter = vtk.vtkTransformFilter()
        transform_filter.SetInputData(source)
        transform_filter.SetTransform(transform)
        transform_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(transform_filter.GetOutput())
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
