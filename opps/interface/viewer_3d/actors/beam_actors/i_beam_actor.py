import numpy as np
import vtk

from opps.interface.viewer_3d.utils.cell_utils import paint_data
from opps.interface.viewer_3d.utils.cross_section_sources import i_beam_data
from opps.interface.viewer_3d.utils.rotations import align_vtk_geometry
from opps.model import IBeam


class IBeamActor(vtk.vtkActor):
    def __init__(self, beam: IBeam):
        self.beam = beam
        self.create_geometry()

    def create_geometry(self):
        vector = self.beam.end.coords() - self.beam.start.coords()
        length = np.linalg.norm(vector)
        source = i_beam_data(
            length,
            self.beam.height,
            self.beam.width_1,
            self.beam.width_2,
            self.beam.thickness_1,
            self.beam.thickness_2,
            self.beam.thickness_3,
        )

        data = align_vtk_geometry(source, self.beam.start.coords(), vector)
        paint_data(data, self.beam.color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
