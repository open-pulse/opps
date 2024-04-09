import numpy as np
import vtk

from opps.interface.viewer_3d.utils.cell_utils import paint_data
from opps.interface.viewer_3d.utils.cross_section_sources import (
    rectangular_beam_data,
)
from opps.interface.viewer_3d.utils.rotations import align_vtk_geometry
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

        data = align_vtk_geometry(source, self.beam.start.coords(), vector)
        paint_data(data, self.beam.color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
