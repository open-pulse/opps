from itertools import pairwise

import numpy as np

from opps.model.bend import Bend
from opps.model.pipe import Pipe
from opps.model.flange import Flange


class Pipeline:
    def __init__(self):
        self.components = []

    def add_pipe(self, *args, **kwargs):
        self.add_structure(Pipe(*args, **kwargs))

    def add_bend(self, *args, **kwargs):
        self.add_structure(Bend(*args, **kwargs))
    
    def add_flange(self, *args, **kwargs):
        self.add_structure(Flange(*args, **kwargs))

    def add_structure(self, structure):
        self.components.append(structure)

    def add_pipe_from_points(self, *points):
        points = np.array(points)

        pipes = []
        for point_a, point_b in pairwise(points):
            pipe = Pipe(point_a, point_b, 40)
            pipes.append(pipe)

        flanges = []
        bends = []
        for pipe_a, pipe_b in pairwise(pipes):
            bend = self.replace_corner_with_bend(pipe_a, pipe_b)
            bends.append(bend)

            flange = Flange(pipe_a.end, (pipe_a.end - pipe_a.start), pipe_a.radius)
            flanges.append(flange)

        self.components.extend(pipes)
        self.components.extend(bends)
        self.components.extend(flanges)

    def add_pipe_from_deltas(self, *deltas, start_point=(0, 0, 0)):
        points = [np.array(start_point)]
        for delta in deltas:
            next_point = points[-1] + np.array(delta)
            points.append(next_point)
        self.add_pipe_from_points(*points)

    def replace_corner_with_bend(self, pipe_a, pipe_b):
        def normalize(vector):
            return vector / np.linalg.norm(vector)

        r = pipe_a.radius * 2

        a_vector = normalize(pipe_a.end - pipe_a.start)
        b_vector = normalize(pipe_b.end - pipe_b.start)
        c_vector = normalize((a_vector + b_vector) / 2 - a_vector)

        sin_angle = np.linalg.norm(a_vector + b_vector) / np.linalg.norm(a_vector) / 2
        angle = np.arcsin(sin_angle)

        center_distance = r / np.sin(angle)
        reduction_distance = center_distance * np.cos(angle)

        bend = Bend(
            start=pipe_a.end - a_vector * reduction_distance,
            end=pipe_b.start + b_vector * reduction_distance,
            center=pipe_a.end + c_vector * center_distance,
            start_radius=pipe_a.radius,
            end_radius=pipe_b.radius,
        )

        # resize the input tubes to fit the bend
        pipe_a.end = bend.start
        pipe_b.start = bend.end

        return bend

    def as_vtk(self):
        from opps.interface.viewer_3d.actors.pipeline_actor import (
            PipelineActor,
        )

        return PipelineActor(self)
