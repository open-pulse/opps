import math
from itertools import pairwise

import numpy as np

from opps.model import Bend, Elbow, Flange, Pipe, Point, ReducerEccentric, Valve


class PCFHandler:
    def __init__(self):
        pass

    def load(self, path, pipeline):
        with open(path, "r", encoding="iso_8859_1") as c2:
            lines = c2.readlines()
            groups = self.group_structures(lines)
            pipeline.structures = self.create_classes(groups)

    def group_structures(self, lines_list):
        structures_list = []
        index_list = []
        lines_list.append("")

        for i, line in enumerate(lines_list):
            if line[0:4] != "    ":
                index_list.append(i)
        for a, b in pairwise(index_list):
            structures_list.append(lines_list[a:b])

        return structures_list

    def create_classes(self, groups):
        objects = []
        for group in groups:
            if group[0].strip() in ["PIPE", "PIPE-FIXED", "PIPE-BLOCK-FIXED", "PIPE-BLOCK-VARIABLE"]:
                pipe = self.create_pipe(group)
                objects.append(pipe)

            elif group[0].strip() == "ELBOW":
                elbow = self.create_elbow(group)
                objects.append(elbow)

            elif group[0].strip() == "BEND":
                bend = self.create_bend(group)
                objects.append(bend)

            elif group[0].strip() in ["FLANGE","FLANGE-BLIND"]:
                flange = self.create_flange(group)
                objects.append(flange)

            elif group[0].strip() == "VALVE":
                valve = self.create_valve(group)
                objects.append(valve)

            elif group[0].strip() == "REDUCER-CONCENTRIC":
                reducer = self.create_reducer(group)
                objects.append(reducer)

        return objects
    

    def create_pipe(self, group):

    
        x0, y0, z0, d0 = self.load_parameter("END-POINT", group, occurence=0)
        x1, y1, z1, d1 = self.load_parameter("END-POINT", group, occurence=1)
        thickness, *_ = self.load_parameter("R2_WALL_THK", group, default=[0])

        extra_info = self.extra_info(group)

        start = Point(float(x0) / 1000, float(y0) / 1000, float(z0) / 1000)
        end = Point(float(x1) / 1000, float(y1) / 1000, float(z1) / 1000)
        start_diameter = float(d0) / 1000
        end_diameter = float(d1) / 1000
        thickness = float(thickness)/1000 
        
        if start_diameter == end_diameter:
            return Pipe(start, end, diameter=start_diameter, thickness=thickness, extra_info=extra_info )
        else:
            return ReducerEccentric(start, end, start_diameter=start_diameter, end_diameter=end_diameter, thickness=thickness)

    def create_reducer(self, group):

    
        x0, y0, z0, d0 = self.load_parameter("END-POINT", group, occurence=0)
        x1, y1, z1, d1 = self.load_parameter("END-POINT", group, occurence=1)
        thickness, *_ = self.load_parameter("R2_WALL_THK", group, default=[0])
        

        start = Point(float(x0) / 1000, float(y0) / 1000, float(z0) / 1000)
        end = Point(float(x1) / 1000, float(y1) / 1000, float(z1) / 1000)
        start_diameter = float(d0) / 1000
        end_diameter = float(d1) / 1000
        thickness = float(thickness)/1000 
        
        return ReducerEccentric(start, end, start_diameter=start_diameter, end_diameter=end_diameter, thickness=thickness, color = (251, 177, 60))
        

    def create_bend(self, group):
        x0, y0, z0, d0 = self.load_parameter("END-POINT", group, occurence=0)
        x1, y1, z1, d1 = self.load_parameter("END-POINT", group, occurence=1)
        x2, y2, z2 = self.load_parameter("CENTRE-POINT", group)
        thickness, *_ = self.load_parameter("R2_WALL_THK", group, default=[0])

        extra_info = self.extra_info(group)

        thickness = float(thickness)/1000
        start = Point(float(x0) / 1000, float(y0) / 1000, float(z0) / 1000)
        end = Point(float(x1) / 1000, float(y1) / 1000, float(z1) / 1000)
        corner = Point(float(x2) / 1000, float(y2) / 1000, float(z2) / 1000)
        start_radius = float(d0) / 1000
        end_radius = float(d1) / 1000

        diameter = start_radius

        
        start_coords = np.array([float(x0) / 1000, float(y0) / 1000, float(z0) / 1000])
        end_coords = np.array([float(x1) / 1000, float(y1) / 1000, float(z1) / 1000])
        corner_coords = np.array([float(x2) / 1000, float(y2) / 1000, float(z2) / 1000])

        a_vector = start_coords - corner_coords
        b_vector = end_coords - corner_coords
        c_vector = a_vector + b_vector
        c_vector_normalized = c_vector / np.linalg.norm(c_vector)

        norm_a_vector = np.linalg.norm(a_vector)
        norm_b_vector = np.linalg.norm(b_vector)

        corner_distance = norm_a_vector / np.sqrt(
            0.5 * ((np.dot(a_vector, b_vector) / (norm_a_vector * norm_b_vector)) + 1)
        )

        center_coords = corner_coords + c_vector_normalized * corner_distance

        start_curve_radius = math.dist(center_coords, start_coords)
        end_curve_radius = math.dist(center_coords, end_coords)
        radius = 0.5 * (start_curve_radius + end_curve_radius)

        return Bend(
            start,
            end,
            corner,
            curvature=radius,
            diameter=diameter,
            thickness=thickness,
            auto=False,
            color=(227, 215, 255),
            extra_info=extra_info,
        )

    def create_flange(self, group):
        
        x0, y0, z0, r0 = self.load_parameter("END-POINT", group, occurence=0)
        x1, y1, z1, r1 = self.load_parameter("END-POINT", group, occurence=1)
        thickness, *_ = self.load_parameter("R2_WALL_THK", group, default=[0])

        extra_info = self.extra_info(group)


        start = Point(float(x0) / 1000, float(y0) / 1000, float(z0) / 1000)
        end = Point(float(x1) / 1000, float(y1) / 1000, float(z1) / 1000)
        position = start
        normal = start.coords() - end.coords()
        start_radius = float(r0) / 1000
        thickness = float(thickness)/1000

        return Flange(start, end , diameter = start_radius, thickness=thickness, color = (50, 168, 82), extra_info=extra_info)
    
    def create_valve(self, group):
        x0, y0, z0, r0 = self.load_parameter("END-POINT", group, occurence=0)
        x1, y1, z1, r1 = self.load_parameter("END-POINT", group, occurence=1)
        thickness, *_ = self.load_parameter("R2_WALL_THK", group, default=[0])

        extra_info = self.extra_info(group)

        start = Point(float(x0) / 1000, float(y0) / 1000, float(z0) / 1000)
        end = Point(float(x1) / 1000, float(y1) / 1000, float(z1) / 1000)
        position = start
        normal = start.coords() - end.coords()
        start_radius = float(r0) / 1000
        thickness = float(thickness)/1000

        return Valve(start, end, diameter=start_radius, thickness = thickness, color = (143, 45, 86), extra_info= extra_info )

    def create_elbow(self, group):
        x0, y0, z0, r0 = self.load_parameter("END-POINT", group, occurence=0)
        x1, y1, z1, r1 = self.load_parameter("END-POINT", group, occurence=1)
        x2, y2, z2 = self.load_parameter("CENTRE-POINT", group)
        thickness, *_ = self.load_parameter("R2_WALL_THK", group, default=[0])

        extra_info = self.extra_info(group)

        thickness = float(thickness)/1000
        start = Point(float(x0) / 1000, float(y0) / 1000, float(z0) / 1000)
        end = Point(float(x1) / 1000, float(y1) / 1000, float(z1) / 1000)
        corner = Point(float(x2) / 1000, float(y2) / 1000, float(z2) / 1000)
        start_radius = float(r0) / 1000
        end_radius = float(r1) / 1000

        start_coords = np.array([float(x0) / 1000, float(y0) / 1000, float(z0) / 1000])
        end_coords = np.array([float(x1) / 1000, float(y1) / 1000, float(z1) / 1000])
        corner_coords = np.array([float(x2) / 1000, float(y2) / 1000, float(z2) / 1000])

        a_vector = start_coords - corner_coords
        b_vector = end_coords - corner_coords
        c_vector = a_vector + b_vector
        c_vector_normalized = c_vector / np.linalg.norm(c_vector)

        norm_a_vector = np.linalg.norm(a_vector)
        norm_b_vector = np.linalg.norm(b_vector)

        corner_distance = norm_a_vector / np.sqrt(
            0.5 * ((np.dot(a_vector, b_vector) / (norm_a_vector * norm_b_vector)) + 1)
        )

        center_coords = corner_coords + c_vector_normalized * corner_distance

        start_curve_radius = math.dist(center_coords, start_coords)
        end_curve_radius = math.dist(center_coords, end_coords)
        radius = 0.5 * (start_curve_radius + end_curve_radius)

        return Bend(
            start,
            end,
            corner,
            curvature=radius,
            diameter = start_radius,
            thickness=thickness,
            auto=False,
            color = (115, 210, 222),
            extra_info= extra_info
        )
        # return Elbow(
        #     start,
        #     end,
        #     corner,
        #     curvature=radius,
        #     start_diameter=start_radius,
        #     end_diameter=end_radius,
        #     thickness=thickness,
        #     auto=False,
        # )

    def load_parameter(
        self, parameter_name: str, group: list[str], occurence: int = 0, default = None
    ) -> list[str]:
        current_occurrence = 0

        for line in group:
            if parameter_name not in line:
                continue
            parts = line.split()
            if parts[0] != parameter_name:
                continue
            if current_occurrence == occurence:
                return parts[1:]

            current_occurrence += 1
        
        if default is None:
            return []
        else: 
            return default
        
    def extra_info(self,group):

        pressure_data = self.load_parameter("R2_DESIGN_PRESS", group)
        temperature_data = self.load_parameter("R2_DESIGN_TEMP", group)
        material_data = self.load_parameter("R2_MATERIAL", group)

        extra_info = dict()

        if len(pressure_data) > 0:
            extra_info["pressure"] = pressure_data[0]
        if len(temperature_data) > 0:
            extra_info["temperature"] = temperature_data[0]
        if len(material_data) > 0:
            extra_info["material"] = material_data[0]

        print (extra_info)

        

