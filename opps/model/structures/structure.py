from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opps.model import Point


class Structure:
    def __init__(self, **kwargs) -> None:
        self.color = kwargs.get("color", [255, 255, 255])
        self.selected = kwargs.get("selected", False)
        self.staged = kwargs.get("staged", False)
        self.tag = kwargs.get("tag", -1)
        self.extra_info = kwargs.get("extra_info", dict())

    def get_points(self) -> list["Point"]:
        raise NotImplementedError("get_points method not implemented")

    def replace_point(self, old, new):
        raise NotImplementedError("replace_point method not implemented")

    def as_dict(self) -> dict:
        return {
            "color": self.color,
            "tag": self.tag,
            "extra_info": self.extra_info,
        }

    def as_vtk(self):
        raise NotImplementedError("vtk actor creation not implemented.")

    def __hash__(self) -> int:
        return id(self)
