import gmsh
from opps.model.pipe import Pipe
from opps.model.bend import Bend
from opps.model.flange import Flange


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
    
    def open(self, path):
        gmsh.initialize("", False)
        gmsh.option.setNumber("General.Verbosity", 0)
        gmsh.open(str(path))
        
        points = gmsh.model.get_entities(0)
        lines = gmsh.model.get_entities(1)

        print(gmsh.model.getType(1,1))
        print(gmsh.model.getType(1,2))
        
        
        gmsh.fltk.run()





