import os
import sys

import vtk
from PyQt5.QtWidgets import QApplication

from opps.interface.main_window import MainWindow

if __name__ == "__main__":
    # disables the terrible vtk error handler and its logs
    # you may want to enable them while debugging something
    vtk.vtkObject.GlobalWarningDisplayOff()
    vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)

    # Make the window scale evenly for every monitor
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
