import numpy as np


def align_y_rotations(vector):
    x, y, z = vector
    rx, ry, rz = 0, 0, 0

    xy_length = np.sqrt(x * x + y * y)
    vector_length = np.sqrt(x * x + y * y + z * z)

    if xy_length:
        rz = np.arccos(y / xy_length)

    if vector_length:
        rx = -np.arccos(xy_length / vector_length)

    return rx, ry, rz
