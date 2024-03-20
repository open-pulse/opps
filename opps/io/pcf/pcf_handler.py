from itertools import pairwise

import numpy as np
import math

from opps.model.bend import Bend
from opps.model.elbow import Elbow
from opps.model.flange import Flange
from opps.model.pipe import Pipe
from opps.model.point import Point


class PCFHandler:
    def __init__(self):
        pass

    def load(self, path, pipeline):

        with open(path, "r", encoding="iso_8859_1") as c2:
            lines = c2.readlines()
            groups = self.group_structures(lines)
            pipeline.structures = self.create_classes(groups)

    def group_structures(self,lines_list):
        structures_list = []
        index_list = []
        lines_list.append("")

        for i, line in enumerate(lines_list):
            if line[0:4] != "    ":
                index_list.append(i)
        for a, b in pairwise(index_list):
            structures_list.append(lines_list[a:b])

        return structures_list


    def create_classes(self,groups):
        objects = []
        for group in groups:
            if group[0].strip() == "PIPE":
                pipe = self.create_pipe(group)
                objects.append(pipe)

            elif group[0].strip() == "BEND":
                bend = self.create_bend(group)
                objects.append(bend)

            elif group[0].strip() == "FLANGE":
                flange = self.create_flange(group)
                objects.append(flange)

            elif group[0].strip() == "ELBOW":
                elbow = self.create_elbow(group)
                objects.append(elbow)

        return objects


    def create_pipe(self,group):
        x0, y0, z0, r0 = self.load_parameter("END-POINT", group, occurence=0)
        x1, y1, z1, r1 = self.load_parameter("END-POINT", group, occurence=1)

        start = Point(float(x0), float(y0), float(z0))
        end = Point(float(x1), float(y1), float(z1))
        radius = float(r0) 

        return Pipe(start, end, radius, radius)

    def create_bend(self,group):
        x0, y0, z0, d0 = self.load_parameter("END-POINT", group, occurence= 0)
        x1, y1, z1, d1 = self.load_parameter("END-POINT", group, occurence= 1)
        x2, y2, z2 = self.load_parameter("CENTRE-POINT", group)

        start = Point(float(x0), float(y0), float(z0))
        end = Point(float(x1), float(y1), float(z1))
        corner = Point(float(x2), float(y2), float(z2))
        start_radius = float(d0) 
        end_radius = float(d1) 

        start_coords = np.array([float(x0), float(y0), float(z0)])
        end_coords = np.array([float(x1), float(y1), float(z1)])
        corner_coords = np.array([float(x2), float(y2), float(z2)])

        a_vector = start_coords - corner_coords
        b_vector = end_coords - corner_coords
        c_vector = a_vector + b_vector
        c_vector_normalized = c_vector / np.linalg.norm(c_vector)

        norm_a_vector = np.linalg.norm(a_vector)
        norm_b_vector = np.linalg.norm(b_vector)

        corner_distance = norm_a_vector / np.sqrt(0.5 * ((np.dot(a_vector, b_vector) / (norm_a_vector * norm_b_vector)) + 1))

        center_coords = corner_coords + c_vector_normalized * corner_distance

        start_curve_radius = math.dist(center_coords, start_coords)
        end_curve_radius = math.dist(center_coords, end_coords)
        radius = 0.5 * (start_curve_radius + end_curve_radius)
        
        return Bend(
            start,
            end,
            corner,  
            curvature = radius,
            start_diameter = start_radius,
            end_diameter = end_radius,
            auto = False,
        )


    def create_flange(self,group):
        x0, y0, z0, r0 = self.load_parameter("END-POINT", group, occurence= 0)
        x1, y1, z1, r1 = self.load_parameter("END-POINT", group, occurence= 1)

        start = Point(float(x0), float(y0), float(z0))
        end = Point(float(x1), float(y1), float(z1))
        position = start
        normal = start.coords() - end.coords()
        start_radius = float(r0) 

        return Flange(position, normal, start_radius)


    def create_elbow(self,group):
        x0, y0, z0, r0 = self.load_parameter("END-POINT", group, occurence= 0)
        x1, y1, z1, r1 = self.load_parameter("END-POINT", group, occurence= 1)
        x2, y2, z2 = self.load_parameter("CENTRE-POINT", group)

        start = Point(float(x0), float(y0), float(z0))
        end = Point(float(x1), float(y1), float(z1))
        corner = Point(float(x2), float(y2), float(z2))
        start_radius = float(r0) 
        end_radius = float(r1) 

        start_coords = np.array([float(x0), float(y0), float(z0)])
        end_coords = np.array([float(x1), float(y1), float(z1)])
        corner_coords = np.array([float(x2), float(y2), float(z2)])

        a_vector = start_coords - corner_coords
        b_vector = end_coords - corner_coords
        c_vector = a_vector + b_vector
        c_vector_normalized = c_vector / np.linalg.norm(c_vector)

        norm_a_vector = np.linalg.norm(a_vector)
        norm_b_vector = np.linalg.norm(b_vector)

        corner_distance = norm_a_vector / np.sqrt(0.5 * ((np.dot(a_vector, b_vector) / (norm_a_vector * norm_b_vector)) + 1))

        center_coords = corner_coords + c_vector_normalized * corner_distance

        start_curve_radius = math.dist(center_coords, start_coords)
        end_curve_radius = math.dist(center_coords, end_coords)
        radius = 0.5 * (start_curve_radius + end_curve_radius)

        return Elbow(
            start,
            end,
            corner,
            curvature=radius,
            start_diameter=start_radius,
            end_diameter=end_radius,
            auto=False,
        )

    def load_parameter(self, parameter_name: str, group: list[str], occurence: int = 0) -> list[str]:
        parameters = []
        current_occurrence = 0
    
        for line in group:
            if parameter_name in line:
                parts = line.split()

                if parts[0] == parameter_name:
                    
                    if current_occurrence == occurence:                    
                        parameters.extend(parts[1:])
                        return parameters
                    
                    current_occurrence += 1
                    
        return (parameters)