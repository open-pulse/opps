from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opps.model import Valve


import numpy as np
import vtk

from opps.interface.viewer_3d.utils.cell_utils import paint_data
from opps.interface.viewer_3d.utils.cross_section_sources import valve_data
from opps.interface.viewer_3d.utils.rotations import align_y_rotations


class ValveActor(vtk.vtkActor):
    def __init__(self, expansion_joint: "Valve"):
        self.expansion_joint = expansion_joint
        self.create_geometry()

    def create_geometry(self):
        vector = self.expansion_joint.end.coords() - self.expansion_joint.start.coords()
        length = np.linalg.norm(vector)
        source = valve_data(length, self.expansion_joint.diameter, self.expansion_joint.thickness)

        x, y, z = self.expansion_joint.start.coords()
        rx, ry, rz = align_y_rotations(vector)

        transform = vtk.vtkTransform()
        transform.Translate(x, y, z)
        transform.RotateZ(-np.degrees(rz))
        transform.RotateY(-np.degrees(ry))
        transform.RotateX(-np.degrees(rx))
        # transform.Translate(0, length / 2, 0)
        transform.Update()

        transform_filter = vtk.vtkTransformFilter()
        transform_filter.SetInputData(source)
        transform_filter.SetTransform(transform)
        transform_filter.Update()

        data = transform_filter.GetOutput()
        color = self.expansion_joint.color
        paint_data(data, color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
