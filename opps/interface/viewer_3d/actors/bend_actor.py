import vtk

from opps.model.bend import Bend


class BendActor(vtk.vtkActor):
    def __init__(self, bend: Bend):
        self.bend = bend
        self.create_geometry()

    def create_geometry(self):
        arc_source = vtk.vtkArcSource()
        arc_source.SetPoint1(self.bend.start)
        arc_source.SetPoint2(self.bend.end)
        arc_source.SetCenter(self.bend.center)
        arc_source.SetResolution(20)
        arc_source.Update()

        tube_filter = vtk.vtkTubeFilter()
        tube_filter.SetInputData(arc_source.GetOutput())
        tube_filter.SetRadius(self.bend.diameter / 2)
        tube_filter.SetNumberOfSides(20)
        tube_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(tube_filter.GetOutput())
        self.SetMapper(mapper)
