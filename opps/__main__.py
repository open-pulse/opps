import os
import sys

import vtk

if __name__ == "__main__":
    # disables the terrible vtk error handler and its logs
    # you may want to enable them while debugging something
    vtk.vtkObject.GlobalWarningDisplayOff()
    vtk.vtkLogger.SetStderrVerbosity(vtk.vtkLogger.VERBOSITY_OFF)

    # Make the window scale evenly for every monitor
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    # Start the application
    from opps.interface.application import Application

    _app = Application(sys.argv)
    sys.exit(_app.exec_())
