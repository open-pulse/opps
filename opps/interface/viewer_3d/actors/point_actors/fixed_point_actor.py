import vtk


class FixedPointActor(vtk.vtkActor):
    def __init__(self):
        super().__init__()
        self.create_geometry()

    def create_geometry(self):
        base = vtk.vtkCubeSource()
        cylinder = vtk.vtkCylinderSource()

        base.SetXLength(1)
        base.SetYLength(0.1)
        base.SetZLength(1)

        cylinder.SetHeight(1)
        cylinder.SetRadius(0.1)
        cylinder.SetCenter(0, 0.5, 0)

        base.Update()
        cylinder.Update()

        append_filter = vtk.vtkAppendPolyData()
        append_filter.AddInputData(base.GetOutput())
        append_filter.AddInputData(cylinder.GetOutput())
        append_filter.Update()

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(append_filter.GetOutput())
        self.SetMapper(mapper)
