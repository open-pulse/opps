import numpy as np
import vtk


def align_y_rotations(vector):
    "https://www.fundza.com/mel/axis_to_vector/index.html"

    x, y, z = vector
    rx, ry, rz = 0, 0, 0

    xy_length = np.sqrt(x * x + y * y)
    vector_length = np.sqrt(x * x + y * y + z * z)

    if vector_length == 0:
        return 0, 0, 0

    if xy_length:
        rz = np.arccos(y / xy_length)
        ry = np.pi
    else:
        rz = np.pi / 2

    rx = np.arccos(xy_length / vector_length)
    if z < 0:
        rx = -rx

    if x > 0:
        rz = -rz

    return rx, ry, rz


def align_vtk_geometry(geometry: vtk.vtkPolyData, start: np.ndarray, vector: np.ndarray):
    x, y, z = start
    rx, ry, rz = align_y_rotations(vector)

    transform = vtk.vtkTransform()
    transform.Translate(x, y, z)
    transform.RotateZ(np.degrees(rz))
    transform.RotateX(np.degrees(rx))
    transform.RotateY(np.degrees(ry))
    transform.Update()

    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetInputData(geometry)
    transform_filter.SetTransform(transform)
    transform_filter.Update()

    return transform_filter.GetOutput()
