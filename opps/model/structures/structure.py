from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opps.model import Point

from copy import deepcopy


class Structure:
    def __init__(self, **kwargs) -> None:
        self.color = kwargs.get("color", [255, 255, 255])
        self.selected = kwargs.get("selected", False)
        self.staged = kwargs.get("staged", False)
        self.tag = kwargs.get("tag", -1)
        self.extra_info = kwargs.get("extra_info", dict())

    def get_points(self) -> list["Point"]:
        raise NotImplementedError(f'get_points method not implemented in "{type(self).__name__}".')

    def replace_point(self, old, new):
        raise NotImplementedError(f'replace_point method not implemented in "{type(self).__name__}".')

    def as_dict(self) -> dict:
        return {
            "color": self.color,
            "tag": self.tag,
            "extra_info": self.extra_info,
        }

    def copy(self):
        return deepcopy(self)

    def as_vtk(self):
        raise NotImplementedError(f'as_vtk method not implemented in "{type(self).__name__}".')

    def __hash__(self) -> int:
        return id(self)
