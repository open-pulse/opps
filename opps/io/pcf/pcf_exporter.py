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
        string = ""
        for structure in pipeline.structures:
            if isinstance(structure, Pipe):
                stringer = self.encoder_pipe(structure)
                string = string + "\n" + stringer
            
            elif isinstance(structure, Bend):
                stringer = self.encoder_bend(structure)
                string = string + "\n" + stringer

            elif isinstance(structure, Flange):
                stringer = self.encoder_flange(structure)
                string = string + "\n" + stringer

            elif isinstance(structure, Elbow):
                stringer = self.encoder_elbow(structure)
                string = string + "\n" + stringer
                
        return string

    def encoder_pipe(self, pipe):
       string = f""" PIPE
    END-POINT            {pipe.start.x}      {pipe.start.y}       {pipe.start.z}         300.00  
    END-POINT            {pipe.end.x}      {pipe.end.y}        {pipe.end.z}            300.00   """
       
       return string
    
    def encoder_bend(self, bend):
       string = f""" BEND
    END-POINT        {bend.start.x}   {bend.start.y}    {bend.start.z}       203.2000   
    END-POINT        {bend.end.x}   {bend.end.y}   {bend.end.z}       203.2000   
    CENTRE-POINT     {bend.corner.x}   {bend.corner.y}    {bend.corner.z}   
    SKEY BEBW
    ANGLE            9000
    BEND-RADIUS         304.8000"""
       
       return string

    def encoder_flange(self, flange):
       string = f""" FLANGE
    END-POINT    {flange.position.x}   {flange.position.y}       0.1990       203.2000   
    END-POINT    {flange.position.x}   {flange.position.y}       0.1990       203.2000   
    SKEY FLBL"""
       
       return string
    
    def encoder_elbow(self, bend):
       string = f""" ELBOW
    END-POINT            {bend.start.x}     {bend.start.y}       {bend.start.z}        300.00  
    END-POINT            {bend.end.x}     {bend.end.y}      {bend.end.z}         300.00  
    CENTRE-POINT         {bend.corner.x}   {bend.corner.y}    {bend.corner.z}        
    SKEY                 ELBW
    """
       
       return string
    
    
