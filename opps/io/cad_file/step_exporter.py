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






