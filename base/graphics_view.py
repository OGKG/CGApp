from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView


class GraphicsView(QGraphicsView):
    def __init__(self, stageLabel, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scale(1, -1)
        self.stageLabel = stageLabel

    def wheelEvent(self, event):
        factor = 0.8
        if event.angleDelta().y() > 0:
            self.scale(1/factor, 1/factor)
        else:
            self.scale(factor, factor)