import gmsh
from opps.model.pipe import Pipe
from opps.model.bend import Bend
from opps.model.flange import Flange


class CADHandler:
    def __init__(self):
        pass

    def save(self, path, pipeline):
        gmsh.initialize("", False)
        for structure in pipeline.structures: 

            if isinstance(structure, Pipe):
                start_point = gmsh.model.occ.add_point(*structure.start.coords())
                end_point = gmsh.model.occ.add_point(*structure.end.coords())

                gmsh.model.occ.add_line(start_point, end_point)

            elif isinstance(structure, Bend):
                if structure.is_colapsed():
                    continue
                start_point = gmsh.model.occ.add_point(*structure.start.coords())
                end_point = gmsh.model.occ.add_point(*structure.end.coords())
                center_point = gmsh.model.occ.add_point(*structure.center.coords())

                gmsh.model.occ.add_circle_arc(start_point, center_point, end_point)

        gmsh.model.occ.synchronize()
        gmsh.write(str(path))






