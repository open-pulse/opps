import numpy as np
import vtk

from opps.interface.viewer_3d.utils.cell_utils import paint_data
from opps.interface.viewer_3d.utils.cross_section_sources import pipe_data
from opps.interface.viewer_3d.utils.rotations import align_vtk_geometry
from opps.model import Pipe


class PipeActor(vtk.vtkActor):
    def __init__(self, pipe: Pipe):
        self.pipe = pipe
        self.create_geometry()

    def create_geometry(self):
        vector = self.pipe.end.coords() - self.pipe.start.coords()
        length = np.linalg.norm(vector)
        source = pipe_data(length, self.pipe.diameter, self.pipe.thickness)

        data = align_vtk_geometry(source, self.pipe.start.coords(), vector)
        paint_data(data, self.pipe.color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
