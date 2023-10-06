import numpy as np
import vtk

from opps.interface.viewer_3d.actors.flange_actor import FlangeActor
from opps.model import Elbow, Flange

from .utils import paint_data


class ElbowActor(vtk.vtkActor):
    def __init__(self, elbow: Elbow):
        self.elbow = elbow
        self.create_geometry()

    def create_geometry(self):
        def lerp(t, a, b):
            return a + t * (b - a)

        arc_points = 10
        arc_source = vtk.vtkArcSource()
        arc_source.SetPoint1(self.elbow.start)
        arc_source.SetPoint2(self.elbow.end)
        arc_source.SetCenter(self.elbow.center)
        arc_source.SetResolution(arc_points - 1)
        arc_source.Update()

        radius = vtk.vtkDoubleArray()
        radius.SetName("TubeRadius")
        radius.SetNumberOfTuples(arc_points)
        for i in range(arc_points):
            r = lerp(i / (arc_points - 1), self.elbow.start_radius, self.elbow.end_radius)
            radius.SetTuple1(i, r)

        polydata = arc_source.GetOutput()
        polydata.GetPointData().AddArray(radius)
        polydata.GetPointData().SetActiveScalars(radius.GetName())

        tube_filter = vtk.vtkTubeFilter()
        tube_filter.SetInputData(polydata)
        tube_filter.SetNumberOfSides(20)
        tube_filter.SetVaryRadiusToVaryRadiusByAbsoluteScalar()
        tube_filter.Update()

        plane_normal = np.cross(
            (self.elbow.start - self.elbow.center), (self.elbow.end - self.elbow.center)
        )
        start_flange = Flange(
            self.elbow.start,
            np.cross(plane_normal, (self.elbow.start - self.elbow.center)),
            self.elbow.start_radius,
        )
        start_flange_data = FlangeActor(start_flange).GetMapper().GetInput()
        end_flange = Flange(
            self.elbow.end,
            np.cross(plane_normal, (self.elbow.end - self.elbow.center)),
            self.elbow.end_radius,
        )
        end_flange_data = FlangeActor(end_flange).GetMapper().GetInput()

        append_polydata = vtk.vtkAppendPolyData()
        append_polydata.AddInputData(tube_filter.GetOutput())
        append_polydata.AddInputData(start_flange_data)
        append_polydata.AddInputData(end_flange_data)
        append_polydata.Update()

        data = append_polydata.GetOutput()
        color = (255, 0, 0)
        paint_data(data, color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.ScalarVisibilityOff()
        self.SetMapper(mapper)
