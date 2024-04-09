import numpy as np
import vtk

from opps.interface.viewer_3d.utils.cell_utils import paint_data
from opps.interface.viewer_3d.utils.cross_section_sources import flange_data
from opps.interface.viewer_3d.utils.rotations import align_vtk_geometry
from opps.model import Flange


class FlangeActor(vtk.vtkActor):
    def __init__(self, flange: Flange):
        self.flange = flange
        self.create_geometry()

    def create_geometry(self):
        vector = self.flange.end.coords() - self.flange.start.coords()
        length = np.linalg.norm(vector)
        source = flange_data(length, self.flange.diameter, self.flange.thickness)

        data = align_vtk_geometry(source, self.flange.start.coords(), vector)
        paint_data(data, self.flange.color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
