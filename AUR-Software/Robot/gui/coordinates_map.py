from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from PySide6.QtCore import Qt

class CoordinateMap(QWidget):
    def __init__(self, grid_size=20):
        super().__init__()
        self.setMinimumSize(600, 600)
        self.setWindowTitle("Coordinate Map")
        self.grid_size = grid_size
        self.latest_point = None
        self.max_coord = 400  # Changed from 4 to 400

    def mark_point(self, x, y, color=QColor("red")):
        self.latest_point = (x, y, color)
        self.update()  # trigger redraw

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width = self.width()
        height = self.height()

        step = width / self.max_coord  # adjust so that 400 fills the entire width
        self.grid_size = step

        # draw grid lines (draw fewer lines to avoid clutter)
        pen = QPen(QColor(220, 220, 220))
        painter.setPen(pen)
        
        # Draw grid lines at major intervals (every 100 units)
        for i in range(0, self.max_coord + 1, 100):
            gx = i * step
            gy = i * step
            painter.drawLine(gx, 0, gx, height) # type: ignore
            painter.drawLine(0, gy, width, gy) # type: ignore

        # draw axes
        pen.setColor(Qt.GlobalColor.black)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(0, height, width, height)  # x axis
        painter.drawLine(0, 0, 0, height)           # y axis

        # draw axis labels at major intervals
        painter.setFont(QFont("Arial", 10))
        painter.setPen(Qt.GlobalColor.black)
        for i in range(0, self.max_coord + 1, 100):
            # x labels
            x_label = str(i)
            painter.drawText(i * step + 2, height - 4, x_label) # type: ignore
            # y labels
            y_label = str(i)
            py = height - i * step
            painter.drawText(4, py - 4, y_label)  # type: ignore

        # draw only the latest point
        if self.latest_point:
            x, y, color = self.latest_point
            painter.setPen(QPen(color, 4))
            painter.setBrush(color)
            draw_x = x * step
            draw_y = height - (y * step)
            r = 8
            painter.drawEllipse(draw_x - r, draw_y - r, r * 2, r * 2)
