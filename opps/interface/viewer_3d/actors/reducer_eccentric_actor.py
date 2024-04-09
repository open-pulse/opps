import numpy as np
import vtk

from opps.interface.viewer_3d.utils.cell_utils import paint_data
from opps.interface.viewer_3d.utils.cross_section_sources import (
    eccentric_reducer_data,
)
from opps.interface.viewer_3d.utils.rotations import align_vtk_geometry
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

        data = align_vtk_geometry(source, self.reducer.start.coords(), vector)
        paint_data(data, self.reducer.color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
