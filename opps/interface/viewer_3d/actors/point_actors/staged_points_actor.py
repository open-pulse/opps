import vtk
from vtkat.poly_data import VerticesData


class StagedPointsActor(vtk.vtkActor):
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

        self.GetProperty().SetPointSize(13)
        self.GetProperty().SetColor([1, 0, 0])
        self.GetProperty().LightingOff()

        offset = -66000
        mapper.SetResolveCoincidentTopologyToPolygonOffset()
        mapper.SetRelativeCoincidentTopologyLineOffsetParameters(0, offset)
        mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, offset)
        mapper.SetRelativeCoincidentTopologyPointOffsetParameter(offset)
