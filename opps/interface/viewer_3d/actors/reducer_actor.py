import numpy as np
import vtk

from opps.interface.viewer_3d.utils.cell_utils import paint_data
from opps.interface.viewer_3d.utils.cross_section_sources import reducer_data
from opps.interface.viewer_3d.utils.rotations import align_vtk_geometry
from opps.model import Reducer


class ReducerActor(vtk.vtkActor):
    def __init__(self, reducer: Reducer):
        self.reducer = reducer
        self.create_geometry()

    def create_geometry(self):
        vector = self.reducer.end.coords() - self.reducer.start.coords()
        length = np.linalg.norm(vector)
        source = reducer_data(
            length,
            self.reducer.initial_diameter,
            self.reducer.final_diameter,
            self.reducer.initial_offset_y,
            self.reducer.initial_offset_z,
            self.reducer.final_offset_y,
            self.reducer.final_offset_z,
        )

        data = align_vtk_geometry(source, self.reducer.start.coords(), vector)
        paint_data(data, self.reducer.color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)