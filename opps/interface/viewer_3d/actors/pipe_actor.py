import vtk

from opps.model.pipe import Pipe

from .utils import paint_data


class PipeActor(vtk.vtkActor):
    def __init__(self, pipe: Pipe):
        self.pipe = pipe
        self.create_geometry()

    def create_geometry(self):
        radius = vtk.vtkDoubleArray()
        radius.SetName("TubeRadius")
        radius.SetNumberOfTuples(2)
        radius.SetTuple1(0, self.pipe.radius)
        radius.SetTuple1(1, self.pipe.radius)

        line_source = vtk.vtkLineSource()
        line_source.SetPoint1(self.pipe.start)
        line_source.SetPoint2(self.pipe.end)
        line_source.Update()

        polydata = line_source.GetOutput()
        polydata.GetPointData().AddArray(radius)
        polydata.GetPointData().SetActiveScalars(radius.GetName())

        tube_filter = vtk.vtkTubeFilter()
        tube_filter.SetInputData(polydata)
        tube_filter.SetNumberOfSides(20)
        tube_filter.SetVaryRadiusToVaryRadiusByAbsoluteScalar()
        tube_filter.Update()

        data = tube_filter.GetOutput()
        color = self.pipe.color
        paint_data(data, color)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        mapper.ScalarVisibilityOff()
        self.SetMapper(mapper)
