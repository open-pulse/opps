class Structure:
    selected: bool = False
    staged: bool = False

    def get_points(self):
        raise NotImplementedError()

    def as_vtk(self):
        raise NotImplementedError("vtk actor creation not implemented.")

    def __hash__(self) -> int:
        return id(self)
