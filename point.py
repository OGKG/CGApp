from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsScene
from PyQt5.QtCore import QAbstractListModel, QPointF, QVariant, Qt


class PointListModel(QAbstractListModel):
    radius = 10
    def __init__(self, point_list=[], scene=None, parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)
        self.point_list = point_list
        self.scene = scene

    def rowCount(self, parent=None) -> int:
        return len(self.point_list)

    def data(self, index, role):
        if index.isValid() and role == Qt.DisplayRole:
            return QVariant(str(self.point_list[index.row()]))
        if index.isValid() and role == Qt.UserRole:
            return self.point_list[index.row()].x, self.point_list[index.row()].y
        return QVariant()

    def setData(self, index, value, role: int) -> bool:
        super().setData(index, value, role=role)
        if isinstance(value, QPointF):
            self.point_list[index.row()].coords = (value.x(), value.y())
        self.dataChanged.emit(index, index, [role])
    

class PointScene(QGraphicsScene):
    def __init__(self, point_model):
        QGraphicsScene.__init__(self)
        self.point_model = point_model
        self.addItems()

    def addItems(self):
        for row in range(self.point_model.rowCount()):
            index = self.point_model.index(row)
            self.addItem(PointGraphicsItem(self.point_model, index))


class PointGraphicsItem(QGraphicsEllipseItem):
    rad = 5
    def __init__(self, point_model, index):
        self.point_model=point_model
        self.index = index
        super().__init__(0, 0, 2*self.rad, 2*self.rad)
        self.moveBy(*self.get_point_data())
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setBrush(Qt.green)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        self.point_model.setData(self.index, value, Qt.UserRole)
        return super().itemChange(change, value)

    def get_point_data(self):
        return self.point_model.data(self.index, Qt.UserRole)
