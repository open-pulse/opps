import numpy as np
import vtk

from opps.interface.viewer_3d.utils.cell_utils import paint_data
from opps.model import Flange


class FlangeActor(vtk.vtkActor):
    def __init__(self, flange: Flange):
        self.flange = flange
        self.create_geometry()

    def create_geometry(self):
        width = 0.15 * self.flange.diameter
        y_vector = np.array((0, 1, 0))

        disk_source = vtk.vtkDiskSource()
        disk_source.SetCenter((0, 0, 0) - y_vector * width / 2)
        disk_source.SetNormal(y_vector)
        disk_source.SetInnerRadius(self.flange.diameter / 2)
        disk_source.SetOuterRadius(self.flange.diameter / 2 + width)
        disk_source.SetCircumferentialResolution(50)
        disk_source.Update()

        extrusion_filter = vtk.vtkLinearExtrusionFilter()
        extrusion_filter.SetInputData(disk_source.GetOutput())
        extrusion_filter.SetExtrusionTypeToNormalExtrusion()
        extrusion_filter.SetVector(y_vector)
        extrusion_filter.SetScaleFactor(width)
        extrusion_filter.Update()

        append_polydata = vtk.vtkAppendPolyData()
        append_polydata.AddInputData(extrusion_filter.GetOutput())

        number_of_bolts = 8
        for i in range(number_of_bolts):
            angle = i * 2 * np.pi / number_of_bolts
            nut = vtk.vtkCylinderSource()
            nut.SetHeight(width * 3 / 2)
            nut.SetRadius(width / 3)
            nut.SetCenter(
                (self.flange.diameter / 2 + width / 2) * np.sin(angle),
                0,
                (self.flange.diameter / 2 + width / 2) * np.cos(angle),
            )
            nut.Update()
            append_polydata.AddInputData(nut.GetOutput())
        append_polydata.Update()

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
        transform_filter.SetInputData(append_polydata.GetOutput())
        transform_filter.SetTransform(transform)
        transform_filter.Update()

        data = transform_filter.GetOutput()
        color = self.flange.color
        paint_data(data, color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        self.SetMapper(mapper)
