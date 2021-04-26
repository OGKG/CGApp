from PyQt5.QtCore import QLineF, QPointF
from PyQt5.QtWidgets import QGraphicsLineItem
from base.point import PointGraphicsItem, PointScene
from module.algo.loci import Loci


class LociGraphicsItem(PointGraphicsItem):
    def append_children(self):
        print('asd')
        qp = QPointF(0, 0)
        qp2 = QPointF(100, 0)
        line = QLineF(qp, qp2)
        line = QGraphicsLineItem(line, parent=self)

class LociPointScene(PointScene):
    graphicsItemClass = LociGraphicsItem
    def __init__(self, point_model):
        super(LociPointScene, self).__init__(point_model)
        self.lines = []

    def refresh(self):
        self.loci = Loci()
        self.loci.append_points(*self.point_model.points)
        # self.linesFromLoci(self.loci)

    def linesFromLoci(self, loci):
        ret = []
        # for point in self.point_model.points:
        #     qp = QPointF(*point.coords)
        #     qp2 = QPointF(point.x+100, point.y)
        #     line = QLineF(qp, qp2)
        #     ret.append(QGraphicsLineItem(line))

        # for line in ret:
        #     self.addItem(line)
