from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opps.model import Valve


import numpy as np
import vtk

from opps.interface.viewer_3d.utils.cell_utils import paint_data
from opps.interface.viewer_3d.utils.cross_section_sources import valve_data
from opps.interface.viewer_3d.utils.rotations import align_vtk_geometry


class ValveActor(vtk.vtkActor):
    def __init__(self, valve: "Valve"):
        self.valve = valve
        self.create_geometry()

    def create_geometry(self):
        vector = self.valve.end.coords() - self.valve.start.coords()
        length = np.linalg.norm(vector)
        source = valve_data(length, self.valve.diameter, self.valve.thickness)

        data = align_vtk_geometry(source, self.valve.start.coords(), vector)
        paint_data(data, self.valve.color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
