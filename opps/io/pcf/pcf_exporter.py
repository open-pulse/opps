from itertools import pairwise

import numpy as np

from opps.model.bend import Bend
from opps.model.elbow import Elbow
from opps.model.flange import Flange
from opps.model.pipe import Pipe
from opps.model.point import Point

class PCFExporter:
    def __init__(self) -> None:
        pass

    def save(self, path, pipeline):
        var = self.stringer(pipeline)
         
        with open(path, "w", encoding="iso_8859_1") as file:
             file.write(var)
    
    def stringer(self, pipeline):
        string = ""
        for structure in pipeline.structures:
            if isinstance(structure, Pipe):
                stringer = self.stringer_pipe(structure)
                string = string + "\n" + stringer

        return string

    def stringer_pipe(self, pipe):
       string = f""" PIPE
    END-POINT            {pipe.start.x}      342.00       0.00         300.00  
    END-POINT            -116.00      342.00       0.00         300.00  """
       return string

    
