from .point import Point
from .structure import Structure


class LinearStructure(Structure):
    def __init__(self, start: Point, end: Point, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.start = start
        self.end = end

    def get_points(self):
        return [
            self.start,
            self.end,
        ]

    def replace_point(self, old, new):
        if self.start == old:
            self.start = new

        elif self.end == old:
            self.end = new

    def as_dict(self) -> dict:
        return super().as_dict() | {
            "start": self.start,
            "end": self.end,
        }
