import gmsh
from opps.model.pipe import Pipe
from opps.model.bend import Bend
from opps.model.flange import Flange


class StepExporter:
    def __init__(self):
        pass

    def save(self, path, pipeline):
        # print(path)
        # print(pipeline.components)
        lines_guide = []
        gmsh.initialize("", False)
        for component in pipeline.components: 
            if type(component) == Pipe:
                start = (tuple(component.start)[0], tuple(component.start)[1], tuple(component.start)[2])
                end = (tuple(component.end)[0], tuple(component.end)[1], tuple(component.end)[2])

                start_point = gmsh.model.occ.add_point(start[0], start[1], start[2])
                end_point = gmsh.model.occ.add_point(end[0], end[1], end[2])

                gmsh.model.occ.add_line(start_point, end_point)

            # elif type(component) == Bend:
            #     print(component)
            #     start = (tuple(component.start)[0], tuple(component.start)[1], tuple(component.start)[2])
            #     end = (tuple(component.end)[0], tuple(component.end)[1], tuple(component.end)[2])
            #     center = (tuple(component.center)[0], tuple(component.center)[1], tuple(component.center)[2])

                
            #     gmsh.model.occ.add_circle_arc()


               
        # last_point = gmsh.model.occ.add_point(tuple(component.end)[0], tuple(component.end)[1], tuple(component.end)[2])
        # lines_guide.append(last_point)

        # for i in range(len(lines_guide) - 1):
        #     gmsh.model.occ.add_line(lines_guide[i], lines_guide[i+1])
                


        
        gmsh.model.occ.synchronize()
        gmsh.fltk.run()






