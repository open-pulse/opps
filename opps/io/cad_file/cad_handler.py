import gmsh

from opps.model import Bend, Flange, Pipe


class CADHandler:
    def save(self, path, pipeline):
        gmsh.initialize("", False)
        for i, structure in enumerate(pipeline.structures, 1):
            # The tag of the structures isn't really a thing after the
            # file is saved, but at least it preserves the desired ordering.

            if isinstance(structure, Pipe):
                start_point = gmsh.model.occ.add_point(*structure.start.coords())
                end_point = gmsh.model.occ.add_point(*structure.end.coords())

                gmsh.model.occ.add_line(start_point, end_point, tag=i)

            elif isinstance(structure, Bend):
                if structure.is_colapsed():
                    continue

                start_point = gmsh.model.occ.add_point(*structure.start.coords())
                end_point = gmsh.model.occ.add_point(*structure.end.coords())
                center_point = gmsh.model.occ.add_point(*structure.center.coords())

                gmsh.model.occ.add_circle_arc(start_point, center_point, end_point, tag=i)

        gmsh.model.occ.synchronize()
        gmsh.write(str(path))
