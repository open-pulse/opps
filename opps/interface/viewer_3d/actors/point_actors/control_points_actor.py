import vtk
from vtkat.poly_data import VerticesData


class ControlPointsActor(vtk.vtkActor):
    def __init__(self, points):
        super().__init__()
        self.points = points
        self.build()

    def build(self):
        coords = [p.coords() for p in self.points]
        data = VerticesData(coords)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(data)
        self.SetMapper(mapper)

        self.GetProperty().SetPointSize(15)
        self.GetProperty().RenderPointsAsSpheresOn()
        self.GetProperty().SetColor([i / 255 for i in (255, 180, 50)])
        self.GetProperty().LightingOff()

        offset = -66000
        mapper.SetResolveCoincidentTopologyToPolygonOffset()
        mapper.SetRelativeCoincidentTopologyLineOffsetParameters(0, offset)
        mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, offset)
        mapper.SetRelativeCoincidentTopologyPointOffsetParameter(offset)
