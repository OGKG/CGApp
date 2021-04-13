from PyQt5.QtCore import QAbstractListModel, QVariant, QPointF, Qt, QModelIndex
from PyQt5.QtGui import QColor, QPen, QPolygonF
from PyQt5.QtWidgets import QGraphicsPolygonItem


class PolygonModel(QAbstractListModel):
    def __init__(self, points, parent=None, *args):
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

    def setData(self, index, value, role: int) -> bool:
        super().setData(index, value, role=role)
        if isinstance(value, QPointF):
            self.points[index.row()].coords = (value.x(), value.y())
        self.dataChanged.emit(index, index, [role])

    def addPoint(self, point):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.points.append(point)
        self.endInsertRows()


class PolygonGraphicsItem(QGraphicsPolygonItem):
    def __init__(self, points, parent=None):
        self.points = points
        polygon = QPolygonF(points)
        QGraphicsPolygonItem.__init__(self, polygon, parent)
        self.setPen(Qt.red)
