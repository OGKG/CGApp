from PyQt5.QtCore import QLineF, QPointF
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsTextItem
from base.point import PointGraphicsItem, PointScene
from module.algo.loci import Loci


class LociGraphicsItem(PointGraphicsItem):
    def append_children(self):
        self.hline = QGraphicsLineItem(QLineF(QPointF(0, 0), QPointF(1000, 0)), parent=self)
        self.vline = QGraphicsLineItem(QLineF(QPointF(0, 0), QPointF(0, 1000)), parent=self)

    def setText(self, text):
        self.text.setPlainText(text)


class LociPointScene(PointScene):
    graphicsItemClass = LociGraphicsItem

    def __init__(self, point_model):
        super().__init__(point_model)
        self.textFields = []

    def refresh(self):
        self.clearTextFields()
        self.loci = Loci()
        self.loci.append_points(*self.point_model.points)
        for key, value in self.loci.repr.items():
            text = QGraphicsTextItem(str(value))
            text.moveBy(*key.coords)
            self.textFields.append(text)
            self.addItem(text)

    def clearTextFields(self):
        for textField in self.textFields:
            self.removeItem(textField)

