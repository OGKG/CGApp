from operator import sub
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsScene, QGraphicsSceneMouseEvent, QGraphicsTextItem
from PyQt5.QtCore import QAbstractListModel, QPointF, QVariant, Qt, QModelIndex
from module.models.point import Point


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

    def setDataByPoint(self, point, value, role):
        self.beginResetModel()
        index = self.index(self.points.index(point), 0, QModelIndex())
        if isinstance(value, QPointF):
            point.coords = (value.x(), value.y())
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


class PointGraphicsItem(QGraphicsEllipseItem):
    rad = 5
    def __init__(self, point_model, scene, index):
        super().__init__(-self.rad, -self.rad, 2*self.rad, 2*self.rad)
        self.point_model=point_model
        self.scene = scene
        self.point = point_model.points[index.row()]
        self.moveBy(*self.point.coords)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setBrush(Qt.blue)
        self.append_children()
    
    def append_children(self):
        pass

    def mousePressEvent(self, event):
        self.prepareGeometryChange()
        if event.button() == Qt.RightButton:
            self.point_model.remove(self.point)
            self.scene.removeItem(self)
            self.scene.refresh()
            del self

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemChildAddedChange or\
            change == QGraphicsItem.GraphicsItemChange.ItemParentHasChanged:
            return super().itemChange(change, value)
        
        if change != QGraphicsItem.GraphicsItemChange.ItemSceneChange\
        and change != QGraphicsItem.GraphicsItemChange.ItemSceneHasChanged:
            self.prepareGeometryChange()
            self.point_model.setDataByPoint(self.point, value, Qt.UserRole)
            if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange\
            or change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
                self.scene.refresh()
        return super().itemChange(change, value)


class PointScene(QGraphicsScene):
    graphicsItemClass = PointGraphicsItem
    def __init__(self, point_model, view):
        QGraphicsScene.__init__(self)
        self.point_model = point_model
        self.view = view

    def mouseDoubleClickEvent(self, event):
        x, y = event.scenePos().x(), event.scenePos().y()
        self.point_model.addPoint(Point(x, y))
        index = self.point_model.index(self.point_model.rowCount() - 1)
        self.addItem(self.graphicsItemClass(self.point_model, self, index))
        self.refresh()

    def refresh(self):
        pass
