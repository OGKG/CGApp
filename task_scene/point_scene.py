from operator import sub
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPolygonF
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsScene
from polygon import PolygonGraphicsItem, PolygonModel
from module.models.point import Point
from module.algo.jarvis import jarvis

class PointScene(QGraphicsScene):
    def __init__(self, point_model):
        QGraphicsScene.__init__(self)
        self.point_model = point_model
        self.polygon_model = PolygonModel(points=[])
        self.polygon = PolygonGraphicsItem([])
        self.polygon.setZValue(-1)
        self.addItems()
        self.addItem(self.polygon)

    def mouseDoubleClickEvent(self, event):
        """Add a new point on mouse double-click"""
        x, y = event.scenePos().x(), event.scenePos().y()
        self.point_model.addPoint(Point(x, y))
        index = self.point_model.index(self.point_model.rowCount() - 1)
        self.addItem(PointGraphicsItem(self.point_model, self, index))
        if self.polygon:
            self.constructConvexHull()

    def addItems(self):
        for row in range(self.point_model.rowCount()):
            index = self.point_model.index(row)
            self.addItem(PointGraphicsItem(self.point_model, self, index))

    def constructConvexHull(self, hull_method=jarvis):
        self.polygon.setPolygon(
            QPolygonF(
                (QPointF(*point.coords) for point in hull_method(self.point_model.points))
            )
        )


class PointGraphicsItem(QGraphicsEllipseItem):
    rad = 5
    def __init__(self, point_model, scene, index):
        self.point_model=point_model
        self.scene = scene
        self.index = index
        super().__init__(0, 0, 2*self.rad, 2*self.rad)
        shift = tuple(map(sub, self.get_point_data(), (self.rad, self.rad)))
        self.moveBy(*shift)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setBrush(Qt.blue)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        self.point_model.setData(self.index, value, Qt.UserRole, self.rad)
        return super().itemChange(change, value)

    def get_point_data(self):
        return self.point_model.data(self.index, Qt.UserRole)
