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

    START-CO-ORDS       0.0000       0.0000       0.0000 """
    
        return string


    def encoder_pipe(self, pipe):
       string = f""" PIPE
    END-POINT            {pipe.start.x}      {pipe.start.y}       {pipe.start.z}         {pipe.start_diameter}  
    END-POINT            {pipe.end.x}      {pipe.end.y}        {pipe.end.z}            {pipe.end_diameter}   """
       
       return string
    
    def encoder_bend(self, bend):
       string = f""" BEND
    END-POINT        {bend.start.x}   {bend.start.y}    {bend.start.z}       {bend.start_diameter}  
    END-POINT        {bend.end.x}   {bend.end.y}   {bend.end.z}       {bend.end_diameter}   
    CENTRE-POINT     {bend.corner.x}   {bend.corner.y}    {bend.corner.z}   
    SKEY BEBW
    """
       
       return string

    def encoder_flange(self, flange):
       string = f""" FLANGE
    END-POINT    {flange.position.x}   {flange.position.y}       {flange.position.z}       {flange.diameter}   
    END-POINT    {flange.position.x + flange.normal[0]}   {flange.position.y + flange.normal[1]}       {flange.position.z + flange.normal[2]}       {flange.diameter}   
    SKEY FLBL"""
       
       return string
    
    def encoder_elbow(self, bend):
       string = f""" ELBOW
    END-POINT            {bend.start.x}     {bend.start.y}       {bend.start.z}        {bend.start_diameter}   
    END-POINT            {bend.end.x}     {bend.end.y}      {bend.end.z}         {bend.end_diameter}   
    CENTRE-POINT         {bend.corner.x}   {bend.corner.y}    {bend.corner.z}        
    SKEY                 ELBW
    """
       
       return string
    
    
