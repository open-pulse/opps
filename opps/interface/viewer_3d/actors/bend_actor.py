import vtk

from opps.interface.viewer_3d.utils.cell_utils import paint_data
from opps.model import Bend


class BendActor(vtk.vtkActor):
    def __init__(self, bend: Bend):
        self.bend = bend
        self.create_geometry()

    def create_geometry(self):
        outer_radius = self.bend.diameter / 2
        inner_radius = (self.bend.diameter - self.bend.thickness) / 2

        arc_points = 50
        arc_source = vtk.vtkArcSource()
        arc_source.SetPoint1(self.bend.start.coords())
        arc_source.SetPoint2(self.bend.end.coords())
        arc_source.SetCenter(self.bend.center.coords())
        arc_source.SetResolution(arc_points - 1)
        arc_source.Update()

        external_faces = vtk.vtkTubeFilter()
        external_faces.SetInputData(arc_source.GetOutput())
        external_faces.SetNumberOfSides(20)
        external_faces.SetRadius(outer_radius)
        external_faces.Update()

        append_polydata = vtk.vtkAppendPolyData()

        if self.bend.thickness != 0:
            internal_faces = vtk.vtkTubeFilter()
            internal_faces.SetInputData(arc_source.GetOutput())
            internal_faces.SetNumberOfSides(20)
            internal_faces.SetRadius(inner_radius)
            internal_faces.Update()
            append_polydata.AddInputData(internal_faces.GetOutput())

            ring_start = vtk.vtkDiskSource()
            ring_start.SetCircumferentialResolution(20)
            ring_start.SetOuterRadius(outer_radius)
            ring_start.SetInnerRadius(inner_radius)
            ring_start.SetCenter(self.bend.start.coords())
            ring_start.SetNormal(*(self.bend.start.coords() - self.bend.corner.coords()))
            ring_start.Update()
            append_polydata.AddInputData(ring_start.GetOutput())

            ring_end = vtk.vtkDiskSource()
            ring_end.SetCircumferentialResolution(20)
            ring_end.SetOuterRadius(outer_radius)
            ring_end.SetInnerRadius(inner_radius)
            ring_end.SetCenter(self.bend.end.coords())
            ring_end.SetNormal(*(self.bend.end.coords() - self.bend.corner.coords()))
            ring_end.Update()
            append_polydata.AddInputData(ring_end.GetOutput())

        append_polydata.AddInputData(external_faces.GetOutput())
        append_polydata.Update()

        data = append_polydata.GetOutput()
        color = self.bend.color
        paint_data(data, color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
