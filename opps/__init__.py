import os
import sys
from pathlib import Path

import vtk
from PyQt5.QtWidgets import QApplication

ROOT_DIR = Path(__file__).parent
UI_DIR = ROOT_DIR / "interface/ui_files"
SYMBOLS_DIR = ROOT_DIR / "interface/symbol_files"


def app() -> "Application":
    return QApplication.instance()


def run():
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
