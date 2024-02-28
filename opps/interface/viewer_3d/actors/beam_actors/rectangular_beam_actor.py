import vtk
import numpy as np

from opps.model import RectangularBeam
from opps.interface.viewer_3d.utils.cross_section_sources import rectangular_beam_data


class RectangularBeamActor(vtk.vtkActor):
    def __init__(self, beam: RectangularBeam):
        self.beam = beam
        self.create_geometry()

    def create_geometry(self):
        length = np.linalg.norm(self.beam.end.coords() - self.beam.start.coords())
        source = rectangular_beam_data(length, self.beam.width, self.beam.height, self.beam.thickness)

        transform = vtk.vtkTransform()
        transform.Update()

        transform_filter = vtk.vtkTransformFilter()
        transform_filter.SetInputData(source)
        transform_filter.SetTransform(transform)
        transform_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(transform_filter.GetOutput())
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
