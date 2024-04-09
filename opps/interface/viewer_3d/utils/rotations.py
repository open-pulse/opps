import vtk
import numpy as np


def align_y_rotations(vector):
    x, y, z = vector
    rx, ry, rz = 0, 0, 0

    xy_length = np.sqrt(x * x + y * y)
    vector_length = np.sqrt(x * x + y * y + z * z)

    if x < 0:
        xy_length = -xy_length

    if xy_length:
        rz = np.arccos(y / xy_length)

    if vector_length:
        rx = -np.arccos(xy_length / vector_length)

    return rx, ry, rz


def align_vtk_geometry(geometry: vtk.vtkPolyData, start: np.ndarray, vector):
    x, y, z = start
    rx, ry, rz = align_y_rotations(vector)

    transform = vtk.vtkTransform()
    transform.Translate(x, y, z)
    transform.RotateZ(-np.degrees(rz))
    transform.RotateY(-np.degrees(ry))
    transform.RotateX(-np.degrees(rx))
    transform.Update()

    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetInputData(geometry)
    transform_filter.SetTransform(transform)
    transform_filter.Update()

    return transform_filter.GetOutput()
