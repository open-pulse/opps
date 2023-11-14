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
        radius.SetTuple1(0, self.pipe.start_diameter / 2)

        if self.pipe.end_diameter == 0:
            radius.SetTuple1(1, self.pipe.start_diameter / 2)
        else:
            radius.SetTuple1(1, self.pipe.end_diameter / 2)

        line_source = vtk.vtkLineSource()
        line_source.SetPoint1(self.pipe.start.coords())
        line_source.SetPoint2(self.pipe.end.coords())
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
