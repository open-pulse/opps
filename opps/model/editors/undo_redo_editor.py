from dataclasses import dataclass
from collections import deque
from typing import TYPE_CHECKING
from .editor import Editor

from pprint import pprint

if TYPE_CHECKING:
    from opps.model.pipeline import Pipeline
    from opps.model.structures import Point, Structure


@dataclass(frozen=True, slots=True)
class PipelineSnapshot:
    points: tuple['Point']
    structures: tuple['Structure']

    @classmethod
    def from_pipeline(cls, pipeline: 'Pipeline'):
        points_copy = tuple(point.copy() for point in pipeline.points)
        structures_copy = tuple(
            structure.copy() for structure in pipeline.structures
            if not structure.staged
        )
        for structure in structures_copy:
            structure.selected = False
        return cls(points_copy, structures_copy)

    def update_pipeline(self, pipeline: 'Pipeline'):
        pipeline.dismiss()
        pipeline.clear_selection()
        pipeline.points = list(self.points)
        pipeline.structures = list(self.structures)


class UndoRedoEditor(Editor):
    def __init__(self, pipeline: 'Pipeline') -> None:
        super().__init__(pipeline)
        self.undo_stack: deque[PipelineSnapshot] = deque()
        self.redo_stack: deque[PipelineSnapshot] = deque()
        self.max_undos = 10

    def undo(self):
        if not self.can_undo():
            return
        
        current_snapshot = PipelineSnapshot.from_pipeline(self.pipeline)
        self.redo_stack.append(current_snapshot)

        snapshot = self.undo_stack.pop()
        snapshot.update_pipeline(self.pipeline)

    def redo(self):
        if not self.can_redo():
            return
        
        current_snapshot = PipelineSnapshot.from_pipeline(self.pipeline)
        self.undo_stack.append(current_snapshot)
        
        snapshot = self.redo_stack.pop()
        snapshot.update_pipeline(self.pipeline)
        self._keep_max_size()

    def push(self):
        snapshot = PipelineSnapshot.from_pipeline(self.pipeline)
        self.undo_stack.append(snapshot)
        self.redo_stack.clear()
        self._keep_max_size()

    def can_undo(self):
        return len(self.undo_stack) != 0

    def can_redo(self):
        return len(self.redo_stack) != 0

    def _keep_max_size(self):
        # remove the oldest snapshot if the stack is full
        while len(self.undo_stack) > self.max_undos:
            self.undo_stack.popleft()
