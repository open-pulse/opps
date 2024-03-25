import vtk
from vtkat.actors import RoundPointsActor


class SelectedPointsActor(RoundPointsActor):
    def __init__(self, points):
        coords = [p.coords() for p in points]
        super().__init__(coords)
        self.GetProperty().SetColor((1, 0, 0))
        self.appear_in_front(True)
