from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from opps.model import Pipeline


class Editor:
    def __init__(self, pipeline: "Pipeline") -> None:
        self.pipeline = pipeline