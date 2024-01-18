import vtk 
from vtkat.actors import SquarePointsActor


class PassivePointsActor(SquarePointsActor):
    def __init__(self, points):
        coords = [p.coords() for p in points]
        super().__init__(coords)
        self.GetProperty().SetColor([i/255 for i in (255, 200, 110)])
        self.GetProperty().SetPointSize(12)
        self.appear_in_front(True)
