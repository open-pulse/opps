from itertools import pairwise
from opps.model.pipe import Pipe

with open('P-29213_1.pcf') as c2:
     lines = c2.readlines()

def group_structures(lines_list):

    structures_list = []
    index_list = []
    for i,line in enumerate(lines_list):
        if line[0:4] != "    ":
            index_list.append(i)
    for a,b in pairwise(index_list):
        structures_list.append(lines_list[a:b])

    return structures_list

def create_classes(groups):
    objects = []
    for group in groups:
        if group[0].strip() == "PIPE":
            pipe = create_pipe(group)
            objects.append(pipe)
    return objects

def create_pipe(group):
    _,x0,y0,z0,r0 = group[1].split()
    _,x1,y1,z1,r1 = group[2].split()
  
    start = (float(x0), float(y0), float(z0))
    end = (float(x1), float(y1), float(z1))
    radius = float(r0)

    return Pipe(start, end, radius)

groups = group_structures(lines)    
create_classes(groups)


