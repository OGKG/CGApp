from operator import sub
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsScene

class PointScene(QGraphicsScene):
    def __init__(self, point_model):
        QGraphicsScene.__init__(self)
        self.point_model = point_model
        self.addItems()

    def addItems(self):
        for row in range(self.point_model.rowCount()):
            index = self.point_model.index(row)
            self.addItem(PointGraphicsItem(self.point_model, self, index))


class PointGraphicsItem(QGraphicsEllipseItem):
    rad = 5
    def __init__(self, point_model, scene, index):
        self.point_model=point_model
        self.scene = scene
        self.index = index
        super().__init__(0, 0, 2*self.rad, 2*self.rad)
        shift = tuple(map(sub, self.get_point_data(), (self.rad, self.rad)))
        self.moveBy(*shift)
        self.setBrush(Qt.blue)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        self.point_model.setData(self.index, value, Qt.UserRole, self.rad)
        return super().itemChange(change, value)

    def get_point_data(self):
        return self.point_model.data(self.index, Qt.UserRole)
