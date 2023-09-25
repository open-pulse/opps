import vtk

from opps.model.bend import Bend


class BendActor(vtk.vtkActor):
    def __init__(self, bend: Bend):
        self.bend = bend
        self.create_geometry()

    def create_geometry(self):
        def lerp(t, a, b):
            return a + t * (b - a)

        arc_points = 50
        arc_source = vtk.vtkArcSource()
        arc_source.SetPoint1(self.bend.start)
        arc_source.SetPoint2(self.bend.end)
        arc_source.SetCenter(self.bend.center)
        arc_source.SetResolution(arc_points - 1)
        arc_source.Update()

        radius = vtk.vtkDoubleArray()
        radius.SetName("TubeRadius")
        radius.SetNumberOfTuples(arc_points)
        for i in range(arc_points):
            r = lerp(i/(arc_points - 1), self.bend.start_radius, self.bend.end_radius)
            radius.SetTuple1(i, r) 

        polydata = arc_source.GetOutput()
        polydata.GetPointData().AddArray(radius)
        polydata.GetPointData().SetActiveScalars(radius.GetName())

        tube_filter = vtk.vtkTubeFilter()
        tube_filter.SetInputData(polydata)
        tube_filter.SetNumberOfSides(20)
        tube_filter.SetVaryRadiusToVaryRadiusByAbsoluteScalar()
        tube_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(tube_filter.GetOutput())
        mapper.ScalarVisibilityOff()
        self.SetMapper(mapper)
