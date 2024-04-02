import numpy as np
import vtk

from opps.interface.viewer_3d.utils.cell_utils import paint_data
from opps.interface.viewer_3d.utils.cross_section_sources import flange_data
from opps.model import Flange


class FlangeActor(vtk.vtkActor):
    def __init__(self, flange: Flange):
        self.flange = flange
        self.create_geometry()

    def create_geometry(self):
        width = 0.15 * self.flange.diameter
        source = flange_data(width, self.flange.diameter, width)
        unit_normal = self.flange.normal / np.linalg.norm(self.flange.normal)

        proj_xz = self.flange.normal.copy()
        proj_xz[1] = 0
        if np.linalg.norm(proj_xz) == 0:
            ry = 0
        else:
            proj_xz = proj_xz / np.linalg.norm(proj_xz)
            ry = np.arccos(np.dot(proj_xz, [1, 0, 0]))

        rz = -np.arccos(np.dot(unit_normal, [0, 1, 0]))
        if unit_normal[2] > 0:
            ry = -ry

        transform = vtk.vtkTransform()
        transform.Translate(self.flange.position.coords())
        transform.RotateY(np.degrees(ry))
        transform.RotateZ(np.degrees(rz))
        transform.Update()

        transform_filter = vtk.vtkTransformFilter()
        transform_filter.SetInputData(source)
        transform_filter.SetTransform(transform)
        transform_filter.Update()

        data = transform_filter.GetOutput()
        color = self.flange.color
        paint_data(data, color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        self.SetMapper(mapper)
