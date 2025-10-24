import sys
import time
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from mapping import CoordinateMap

app = QApplication(sys.argv)

mapping = CoordinateMap(grid_size=25)
mapping.show()

coords = [(0,0), (2,1), (4,3), (6,5), (8,6), (10,8), (10,13), (12,13), (15,18), (20,20)]
index = 0

def update_point():
    global index
    if index < len(coords):
        x, y = coords[index]
        mapping.mark_point(x, y)
        index += 1
    else:
        index = 0 

timer = QTimer()
timer.timeout.connect(update_point)
timer.start(500)

sys.exit(app.exec())
