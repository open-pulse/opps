import vtk

from opps.model.pipe import Pipe


class PipeActor(vtk.vtkActor):
    def __init__(self, pipe: Pipe):
        self.pipe = pipe
        self.create_geometry()

    def create_geometry(self):
        line_source = vtk.vtkLineSource()
        line_source.SetPoint1(self.pipe.start)
        line_source.SetPoint2(self.pipe.end)
        line_source.Update()

        tube_filter = vtk.vtkTubeFilter()
        tube_filter.SetInputData(line_source.GetOutput())
        tube_filter.SetRadius(self.pipe.radius)
        tube_filter.SetNumberOfSides(50)
        tube_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(tube_filter.GetOutput())
        self.SetMapper(mapper)
