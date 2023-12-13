import vtk


def paint_data(data: vtk.vtkPolyData, color: tuple):
    n_cells = data.GetNumberOfCells()
    cell_colors = vtk.vtkUnsignedCharArray()
    cell_colors.SetName("colors")
    cell_colors.SetNumberOfComponents(3)
    cell_colors.SetNumberOfTuples(n_cells)
    cell_colors.FillComponent(0, color[0])
    cell_colors.FillComponent(1, color[1])
    cell_colors.FillComponent(2, color[2])
    data.GetCellData().SetScalars(cell_colors)
