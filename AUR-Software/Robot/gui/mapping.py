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
        self.update()  #trigger redraw

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width = self.width()
        height = self.height()

        #draw grid lines
        pen = QPen(QColor(220, 220, 220))
        painter.setPen(pen)
        for gx in range(0, width, self.grid_size):
            painter.drawLine(gx, 0, gx, height)
        for gy in range(0, height, self.grid_size):
            painter.drawLine(0, gy, width, gy)

        #draw axes
        pen.setColor(Qt.GlobalColor.black)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawLine(0, 0, width, 0)
        painter.drawLine(0, 0, 0, height)

        #draw axis labels
        painter.setFont(QFont("Arial", 10))
        painter.setPen(Qt.GlobalColor.black)
        label_interval = 5
        label_step = label_interval * self.grid_size

        for px in range(label_step, width, label_step):
            label_val = px // self.grid_size
            painter.drawText(px + 2, height - 4, str(label_val))

        for i in range(label_step, height + 1, label_step):
            label_val = i // self.grid_size
            py = height - i
            painter.drawText(4, py + 4, str(label_val))

        #draw only the latest point
        if self.latest_point:
            x, y, color = self.latest_point
            painter.setPen(QPen(color, 4))
            painter.setBrush(color)
            draw_x = x * self.grid_size
            draw_y = height - (y * self.grid_size)
            r = 8
            painter.drawEllipse(draw_x - r, draw_y - r, r * 2, r * 2)

