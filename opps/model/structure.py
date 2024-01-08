class Structure:
    selected: bool = False

    def get_points(self):
        raise NotImplementedError()

    def as_vtk(self):
        raise NotImplementedError("vtk actor creation not implemented.")