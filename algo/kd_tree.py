from PyQt5.QtCore import QLineF, QPointF, Qt
from main import PointGraphicsView
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsScene, QGraphicsView, QInputDialog, QLineEdit
from base.task_layout import TaskLayout
from module.models.bin_tree_node import Node
from module.models.bin_tree import KdTree
from base.task_model import TaskModel
from operator import sub


class KdTreeTaskLayout(TaskLayout):
    def __init__(self, point_model, task_model, parent=None):
        super(KdTreeTaskLayout, self).__init__(point_model, task_model, None, parent)
        self.xListInput = QLineEdit()
        self.yListInput = QLineEdit()
        
        self.partitionScene = KdTreePartitionScene(point_model, task_model)
        self.treeScene = KdTreeScene(point_model, task_model)
        
        graphics_view = KdTreeGraphicsView()
        graphics_view.setScene(self.partitionScene)
        self.vlayout_input.addWidget(graphics_view)
        self.vlayout_right.addLayout(self.vlayout_input)
        self.stageLayouts = []

        self.addLayout(self.vlayout_left)
        self.addLayout(self.vlayout_right)


class KdTreeTaskModel(TaskModel):
    fines = [0.25, 0.75, 1, 1]
    extra_fines = [0, 0, 0, 0]
    
    def __init__(self, points, x_range, y_range, parent=None, *args):
        super(KdTreeTaskModel, self).__init__(points, parent, *args)
        self.xList = []
        self.yList = []
        self.tree = KdTree(Node(None), x_range, y_range)
        self.ans_points = []
    
    @property
    def score(self):
        res = 3
        stages = [
            (
                self.xList,
                self.yList
            ),
            self.tree.directions,
            self.tree,
            self.ans_points
        ]

        return self.evaluate(stages, res)


class KdTreePartitionScene(QGraphicsScene):
    def __init__(self, point_model, task_model):
        QGraphicsScene.__init__(self)
        self.point_model = point_model
        self.task_model = task_model
        self.addItems()

        x_max = max(self.point_model.points, key=lambda p: p.x).x + 20
        y_max = max(self.point_model.points, key=lambda p: p.y).y + 20
        self.vLinesXCoords = [0, x_max]
        self.hLinesYCoords = [0, y_max]
        self.vLinesYRanges = [[0, y_max], [0, y_max]]
        self.hLinesXRanges = [[0, x_max], [0, x_max]]

    def addItems(self):
        for row in range(self.point_model.rowCount()):
            index = self.point_model.index(row)
            self.addItem(KdTreePointGraphicsItem(self.point_model, self, index))
        


class KdTreeScene(QGraphicsScene):
    def __init__(self, point_model, task_model):
        QGraphicsScene.__init__(self)
        self.point_model = point_model
        self.task_model = task_model
        self.tree = task_model.tree
    
    def mousePressEvent(self, event):
        index = QInputDialog.getInt(
            self,
            "Додати вузол дерева",
            "Введіть номер точки:"
        )
        self.addItem(KdTreeNodeGraphicsItem(self, self.width() / 2, self.height() / 2, str(index)))
        return super().mousePressEvent(event)


class KdTreePointGraphicsItem(PointGraphicsView):
    rad = 5

    @property
    def point_data(self):
        return self.point_model.data(self.index, Qt.UserRole)

    def mousePressEvent(self, event):
        line = None
        direction = True
        
        if event.button() == Qt.LeftButton:
            lowermostY, uppermostY = self._boundingHorizontalLinesYCoords
            x = self.pos().x() + self.rad
            line = QGraphicsLineItem(
                QLineF(
                    QPointF(x, lowermostY),
                    QPointF(x, uppermostY)
                )
            )
            line.setPen(Qt.red)
            line.setZValue(-1)
            self.scene.vLinesXCoords.append(x)
            self.scene.vLinesYRanges.append([lowermostY, uppermostY])
        if event.button() == Qt.RightButton:
            leftmostX, rightmostX = self._boundingVerticalLinesXCoords
            y = self.pos().y() + self.rad
            line = QGraphicsLineItem( 
                QLineF(
                    QPointF(leftmostX, y),
                    QPointF(rightmostX, y)
                )
            )
            direction = False
            line.setPen(Qt.green)
            line.setZValue(-2)
            self.scene.hLinesYCoords.append(y)
            self.scene.hLinesXRanges.append([leftmostX, rightmostX])
        
        self.scene.addItem(line)
        self.scene.task_model.tree.directions.append(direction)
        return super().mousePressEvent(event)

    @property
    def _boundingVerticalLinesXCoords(self):
        lines_data = list(zip(self.scene.vLinesXCoords, self.scene.vLinesYRanges))
        lowermostY = max(filter(lambda y: y <= self.pos().y(), self.scene.hLinesYCoords))
        uppermostY = min(filter(lambda y: y >= self.pos().y(), self.scene.hLinesYCoords))

        leftmostX = max(
            [
                x[0] for x in list(
                    filter(
                        lambda e: e[0] <= self.pos().x()
                        and not self._lineOutOfBounds(e[1], lowermostY, uppermostY),
                        lines_data
                    )
                )
            ]
        )
        rightmostX = min(
            [
                x[0] for x in list(
                    filter(
                        lambda e: e[0] >= self.pos().x()
                        and not self._lineOutOfBounds(e[1], lowermostY, uppermostY),
                        lines_data
                    )
                )
            ]
        )
        return leftmostX, rightmostX
    
    @property
    def _boundingHorizontalLinesYCoords(self):
        lines_data = list(zip(self.scene.hLinesYCoords, self.scene.hLinesXRanges))
        leftmostX = max(filter(lambda x: x <= self.pos().x(), self.scene.vLinesXCoords))
        rightmostX = min(filter(lambda x: x >= self.pos().x(), self.scene.vLinesXCoords))
        lowermostY = max(
            [
                x[0] for x in list(
                    filter(
                        lambda e: e[0] <= self.pos().y()
                        and not self._lineOutOfBounds(e[1], leftmostX, rightmostX),
                        lines_data
                    )
                )
            ]
        )
        uppermostY = min(
            [
                x[0] for x in list(
                    filter(
                        lambda e: e[0] >= self.pos().y()
                        and not self._lineOutOfBounds(e[1], leftmostX, rightmostX),
                        lines_data
                    )
                )
            ]
        )
        return lowermostY, uppermostY
    
    def _lineOutOfBounds(self, line_range, lower_bound, upper_bound):
        if line_range[0] == lower_bound and line_range[1] == upper_bound:
            return False
        
        return line_range[0] >= upper_bound or line_range[1] <= lower_bound


class KdTreeNodeGraphicsItem(QGraphicsEllipseItem):
    rad = 20
    textSize = 10

    def __init__(self, scene, x, y, text, depth=0):
        self.scene = scene
        self.depth = depth
        self.text = text
        super().__init__(0, 0, 2*self.rad, 2*self.rad)
        shift = tuple(map(sub, (x, y), (self.rad, self.rad)))
        self.moveBy(*shift)
