import numpy as np
import vtk

from opps.interface.viewer_3d.utils.cell_utils import paint_data
from opps.interface.viewer_3d.utils.cross_section_sources import (
    expansion_joint_data,
)
from opps.interface.viewer_3d.utils.rotations import align_vtk_geometry
from opps.model import ExpansionJoint


class ExpansionJointActor(vtk.vtkActor):
    def __init__(self, expansion_joint: ExpansionJoint):
        self.expansion_joint = expansion_joint
        self.create_geometry()

    def create_geometry(self):
        vector = self.expansion_joint.end.coords() - self.expansion_joint.start.coords()
        length = np.linalg.norm(vector)
        source = expansion_joint_data(
            length, self.expansion_joint.diameter, self.expansion_joint.thickness
        )

        data = align_vtk_geometry(source, self.expansion_joint.start.coords(), vector)
        paint_data(data, self.expansion_joint.color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
