from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPolygonF
from PyQt5.QtWidgets import QGraphicsPolygonItem

class PolygonGraphicsItem(QGraphicsPolygonItem):
    def __init__(self, points, parent=None):
        QGraphicsPolygonItem.__init__(self, QPolygonF(points), parent)
        self.setPen(Qt.red)
