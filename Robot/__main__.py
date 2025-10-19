import sys

if __package__ is None and not getattr(sys, 'frozen', False):
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

from PySide6.QtWidgets import QApplication
from Robot.gui.window import Window

app = QApplication()

window = Window()
app.exec()