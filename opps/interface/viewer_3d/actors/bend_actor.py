import vtk

from opps.model.bend import Bend

from .utils import paint_data


class BendActor(vtk.vtkActor):
    def __init__(self, bend: Bend):
        self.bend = bend
        self.create_geometry()

    def create_geometry(self):
        def lerp(t, a, b):
            return a + t * (b - a)

        arc_points = 50
        arc_source = vtk.vtkArcSource()
        arc_source.SetPoint1(self.bend.start.coords())
        arc_source.SetPoint2(self.bend.end.coords())
        arc_source.SetCenter(self.bend.center.coords())
        arc_source.SetResolution(arc_points - 1)
        arc_source.Update()

        radius = vtk.vtkDoubleArray()
        radius.SetName("TubeRadius")
        radius.SetNumberOfTuples(arc_points)
        for i in range(arc_points):
            r = lerp(i / (arc_points - 1), self.bend.diameter/2, self.bend.diameter/2)
            radius.SetTuple1(i, r)

        polydata = arc_source.GetOutput()
        polydata.GetPointData().AddArray(radius)
        polydata.GetPointData().SetActiveScalars(radius.GetName())

        tube_filter = vtk.vtkTubeFilter()
        tube_filter.SetInputData(polydata)
        tube_filter.SetNumberOfSides(20)
        tube_filter.SetVaryRadiusToVaryRadiusByAbsoluteScalar()
        tube_filter.Update()

        data = tube_filter.GetOutput()
        color = self.bend.color
        paint_data(data, color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.SetScalarModeToUseCellData()
        self.SetMapper(mapper)
