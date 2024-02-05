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
        var = self.encoder(pipeline)
         
        with open(path, "w", encoding="iso_8859_1") as file:
             file.write(var)
    
    def encoder(self, pipeline):

        string = self.encoder_header(pipeline) 

        for structure in pipeline.structures:
            if isinstance(structure, Pipe):
                stringer = self.encoder_pipe(structure)
                string = string + "\n" + stringer

            elif isinstance(structure, Elbow):
                stringer = self.encoder_elbow(structure)
                string = string + "\n" + stringer
            
            elif isinstance(structure, Bend):
                stringer = self.encoder_bend(structure)
                string = string + "\n" + stringer

            elif isinstance(structure, Flange):
                stringer = self.encoder_flange(structure)
                string = string + "\n" + stringer


                
        return string

    def encoder_header(self, pipeline):
    
        string = """ISOGEN-FILES            ISOGEN.FLS
UNITS-BORE              INCH
   

UNITS-CO-ORDS           MM

UNITS-BOLT-LENGTH       MM

UNITS-BOLT-DIA          MM

UNITS-WEIGHT            KGS

PIPELINE-REFERENCE      CFG1

    PIPING-SPEC         CS150

    START-CO-ORDS       0.0000       0.0000      0.0000 """
    
        return string


    def encoder_pipe(self, pipe):
       string = f""" PIPE
    END-POINT            {round(pipe.start.x, 2)}      {round(pipe.start.y, 2)}       {round(pipe.start.z, 2)}         {round(pipe.start_diameter, 2)}  
    END-POINT            {round(pipe.end.x, 2)}      {round(pipe.end.y, 2)}        {round(pipe.end.z, 2)}            {round(pipe.end_diameter, 2)}   """
       
       return string
    
    def encoder_bend(self, bend):
       string = f""" BEND
    END-POINT        {round(bend.start.x, 2)}   {round(bend.start.y, 2)}    {round(bend.start.z, 2)}       {round(bend.start_diameter,2)}  
    END-POINT        {round(bend.end.x, 2)}   {round(bend.end.y, 2)}   {round(bend.end.z, 2)}       {round(bend.end_diameter, 2)}   
    CENTRE-POINT     {round(bend.corner.x, 2)}   {round(bend.corner.y, 2)}    {round(bend.corner.z, 2)}   
    SKEY BEBW
    """
       
       return string

    def encoder_flange(self, flange):
       end_x = round(flange.position.x + flange.normal[0], 2)
       end_y = round(flange.position.y + flange.normal[1], 2)
       end_z = round(flange.position.z + flange.normal[2], 2)

       string = f""" FLANGE
    END-POINT    {round(flange.position.x, 2)}   {round(flange.position.y, 2)}       {round(flange.position.z, 2)}       {round(flange.diameter, 2)}   
    END-POINT    {end_x}   {end_y}       {end_z}       {round(flange.diameter, 2)}   
    SKEY FLBL
    """
       
       return string
    
    def encoder_elbow(self, bend):
       
       string = f""" ELBOW
    END-POINT            {round(bend.start.x,2)}     {round(bend.start.y,2)}       {round(bend.start.z,2)}        {round(bend.start_diameter,2)}   
    END-POINT            {round(bend.end.x ,2)}  {round(bend.end.y,2)}     {round(bend.end.z ,2)}        {round(bend.end_diameter,2)}   
    CENTRE-POINT         {round(bend.corner.x,2)}   {round(bend.corner.y,2)}    {round(bend.corner.z,2)}        
    SKEY                 ELBW
    """
       
       return string
    
    
