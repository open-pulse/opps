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

            if isinstance(component, Pipe):
                start_point = gmsh.model.occ.add_point(*component.start)
                end_point = gmsh.model.occ.add_point(*component.end)

                gmsh.model.occ.add_line(start_point, end_point)

            elif isinstance(component, Bend):
                start_point = gmsh.model.occ.add_point(*component.start)
                end_point = gmsh.model.occ.add_point(*component.end)
                center_point = gmsh.model.occ.add_point(*component.center)

                gmsh.model.occ.add_circle_arc(start_point, center_point, end_point)

        gmsh.model.occ.synchronize()
        gmsh.write(path)
        gmsh.fltk.run()






