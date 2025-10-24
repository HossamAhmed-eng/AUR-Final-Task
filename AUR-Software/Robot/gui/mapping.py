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

    def mark_point(self, x, y, color=QColor("red")):
        self.latest_point = (x, y, color)
        self.update()  # trigger redraw

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width = self.width()
        height = self.height()

        max_coord = 4  # only 0 to 4
        step = width / max_coord  # adjust so that 4 fills the entire width
        self.grid_size = step

        # draw grid lines
        pen = QPen(QColor(220, 220, 220))
        painter.setPen(pen)
        for i in range(max_coord + 1):
            gx = i * step
            gy = i * step
            painter.drawLine(gx, 0, gx, height)
            painter.drawLine(0, gy, width, gy)

        #draw axes
        pen.setColor(Qt.GlobalColor.black)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(0, height, width, height)  # x axis
        painter.drawLine(0, 0, 0, height)           # y axis

        # draw axis labels
        painter.setFont(QFont("Arial", 10))
        painter.setPen(Qt.GlobalColor.black)
        for i in range(max_coord + 1):
            # x labels
            x_label = str(i)
            painter.drawText(i * step + 2, height - 4, x_label)
            # y labels
            y_label = str(i)
            py = height - i * step
            painter.drawText(4, py - 4, y_label)

        # draw only the latest point
        if self.latest_point:
            x, y, color = self.latest_point
            painter.setPen(QPen(color, 4))
            painter.setBrush(color)
            draw_x = x * step
            draw_y = height - (y * step)
            r = 8
            painter.drawEllipse(draw_x - r, draw_y - r, r * 2, r * 2)


