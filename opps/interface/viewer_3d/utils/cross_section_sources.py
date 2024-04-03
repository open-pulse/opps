import vtk
import numpy as np


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
    inner_radius = outer_radius - thickness

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
    # ring_bottom.SetCenter(0, -length / 2, 0)
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
    return pipe_data(length, outside_diameter, thickness)


def closed_rectangular_beam_data(length, b, h):
    rectangular = vtk.vtkCubeSource()
    rectangular.SetYLength(length)
    rectangular.SetXLength(b)
    rectangular.SetZLength(h)
    rectangular.Update()
    return rectangular.GetOutput()


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
    rectangular_top.SetCenter(0, 0, -h / 2 + t / 2)

    rectangular_left.SetYLength(length)
    rectangular_left.SetZLength(h)
    rectangular_left.SetXLength(t)
    rectangular_left.SetCenter(-b / 2 + t / 2, 0, 0)

    rectangular_right.SetYLength(length)
    rectangular_right.SetZLength(h)
    rectangular_right.SetXLength(t)
    rectangular_right.SetCenter(b / 2 - t / 2, 0, 0)

    rectangular_bottom.SetYLength(length)
    rectangular_bottom.SetZLength(t)
    rectangular_bottom.SetXLength(b)
    rectangular_bottom.SetCenter(0, 0, h / 2 - t / 2)

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
    rectangular_top.SetCenter(w1 / 2 - max(w1, w2) / 2, 0, -h / 2 + t1 / 2)

    rectangular_left.SetYLength(length)
    rectangular_left.SetZLength(h)
    rectangular_left.SetXLength(tw)
    rectangular_left.SetCenter(-max(w1, w2) / 2 + tw / 2, 0, 0)

    rectangular_bottom.SetYLength(length)
    rectangular_bottom.SetZLength(t2)
    rectangular_bottom.SetXLength(w2)
    rectangular_bottom.SetCenter(w2 / 2 - max(w1, w2) / 2, 0, h / 2 - t2 / 2)

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
    rectangular_top.SetCenter(0, 0, -h / 2 + t1 / 2)

    rectangular_center.SetYLength(length)
    rectangular_center.SetZLength(h)
    rectangular_center.SetXLength(tw)

    rectangular_bottom.SetYLength(length)
    rectangular_bottom.SetZLength(t2)
    rectangular_bottom.SetXLength(w2)
    rectangular_bottom.SetCenter(0, 0, h / 2 - t2 / 2)

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
    rectangular_top.SetCenter(0, 0, -h / 2 + t1 / 2)

    rectangular_center.SetYLength(length)
    rectangular_center.SetZLength(h)
    rectangular_center.SetXLength(tw)

    rectangular_top.Update()
    rectangular_center.Update()

    append_polydata = vtk.vtkAppendPolyData()
    append_polydata.AddInputData(rectangular_top.GetOutput())
    append_polydata.AddInputData(rectangular_center.GetOutput())
    append_polydata.Update()

    return append_polydata.GetOutput()


def eccentric_reducer_data(length, start_diameter, end_diameter, offset_y, offset_z):
    radius_array = vtk.vtkDoubleArray()
    radius_array.SetName("TubeRadius")
    radius_array.SetNumberOfTuples(2)
    radius_array.SetTuple1(0, start_diameter / 2)
    radius_array.SetTuple1(1, end_diameter / 2)

    line_source = vtk.vtkLineSource()
    line_source.SetPoint1(0, -length / 2, 0)
    line_source.SetPoint2((offset_y, length / 2, offset_z))
    line_source.Update()

    polydata = line_source.GetOutput()
    polydata.GetPointData().AddArray(radius_array)
    polydata.GetPointData().SetActiveScalars(radius_array.GetName())

    tube_filter = vtk.vtkTubeFilter()
    tube_filter.SetInputData(polydata)
    tube_filter.SetNumberOfSides(30)
    tube_filter.SetVaryRadiusToVaryRadiusByAbsoluteScalar()
    tube_filter.Update()

    return tube_filter.GetOutput()


def flange_data(length, inside_diameter, thickness, bolts=8):
    pipe = pipe_data(length, inside_diameter + thickness * 2, thickness)
    append_polydata = vtk.vtkAppendPolyData()
    append_polydata.AddInputData(pipe)

    for i in range(bolts):
        angle = i * 2 * np.pi / bolts
        nut = vtk.vtkCylinderSource()
        nut.SetHeight(thickness * 3 / 2)
        nut.SetRadius(thickness / 3)
        nut.SetCenter(
            (inside_diameter / 2 + thickness / 2) * np.sin(angle),
            thickness / 2,
            (inside_diameter / 2 + thickness / 2) * np.cos(angle),
        )
        nut.Update()
        append_polydata.AddInputData(nut.GetOutput())

    append_polydata.Update()
    return append_polydata.GetOutput()

def expansion_joint_data(length, outside_diameter, thickness):
    append_polydata = vtk.vtkAppendPolyData()

    width = 0.15 * outside_diameter
    pipe = pipe_data(length, outside_diameter, thickness)
    start_flange = flange_data(width, outside_diameter, width)

    # I just wanted to move the flange to the end of the structure
    # but that is the only way vtk let me do it.
    transform = vtk.vtkTransform()
    transform.Translate(0, length - width, 0)
    transform.Update()
    transform_filter = vtk.vtkTransformFilter()
    transform_filter.SetInputData(flange_data(width, outside_diameter, width))
    transform_filter.SetTransform(transform)
    transform_filter.Update()
    end_flange = transform_filter.GetOutput()

    append_polydata.AddInputData(pipe)
    append_polydata.AddInputData(start_flange)
    append_polydata.AddInputData(end_flange)

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
    
    initial_left_nut = vtk.vtkCubeSource()
    initial_left_nut.SetCenter(-(3 * width + outside_diameter) / 2, width / 2, 0)
    initial_left_nut.SetXLength(2 * width)
    initial_left_nut.SetYLength(width)
    initial_left_nut.SetZLength(2 * width)
    initial_left_nut.Update()
    append_polydata.AddInputData(initial_left_nut.GetOutput())

    initial_right_nut = vtk.vtkCubeSource()
    initial_right_nut.SetCenter((3 * width + outside_diameter) / 2, width / 2, 0)
    initial_right_nut.SetXLength(2 * width)
    initial_right_nut.SetYLength(width)
    initial_right_nut.SetZLength(2 * width)
    initial_right_nut.Update()
    append_polydata.AddInputData(initial_right_nut.GetOutput())

    final_left_nut = vtk.vtkCubeSource()
    final_left_nut.SetCenter(-(3 * width + outside_diameter) / 2, length - width / 2, 0)
    final_left_nut.SetXLength(2 * width)
    final_left_nut.SetYLength(width)
    final_left_nut.SetZLength(2 * width)
    final_left_nut.Update()
    append_polydata.AddInputData(final_left_nut.GetOutput())

    final_right_nut = vtk.vtkCubeSource()
    final_right_nut.SetCenter((3 * width + outside_diameter) / 2, length - width / 2, 0)
    final_right_nut.SetXLength(2 * width)
    final_right_nut.SetYLength(width)
    final_right_nut.SetZLength(2 * width)
    final_right_nut.Update()
    append_polydata.AddInputData(final_right_nut.GetOutput())

    left_screw = vtk.vtkCylinderSource()
    left_screw.SetHeight(length)
    left_screw.SetRadius(width / 2)
    left_screw.SetCenter(-(3 * width + outside_diameter) / 2, length / 2, 0)
    left_screw.Update()
    append_polydata.AddInputData(left_screw.GetOutput())

    right_screw = vtk.vtkCylinderSource()
    right_screw.SetHeight(length)
    right_screw.SetRadius(width / 2)
    right_screw.SetCenter((3 * width + outside_diameter) / 2, length / 2, 0)
    right_screw.Update()
    append_polydata.AddInputData(right_screw.GetOutput())

    append_polydata.Update()
    return append_polydata.GetOutput()