import gmsh
from opps.model.pipe import Pipe
from opps.model.bend import Bend
from opps.model.flange import Flange


class StepExporter:
    def __init__(self):
        pass

    def save(self, path, pipeline):

        gmsh.initialize("", False)
        for component in pipeline.components: 

            if type(component) == Pipe:
                start = (tuple(component.start)[0], tuple(component.start)[1], tuple(component.start)[2])
                end = (tuple(component.end)[0], tuple(component.end)[1], tuple(component.end)[2])

                start_point = gmsh.model.occ.add_point(start[0], start[1], start[2])
                end_point = gmsh.model.occ.add_point(end[0], end[1], end[2])

                gmsh.model.occ.add_line(start_point, end_point)

            elif type(component) == Bend:
                print(component)
                start = (tuple(component.start)[0], tuple(component.start)[1], tuple(component.start)[2])
                end = (tuple(component.end)[0], tuple(component.end)[1], tuple(component.end)[2])
                center = (tuple(component.center)[0], tuple(component.center)[1], tuple(component.center)[2])

                start_point = gmsh.model.occ.add_point(start[0], start[1], start[2])
                end_point = gmsh.model.occ.add_point(end[0], end[1], end[2])
                center_point = gmsh.model.occ.add_point(center[0], center[1], center[2])

                gmsh.model.occ.add_circle_arc(start_point, center_point, end_point)

            # elif type(component) == Flange:
            #     print(component)
            #     position = (tuple(component.position)[0], tuple(component.position)[1], tuple(component.position)[2])
            #     position_point = gmsh.model.occ.add_point(position[0], position[1], position[2])
            #     gmsh.model.occ.add_circle()

            # there's still the flange left to do, the idea is to create a circle to denote it
            # duplicate points are being created on the end and start of pipes (lines)

        gmsh.model.occ.synchronize()
        gmsh.write("YourFile.step")
        # gmsh.fltk.run()






