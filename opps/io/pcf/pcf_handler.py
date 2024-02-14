from itertools import pairwise

import numpy as np

from opps.model.bend import Bend
from opps.model.elbow import Elbow
from opps.model.flange import Flange
from opps.model.pipe import Pipe
from opps.model.point import Point


def group_structures(lines_list):
    structures_list = []
    index_list = []
    for i, line in enumerate(lines_list):
        if line[0:4] != "    ":
            index_list.append(i)
    for a, b in pairwise(index_list):
        structures_list.append(lines_list[a:b])

    return structures_list


def create_classes(groups):
    objects = []
    for group in groups:
        if group[0].strip() == "PIPE":
            pipe = create_pipe(group)
            objects.append(pipe)

        elif group[0].strip() == "BEND":
            bend = create_bend(group)
            objects.append(bend)

        elif group[0].strip() == "FLANGE":
            flange = create_flange(group)
            objects.append(flange)

        elif group[0].strip() == "ELBOW":
            elbow = create_elbow(group)
            objects.append(elbow)

    return objects


def create_pipe(group):
    _, x0, y0, z0, r0 = group[1].split()
    _, x1, y1, z1, r1 = group[2].split()

    start = Point(float(x0), float(y0), float(z0))
    end = Point(float(x1), float(y1), float(z1))
    radius = float(r0) / 2

    return Pipe(start, end, radius, radius)


def create_bend(group):
    _, x0, y0, z0, r0 = group[1].split()
    _, x1, y1, z1, r1 = group[2].split()
    _, x2, y2, z2 = group[3].split()
    _, curvature = group[6].split()

    start = Point(float(x0), float(y0), float(z0))
    end = Point(float(x1), float(y1), float(z1))
    center = Point(float(x2), float(y2), float(z2))
    start_radius = float(r0) / 2
    end_radius = float(r1) / 2
    curvature = float(curvature)

    color = (255, 0, 0)

    return Bend(
        start,
        end,
        center,
        curvature=curvature,
        start_diameter=start_radius,
        end_diameter=end_radius,
        color=color,
        auto=False,
    )


def create_flange(group):
    _, x0, y0, z0, r0 = group[1].split()
    _, x1, y1, z1, r1 = group[2].split()

    start = Point(float(x0), float(y0), float(z0))
    end = Point(float(x1), float(y1), float(z1))
    position = start
    normal = start.coords() - end.coords()
    start_radius = float(r0) / 2

    color = (0, 0, 255)

    return Flange(position, normal, start_radius, color=color)


def create_elbow(group):
    _, x0, y0, z0, r0 = group[1].split()
    _, x1, y1, z1, r1 = group[2].split()
    _, x2, y2, z2 = group[3].split()

    start = Point(float(x0), float(y0), float(z0))
    end = Point(float(x1), float(y1), float(z1))
    center = Point(float(x2), float(y2), float(z2))
    start_radius = float(r0) / 2
    end_radius = float(r1) / 2

    color = (0, 255, 0)

    return Elbow(
        start,
        end,
        center,
        curvature=1.5 * start_radius,
        start_diameter=start_radius,
        end_diameter=end_radius,
        color=color,
        auto=False,
    )
