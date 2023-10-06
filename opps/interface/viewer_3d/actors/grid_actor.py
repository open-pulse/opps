import numpy as np
import vtk
from pathlib import Path


vertex_shader_path = Path("opps/interface/viewer_3d/shaders/grid_vertex_shader.glsl")
fragment_shader_path = Path("opps/interface/viewer_3d/shaders/grid_fragment_shader.glsl")


class GridActor(vtk.vtkActor):
    def __init__(self):
        sp = self.GetShaderProperty()

        with open(vertex_shader_path) as file:
            vertex_shader_code = file.read()

        with open(fragment_shader_path) as file:
            fragment_shader_code = file.read()

        sp.SetVertexShaderCode(vertex_shader_code)
        sp.SetFragmentShaderCode(fragment_shader_code)


        data = vtk.vtkPolyData()
        points = vtk.vtkPoints()

        points.InsertPoint(0, -0.5, -0.5, 0)
        points.InsertPoint(1,  0.5, -0.5, 0)
        points.InsertPoint(2,  0.5,  0.5, 0)
        points.InsertPoint(3, -0.5,  0.5, 0)

        # data.InsertNextCell(vtk.VTK_TRIANGLE, 3, [0, 1, 2])
        data.SetPoints(points)
        data.Allocate(1)
        data.InsertNextCell(vtk.VTK_QUAD, 4, [0, 1, 2, 3])

        plane = vtk.vtkPlaneSource()
        plane.SetResolution(4, 4)
        plane.SetNormal(0, 0, 1)
        plane.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(plane.GetOutput())
        # mapper.SetInputData(data)

        self.SetMapper(mapper)
        self.UseBoundsOff()
        # self.RotateX(-30)
        # self.RotateY(-30)
        self.ForceTranslucentOn()
        # self.GetProperty().SetOpacity(0)
    
    # def GetBounds(self):
    #     return (100, -100, 100, -100, 100, -100)