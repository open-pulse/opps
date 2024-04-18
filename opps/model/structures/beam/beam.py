from opps.model.structures.structure import Structure, Point


class Beam(Structure):
    def get_points(self) -> list[Point]:
        return [self.start, self.end]

    def replace_point(self, old, new):
        if self.start == old:
            self.start = new

        elif self.end == old:
            self.end = new
