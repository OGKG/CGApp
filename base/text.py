from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QGraphicsTextItem


class GraphicsTextItem(QGraphicsTextItem):
    def __init__(self, text):
        super().__init__(text)
        self.setRotation(180)
        self.setTransform(QTransform.fromScale(-1, 1))