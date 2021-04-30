from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QGraphicsView


class GraphicsView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super(GraphicsView, self).__init__(parent)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setScene(scene)

    def wheelEvent(self, event):
        factor = 0.8
        if event.angleDelta().y() > 0:
            self.scale(1/factor, 1/factor)
        else:
            self.scale(factor, factor)