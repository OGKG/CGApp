from PyQt5.QtGui import QPolygonF
from module.algo.jarvis import jarvis
from operator import sub
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsScene
from PyQt5.QtCore import QAbstractListModel, QPersistentModelIndex, QPointF, QVariant, Qt, QModelIndex
from module.models.point import Point
from .polygon import PolygonGraphicsItem

class PointListModel(QAbstractListModel):
    
    def __init__(self, points=[], parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)
        self.points = points

    def rowCount(self, parent=None) -> int:
        return len(self.points)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(str(self.points[index.row()]))
        if index.isValid() and role == Qt.UserRole:
            return self.points[index.row()].x, self.points[index.row()].y
        return QVariant()

    def setData(self, index, value, role: int, radius) -> bool:
        self.beginResetModel()
        super().setData(QModelIndex(index), value, role=role)
        if isinstance(value, QPointF):
            self.points[index.row()].coords = (value.x()+radius, value.y()+radius)
        self.dataChanged.emit(index, index, [role])
        self.endResetModel()

    def setDataByPoint(self, point, value, role, radius):
        self.beginResetModel()
        index = self.index(self.points.index(point), 0, QModelIndex())
        if isinstance(value, QPointF):
            point.coords = (value.x()+radius, value.y()+radius)
        self.dataChanged.emit(index, index, [role])
        self.endResetModel()


    def addPoint(self, point):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.points.append(point)
        self.endInsertRows()

    def remove(self, point):
        self.beginRemoveRows(QModelIndex(), 0, self.rowCount())
        self.points.remove(point)
        self.endRemoveRows()



class PointScene(QGraphicsScene):
    def __init__(self, point_model):
        QGraphicsScene.__init__(self)
        self.point_model = point_model
        self.polygon = PolygonGraphicsItem([])
        self.polygon.setZValue(-1)
        self.addItems()
        self.addItem(self.polygon)

    '''Add a new point on mouse double-click'''
    def mouseDoubleClickEvent(self, event):
        x, y = event.scenePos().x(), event.scenePos().y()
        self.point_model.addPoint(Point(x, y))
        index = self.point_model.index(self.point_model.rowCount() - 1)
        self.addItem(PointGraphicsItem(self.point_model, self, index))

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
        self.point = point_model.points[index.row()]
        super().__init__(0, 0, 2*self.rad, 2*self.rad)
        shift = tuple(map(sub, (self.point.coords), (self.rad, self.rad)))
        self.moveBy(*shift)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setBrush(Qt.blue)

    def mousePressEvent(self, event):
        self.prepareGeometryChange()
        if event.button() == Qt.RightButton:
            self.point_model.remove(self.point)
            self.scene.removeItem(self)
            self.scene.constructConvexHull()
            del self

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        if change != QGraphicsItem.GraphicsItemChange.ItemSceneChange\
        and change != QGraphicsItem.GraphicsItemChange.ItemSceneHasChanged:
            self.prepareGeometryChange()
            self.point_model.setDataByPoint(self.point, value, Qt.UserRole, self.rad)
            self.scene.constructConvexHull()
        return super().itemChange(change, value)