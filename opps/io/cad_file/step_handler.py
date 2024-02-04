import gmsh
import math
import numpy as np
from opps.model.pipe import Pipe
from opps.model.bend import Bend
from opps.model import Point
from opps.model.pipeline_editor import PipelineEditor


class StepHandler:
    def __init__(self):
        pass

    def save(self, path, pipeline):
        gmsh.initialize("", False)
        for component in pipeline.components: 

            if isinstance(component, Pipe):
                start_point = gmsh.model.occ.add_point(*component.start.coords())
                end_point = gmsh.model.occ.add_point(*component.end.coords())

                gmsh.model.occ.add_line(start_point, end_point)

            elif isinstance(component, Bend):
                if (component.start.coords() == component.end.coords()).all():
                    continue
                start_point = gmsh.model.occ.add_point(*component.start.coords())
                end_point = gmsh.model.occ.add_point(*component.end.coords())
                center_point = gmsh.model.occ.add_point(*component.center.coords())

                gmsh.model.occ.add_circle_arc(start_point, center_point, end_point)

        gmsh.model.occ.synchronize()
        gmsh.write(str(path))
    
    def open(self, path, pipeline):
        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.open(str(path))

        structures = [] 
        points = gmsh.model.get_entities(0)
        lines = gmsh.model.get_entities(1)
        
        points_coords = []
        for point in points: 
            coords = gmsh.model.getValue(*point, [])
            points_coords.append((point[1], (coords)))

        associated_points = []
        for line in lines:
            associated_points.append(gmsh.model.get_adjacencies(*line)[1][0])
            associated_points.append(gmsh.model.get_adjacencies(*line)[1][1])

        center_points = []
        for point in points:
            if point[1] not in associated_points:
                center_points.append(point[1])

        for line in lines: 
            start_point = gmsh.model.get_adjacencies(*line)[1][0]
            end_point = gmsh.model.get_adjacencies(*line)[1][1]
            type = gmsh.model.get_type(*line)

            start_coords = (points_coords[start_point -1][1])
            end_coords = (points_coords[end_point -1][1])

            start = Point(*start_coords)
            end = Point(*end_coords)

            if type == 'Line':
                pipe = Pipe(start, end)

            elif type == 'Circle':
                for point in center_points:
                    start_radius = math.dist(start_coords, points_coords[point-1][1])
                    end_radius = math.dist(end_coords, points_coords[point-1][1])
                    if start_radius - end_radius <= 1e-14:
                        center_point = point
                center_coords = np.array(points_coords[center_point - 1][1])
                start_coords = np.array(start_coords)
                end_coords = np.array(end_coords)
                # vectorial sum
                v = start_coords - center_coords + end_coords - center_coords
                corner_coords = center_coords + 2*v

                corner = Point(*corner_coords)
                pipe = Bend(start, end, corner, start_radius)

            structures.append(pipe)

        pipeline.components = structures
        
        gmsh.fltk.run()





