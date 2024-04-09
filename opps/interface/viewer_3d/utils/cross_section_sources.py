import numpy as np
import vtk
from itertools import chain

from opps import SYMBOLS_DIR


def load_symbol(path):
    reader = vtk.vtkOBJReader()
    reader.SetFileName(str(path))
    reader.Update()
    return reader.GetOutput()


VALVE_WHEEL = load_symbol(SYMBOLS_DIR / "valve_wheel.obj")


def closed_pipe_data(length, outside_diameter):
    cilinder = vtk.vtkCylinderSource()
    cilinder.SetResolution(20)
    cilinder.SetRadius(outside_diameter / 2)
    cilinder.SetCenter(0, length / 2, 0)
    cilinder.SetHeight(length)
    cilinder.CappingOn()
    cilinder.Update()
    return cilinder.GetOutput()


def pipe_data(length, outside_diameter, thickness):
    if (thickness == 0) or (2 * thickness > outside_diameter):
        return closed_pipe_data(length, outside_diameter)

    outer_radius = outside_diameter / 2
    inner_radius = (outside_diameter - thickness) / 2

    outer_cilinder = vtk.vtkCylinderSource()
    outer_cilinder.SetResolution(20)
    outer_cilinder.SetRadius(outer_radius)
    outer_cilinder.SetHeight(length)
    outer_cilinder.SetCenter(0, length / 2, 0)
    outer_cilinder.CappingOff()
    outer_cilinder.Update()

    inner_cilinder = vtk.vtkCylinderSource()
    inner_cilinder.SetResolution(20)
    inner_cilinder.SetRadius(inner_radius)
    inner_cilinder.SetHeight(length)
    inner_cilinder.SetCenter(0, length / 2, 0)
    inner_cilinder.CappingOff()
    inner_cilinder.Update()

    ring_bottom = vtk.vtkDiskSource()
    ring_bottom.SetCircumferentialResolution(20)
    ring_bottom.SetOuterRadius(outer_radius)
    ring_bottom.SetInnerRadius(inner_radius)
    ring_bottom.SetNormal(0, 1, 0)
    ring_bottom.Update()

    ring_top = vtk.vtkDiskSource()
    ring_top.SetCircumferentialResolution(20)
    ring_top.SetOuterRadius(outer_radius)
    ring_top.SetInnerRadius(inner_radius)
    ring_top.SetCenter(0, length, 0)
    ring_top.SetNormal(0, 1, 0)
    ring_top.Update()

    append_polydata = vtk.vtkAppendPolyData()
    append_polydata.AddInputData(outer_cilinder.GetOutput())
    append_polydata.AddInputData(inner_cilinder.GetOutput())
    append_polydata.AddInputData(ring_bottom.GetOutput())
    append_polydata.AddInputData(ring_top.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()


def circular_beam_data(length, outside_diameter, thickness):
    cilinder = vtk.vtkCylinderSource()
    cilinder.SetResolution(12)
    cilinder.SetRadius(outside_diameter / 2)
    cilinder.SetHeight(length)
    cilinder.SetCenter(0, length / 2, 0)
    cilinder.CappingOn()
    cilinder.Update()
    return cilinder.GetOutput()


def closed_rectangular_beam_data(length, b, h):
    rectangle = vtk.vtkCubeSource()
    rectangle.SetYLength(length)
    rectangle.SetXLength(b)
    rectangle.SetZLength(h)
    rectangle.SetCenter(0, length / 2, 0)
    rectangle.Update()
    return rectangle.GetOutput()


def rectangular_beam_data(length, b, h, t):
    if t == 0:
        return closed_rectangular_beam_data(length, b, h)

    rectangular_top = vtk.vtkCubeSource()
    rectangular_left = vtk.vtkCubeSource()
    rectangular_right = vtk.vtkCubeSource()
    rectangular_bottom = vtk.vtkCubeSource()

    rectangular_top.SetYLength(length)
    rectangular_top.SetZLength(t)
    rectangular_top.SetXLength(b)
    rectangular_top.SetCenter(0, length / 2, -h / 2 + t / 2)

    rectangular_left.SetYLength(length)
    rectangular_left.SetZLength(h)
    rectangular_left.SetXLength(t)
    rectangular_left.SetCenter(-b / 2 + t / 2, length / 2, 0)

    rectangular_right.SetYLength(length)
    rectangular_right.SetZLength(h)
    rectangular_right.SetXLength(t)
    rectangular_right.SetCenter(b / 2 - t / 2, length / 2, 0)

    rectangular_bottom.SetYLength(length)
    rectangular_bottom.SetZLength(t)
    rectangular_bottom.SetXLength(b)
    rectangular_bottom.SetCenter(0, length / 2, h / 2 - t / 2)

    rectangular_top.Update()
    rectangular_left.Update()
    rectangular_right.Update()
    rectangular_bottom.Update()

    append_polydata = vtk.vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_left.GetOutput())
    append_polydata.AddInputData(rectangular_right.GetOutput())
    append_polydata.AddInputData(rectangular_bottom.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()


def c_beam_data(length, h, w1, w2, t1, t2, tw):
    rectangular_top = vtk.vtkCubeSource()
    rectangular_left = vtk.vtkCubeSource()
    rectangular_bottom = vtk.vtkCubeSource()

    rectangular_top.SetYLength(length)
    rectangular_top.SetZLength(t1)
    rectangular_top.SetXLength(w1)
    rectangular_top.SetCenter(
        w1 / 2 - max(w1, w2) / 2,
        length / 2,
        -h / 2 + t1 / 2
    )

    rectangular_left.SetYLength(length)
    rectangular_left.SetZLength(h)
    rectangular_left.SetXLength(tw)
    rectangular_left.SetCenter(
        -max(w1, w2) / 2 + tw / 2,
        length / 2,
        0
    )

    rectangular_bottom.SetYLength(length)
    rectangular_bottom.SetZLength(t2)
    rectangular_bottom.SetXLength(w2)
    rectangular_bottom.SetCenter(
        w2 / 2 - max(w1, w2) / 2,
        length / 2,
        h / 2 - t2 / 2
    )

    rectangular_top.Update()
    rectangular_left.Update()
    rectangular_bottom.Update()

    append_polydata = vtk.vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_left.GetOutput())
    append_polydata.AddInputData(rectangular_bottom.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()


def i_beam_data(length, h, w1, w2, t1, t2, tw):
    rectangular_top = vtk.vtkCubeSource()
    rectangular_center = vtk.vtkCubeSource()
    rectangular_bottom = vtk.vtkCubeSource()

    rectangular_top.SetYLength(length)
    rectangular_top.SetZLength(t1)
    rectangular_top.SetXLength(w1)
    rectangular_top.SetCenter(0, length / 2, -h / 2 + t1 / 2)

    rectangular_center.SetYLength(length)
    rectangular_center.SetZLength(h)
    rectangular_center.SetCenter(0, length / 2, 0)
    rectangular_center.SetXLength(tw)

    rectangular_bottom.SetYLength(length)
    rectangular_bottom.SetZLength(t2)
    rectangular_bottom.SetXLength(w2)
    rectangular_bottom.SetCenter(0, length / 2, h / 2 - t2 / 2)

    rectangular_top.Update()
    rectangular_center.Update()
    rectangular_bottom.Update()

    append_polydata = vtk.vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_center.GetOutput())
    append_polydata.AddInputData(rectangular_bottom.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()


def t_beam_data(length, h, w1, t1, tw):
    rectangular_top = vtk.vtkCubeSource()
    rectangular_center = vtk.vtkCubeSource()

    rectangular_top.SetYLength(length)
    rectangular_top.SetZLength(t1)
    rectangular_top.SetXLength(w1)
    rectangular_top.SetCenter(0, length / 2, -h / 2 + t1 / 2)

    rectangular_center.SetYLength(length)
    rectangular_center.SetZLength(h)
    rectangular_center.SetCenter(0, length / 2, 0)
    rectangular_center.SetXLength(tw)

    rectangular_top.Update()
    rectangular_center.Update()

    append_polydata = vtk.vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_center.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()


def eccentric_reducer_data(length, start_diameter, end_diameter, offset_y, offset_z):
    initial_radius = start_diameter / 2
    final_radius = end_diameter / 2

    sides = 20

    initial_ring = vtk.vtkRegularPolygonSource()
    initial_ring.SetRadius(initial_radius)
    initial_ring.SetNumberOfSides(sides)
    initial_ring.SetNormal(0, 1, 0)
    initial_ring.Update()

    final_ring = vtk.vtkRegularPolygonSource()
    final_ring.SetRadius(final_radius)
    final_ring.SetNumberOfSides(sides)
    final_ring.SetCenter(offset_y, length, offset_z)
    final_ring.SetNormal(0, 1, 0)
    final_ring.Update()

    initial_points = initial_ring.GetOutput().GetPoints()
    final_points = final_ring.GetOutput().GetPoints()

    points = vtk.vtkPoints()
    points.InsertPoints(
        0, 
        sides,
        0,
        initial_points
    )
    points.InsertPoints(
        sides,
        sides,
        0,
        final_points
    )

    points_order = []
    for i in range(sides):
        points_order.append(i)
        points_order.append(i + sides)
    points_order.append(0)

    external_face = vtk.vtkPolyData()
    external_face.Allocate()
    external_face.SetPoints(points)
    external_face.InsertNextCell(vtk.VTK_TRIANGLE_STRIP, len(points_order), points_order)

    append_polydata = vtk.vtkAppendPolyData()
    append_polydata.AddInputData(initial_ring.GetOutput())
    append_polydata.AddInputData(final_ring.GetOutput())
    append_polydata.AddInputData(external_face)
    append_polydata.Update()

    return append_polydata.GetOutput()

def flange_data(length, outside_diameter, thickness, bolts=8):
    pipe = pipe_data(length, outside_diameter, thickness)
    append_polydata = vtk.vtkAppendPolyData()
    append_polydata.AddInputData(pipe)

    for i in range(bolts):
        angle = i * 2 * np.pi / bolts
        nut = vtk.vtkCylinderSource()
        nut.SetHeight(length + thickness / 2)
        nut.SetRadius(thickness / 4 / 2)
        nut.SetCenter(
            (outside_diameter - thickness / 3) * np.sin(angle) / 2,
            length / 2,
            (outside_diameter - thickness / 3) * np.cos(angle) / 2,
        )
        nut.Update()
        append_polydata.AddInputData(nut.GetOutput())

    append_polydata.Update()
    return append_polydata.GetOutput()


def expansion_joint_data(length, outside_diameter, thickness):
    append_polydata = vtk.vtkAppendPolyData()

    width = 0.15 * outside_diameter
    pipe = pipe_data(length, outside_diameter, thickness)
    start_flange = flange_data(width, outside_diameter + width, width)

    # I just wanted to move the flange to the end of the structure
    # but that is the only way vtk let me do it.
    transform = vtk.vtkTransform()
    transform.Translate(0, length - width, 0)
    transform.Update()
    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetInputData(flange_data(width, outside_diameter + width, width))
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    end_flange = transform_filter.GetOutput()

    append_polydata.AddInputData(pipe)
    append_polydata.AddInputData(start_flange)
    append_polydata.AddInputData(end_flange)

    # Draw rings in the middle portion of the pipe
    rings = int(3 * length / width / 5)
    for i in range(0, rings, 2):
        position = i / (rings - 1) * (3 * length / 5) + length / 5
        ring = vtk.vtkCylinderSource()
        ring.SetHeight(width)
        ring.SetRadius(width + outside_diameter / 2)
        ring.SetCenter(0, position + width / 2, 0)
        ring.SetResolution(15)
        ring.Update()
        append_polydata.AddInputData(ring.GetOutput())

    tie_rods = 2
    for i in range(tie_rods):
        angle = i * 2 * np.pi / tie_rods
        x = (3 * width + outside_diameter) / 2 * np.sin(angle)
        z = (3 * width + outside_diameter) / 2 * np.cos(angle)

        tie_rod = vtk.vtkCylinderSource()
        tie_rod.SetHeight(length)
        tie_rod.SetRadius(width / 2)
        tie_rod.SetCenter(x, length / 2, z)
        tie_rod.Update()
        append_polydata.AddInputData(tie_rod.GetOutput())

        initial_nut = vtk.vtkCubeSource()
        initial_nut.SetCenter(x, width / 2, z)
        initial_nut.SetXLength(2 * width)
        initial_nut.SetYLength(width)
        initial_nut.SetZLength(2 * width)
        initial_nut.Update()
        append_polydata.AddInputData(initial_nut.GetOutput())

        final_nut = vtk.vtkCubeSource()
        final_nut.SetCenter(x, length - width / 2, z)
        final_nut.SetXLength(2 * width)
        final_nut.SetYLength(width)
        final_nut.SetZLength(2 * width)
        final_nut.Update()
        append_polydata.AddInputData(final_nut.GetOutput())

    append_polydata.Update()
    return append_polydata.GetOutput()


def valve_data(length, outside_diameter, thickness):
    append_polydata = vtk.vtkAppendPolyData()

    if length == 0:
        # empty poly data
        return vtk.vtkPolyData()

    width = 0.20 * outside_diameter
    pipe = pipe_data(length, outside_diameter, thickness)
    start_flange = flange_data(width, outside_diameter + width, width)

    # I just wanted to move the flange to the end of the structure
    # but that is the only way vtk let me do it.
    transform = vtk.vtkTransform()
    transform.Translate(0, length - width, 0)
    transform.Update()
    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetInputData(flange_data(width, outside_diameter + width, width))
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    end_flange = transform_filter.GetOutput()

    center_sphere = vtk.vtkSphereSource()
    center_sphere.SetPhiResolution(20)
    center_sphere.SetThetaResolution(20)
    center_sphere.SetRadius(outside_diameter)
    center_sphere.SetCenter(0, length / 2, 0)
    center_sphere.Update()

    transform = vtk.vtkTransform()
    transform.Translate(0, length / 2, 0)
    transform.RotateZ(90)
    transform.Translate(0, outside_diameter / 3, 0)
    transform.Update()
    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetInputData(valve_handle(outside_diameter, length / 4, width))
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    handle = transform_filter.GetOutput()

    append_polydata.AddInputData(pipe)
    append_polydata.AddInputData(start_flange)
    append_polydata.AddInputData(end_flange)
    append_polydata.AddInputData(center_sphere.GetOutput())
    append_polydata.AddInputData(handle)

    append_polydata.Update()
    return append_polydata.GetOutput()


def valve_handle(outside_diameter, height, axis_diameter):
    append_polydata = vtk.vtkAppendPolyData()
    width = 0.20 * outside_diameter

    # I just wanted to move the flange to the end of the structure
    # but that is the only way vtk let me do it.
    transform = vtk.vtkTransform()
    transform.Translate(0, (height - axis_diameter), 0)
    transform.Update()
    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetInputData(flange_data(axis_diameter, outside_diameter + width, axis_diameter))
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    end_flange = transform_filter.GetOutput()

    pipe = pipe_data(height, outside_diameter, 0)

    wheel_diameter = outside_diameter * 1.5
    transform = vtk.vtkTransform()
    transform.Translate(0, height, 0)
    transform.Scale(wheel_diameter, wheel_diameter, wheel_diameter)
    transform.Update()
    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetInputData(VALVE_WHEEL)
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    wheel = transform_filter.GetOutput()

    append_polydata.AddInputData(end_flange)
    append_polydata.AddInputData(pipe)
    append_polydata.AddInputData(wheel)
    append_polydata.Update()
    return append_polydata.GetOutput()
