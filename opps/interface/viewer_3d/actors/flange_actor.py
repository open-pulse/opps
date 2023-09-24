import vtk

from opps.model.flange import Flange
import numpy as np


class FlangeActor(vtk.vtkActor):
    def __init__(self, flange: Flange):
        self.flange = flange
        self.create_geometry()
        
    def create_geometry(self):
        bigger_radius = max(self.flange.start_radius, self.flange.end_radius)
        width = 0.3 * bigger_radius

        disk_source = vtk.vtkDiskSource()
        disk_source.SetCenter(self.flange.position - self.flange.normal * width / 2)
        disk_source.SetNormal(self.flange.normal)
        disk_source.SetInnerRadius(self.flange.start_radius)
        disk_source.SetOuterRadius(bigger_radius + width)
        disk_source.SetCircumferentialResolution(20)
        disk_source.Update()

        extrusion_filter = vtk.vtkLinearExtrusionFilter()
        extrusion_filter.SetInputData(disk_source.GetOutput())
        extrusion_filter.SetExtrusionTypeToNormalExtrusion()
        extrusion_filter.SetVector(self.flange.normal)
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
                (bigger_radius + width / 2) * np.sin(angle), 
                0, 
                (bigger_radius + width / 2) * np.cos(angle),
            )
            nut.Update()

            append_polydata.AddInputData(nut.GetOutput())

        append_polydata.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(append_polydata.GetOutput())
        self.SetMapper(mapper)
