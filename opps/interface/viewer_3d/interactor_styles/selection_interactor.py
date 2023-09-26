import vtk

from opps.interface.viewer_3d.interactor_styles.arcball_camera import (
    vtkInteractorStyleArcballCamera,
)
import numpy as np


class SelectionInteractor(vtkInteractorStyleArcballCamera):
    """
    Interactor style that invoke SelectionEvent every time a
    object is clicked.

    The pick information can be extracted directly from
    selection picker.
    """

    def __init__(self):
        super().__init__()
        self.selection_picker = vtk.vtkCellPicker()
        self.hover_picker = vtk.vtkCellPicker()
        self.selection_picker.SetTolerance(0.002)

        self._selectable_points = [(0,0,0), (1,0,0), (0,1,0), (0,0,1)]
        self._pixel_data = vtk.vtkUnsignedCharArray()
        self._current_highlight = None

    def left_button_press_event(self, obj, event):
        cursor = self.GetInteractor().GetEventPosition()
        self.FindPokedRenderer(cursor[0], cursor[1])

        renderer = self.GetCurrentRenderer() or self.GetDefaultRenderer()
        if renderer is None:
            return

        self.selection_picker.Pick(cursor[0], cursor[1], 0, renderer)
        self.InvokeEvent("SelectionEvent")

    def mouse_move_event(self, obj, event):
        super().mouse_move_event(obj, event)
        if self._rotating or self.is_panning:
           return
        self.update_hover()
        self.highlight_closest_point()
        # self.draw_box_around_point(self.GetInteractor().GetEventPosition())
    
    def update_hover(self):
        cursor = self.GetInteractor().GetEventPosition()
        self.FindPokedRenderer(cursor[0], cursor[1])
        renderer = self.GetCurrentRenderer() or self.GetDefaultRenderer()
        if renderer is None:
            self._current_highlight = None
            return
        self.hover_picker.Pick(cursor[0], cursor[1], 0, renderer)

    def highlight_closest_point(self):
        def distance(a, b):
            return np.linalg.norm(np.array(a) - np.array(b))

        mouse_3d = self.hover_picker.GetPickPosition()
        closest_point = (0,0,0)
        for point in self._selectable_points:
            if (distance(mouse_3d, point) < distance(mouse_3d, closest_point)):
                closest_point = point

        if self._current_highlight == closest_point:
            return

        self._current_highlight = closest_point
        coordinate = vtk.vtkCoordinate()
        coordinate.SetValue(*closest_point)
        renderer = self.GetCurrentRenderer() or self.GetDefaultRenderer()
        point_2d = coordinate.GetComputedDisplayValue(renderer)
        self.draw_box_around_point(point_2d)

    def draw_box_around_point(self, position):
        window_size = self.GetInteractor().GetSize()
        renderWindow = self.GetInteractor().GetRenderWindow()
        renderWindow.Render()
        renderWindow.GetRGBACharPixelData(0, 0, window_size[0]-1, window_size[1]-1, 0, self._pixel_data)

        box_size = 15
        for i in range(box_size):
            for j in range(box_size):
                x = position[0] + i
                y = position[1] + j
                pixel = y * window_size[0] + x
                self._pixel_data.SetTuple3(pixel, 255, 0, 0)
        
        renderWindow.SetRGBACharPixelData(0, 0, window_size[0]-1, window_size[1]-1, self._pixel_data, 0)
        renderWindow.Frame()
