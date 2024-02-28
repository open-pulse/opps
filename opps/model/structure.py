class Structure:
    color: tuple[int, int, int] = (255, 255, 255)
    selected: bool = False
    staged: bool = False
    tag: int = -1

    __extra_info: dict = None

    @property
    def extra_info(self):
        if self.__extra_info is None:
            self.__extra_info = dict()
        return self.__extra_info

    def get_points(self):
        raise NotImplementedError()

    def as_vtk(self):
        raise NotImplementedError("vtk actor creation not implemented.")

    def __hash__(self) -> int:
        return id(self)
