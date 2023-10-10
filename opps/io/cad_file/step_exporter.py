import gmsh


class StepExporter:
    def __init__(self):
        pass

    def save(self, path, pipeline):
        # print(path)
        # print(pipeline.components)
        
        for component in pipeline.components:   
            print(type(component))

    x0 = 0
    y0 = 0 # these need to be the coordinates of the last x, y, z plus the dx, dy, dz
    z0 = 0
    gmsh.model.occ.add_cylinder(x0, y0, z0, dx, dy, dz, r, -1) # it adds a cap to the cylinder, need to solve this  
    # gmsh.model.occ.add_torus()? #for the bends; Maybe there is a better way to do this, perhaps using a curved line and sweeping a circle on it
    # add_flange needs to be modeled in some CAD 
    