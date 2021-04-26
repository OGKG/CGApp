from PyQt5.QtCore import QLineF, QPointF
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsTextItem
from base.point import PointGraphicsItem, PointScene
from module.algo.loci import Loci


class LociGraphicsItem(PointGraphicsItem):
    def append_children(self):
        self.hline = QGraphicsLineItem(QLineF(QPointF(0, 0), QPointF(1000, 0)), parent=self)
        self.vline = QGraphicsLineItem(QLineF(QPointF(0, 0), QPointF(0, 1000)), parent=self)
        self.text = QGraphicsTextItem(parent=self)

    def setText(self, text):
        self.text.setPlainText(text)

    def refresh(self, loci):
        self.setText(str(loci.query(self.point)))


class LociPointScene(PointScene):
    graphicsItemClass = LociGraphicsItem

    def refresh(self):
        self.loci = Loci()
        self.loci.append_points(*self.point_model.points)
        for point in self.items():
            if isinstance(point, LociGraphicsItem):
                point.refresh(self.loci)


