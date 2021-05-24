from base.tree import BinTreeNodeGraphicsItem, BinTreeScene, BinTreeSquareNodeGraphicsItem
from base.text import GraphicsTextItem
from base.rect import RectGraphicsItem
from PyQt5.QtGui import QCursor, QTransform
from base.graphics_view import ExtraView
from base.point import PointGraphicsItem, PointListModel, PointScene
from module.algo.kd_tree_method import kd_tree_gen
from base.algorithm import Algorithm, AlgorithmLayout, AlgorithmScene
from PyQt5.QtCore import QLineF, QPointF, QRectF, Qt
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QGraphicsRectItem, QGraphicsScene, QGraphicsSceneMouseEvent, QGraphicsTextItem, QGraphicsView, QInputDialog, QLineEdit
from module.models.bin_tree_node import Node
from module.models.bin_tree import KdTree
from operator import sub, truediv

class KdTreePointListModel(PointListModel):
    xRange = [0, 500]
    yRange = [0, 250]

    def __init__(self, points=[], parent=None, *args):
        super().__init__(points=points, parent=parent, *args)


class KdTreeAlgorithm(Algorithm):
    def __init__(self, view, extraViews=[]):
        super().__init__(view, extraViews)
        self.stagesRenderMethods.extend(
            [
                self.renderStage0,
                self.renderStage1
            ]
        )
    
    def refresh(self):
        self.stageResults = list(
            self.solve(
                self.scene.point_model.points,
                self.scene.point_model.xRange,
                self.scene.point_model.yRange
            )
        )

    @staticmethod
    def solve(points, x_range, y_range):
        return kd_tree_gen(points, x_range, y_range)

    def renderStage0(self):
        self.view.stageLabel.setText("Етап 0. Умова")
        self.scene = KdTreePointScene(self.point_model, self.view)
        self.view.setScene(self.scene)
        self.setScenePoints()
        self.scene.setSearchRegion(*self.point_model.xRange, *self.point_model.yRange)
        self.extraViews[0].setVisible(False)
    
    def renderStage1(self):
        self.view.stageLabel.setText("Етап 1-3. Розбиття. Побудова дерева. Пошук у дереві")
        self.scene = KdTreePartitionScene(self.point_model, self, self.view)
        self.view.setScene(self.scene)
        self.setScenePoints()
        self.scene.setSearchRegion()
        self.scene.refresh()

        tree = self.stageResults[1]
        ordered_x = list(enumerate(self.stageResults[0], start=1))
        region_points = [p[0] for p in filter(lambda x: x[1] in self.stageResults[3], ordered_x)]
        self.overwriteTreeNodes(tree.root, ordered_x)

        extraView = self.extraViews[0]
        tree_scene = KdTreeScene(tree, extraView.width(), extraView.height(), region_points)
        extraView.setScene(tree_scene)
        extraView.setVisible(True)

        self.scene.treeScene = tree_scene
    
    def overwriteTreeNodes(self, node, ordered_points):
        node.data = list(filter(lambda p: p[1] == node.data, ordered_points))[0][0]

        if node.left:
            self.overwriteTreeNodes(node.left, ordered_points)
        if node.right:
            self.overwriteTreeNodes(node.right, ordered_points)


class KdTreePointScene(PointScene):
    mousePressed = False
    mousePos = (0, 0)
    rect = None
    
    def setSearchRegion(self, xmin, xmax, ymin, ymax):
        rect = RectGraphicsItem(xmin, ymin, xmax, ymax, self.point_model)
        rect.setPen(Qt.blue)
        self.addItem(rect)
        self.point_model.xRange = [xmin, xmax]
        self.point_model.yRange = [ymin, ymax]


class KdTreePartitionScene(AlgorithmScene):
    hLinesYCoords = []
    vLinesXCoords = []
    vLinesYRanges = []
    hLinesXRanges = []
    treeScene = None
    rect = None
    
    def initLines(self):
        ry_min, ry_max = self.rect.y(), self.rect.y() + self.rect.boundingRect().height()
        rx_min, rx_max = self.rect.x(), self.rect.x() + self.rect.boundingRect().width()
        x_min = min(rx_min, min(self.point_model.points, key=lambda p: p.x).x) - 50
        y_min = min(ry_min, min(self.point_model.points, key=lambda p: p.y).y) - 50
        x_max = max(rx_max, max(self.point_model.points, key=lambda p: p.x).x) + 50
        y_max = max(ry_max, max(self.point_model.points, key=lambda p: p.y).y) + 50
        self.vLinesXCoords = [x_min, x_max]
        self.hLinesYCoords = [y_min, y_max]
        self.vLinesYRanges = [[y_min, y_max], [y_min, y_max]]
        self.hLinesXRanges = [[x_min, x_max], [x_min, x_max]]
        v_line = QGraphicsLineItem(x_min, y_min, x_min, y_max)
        h_line = QGraphicsLineItem(x_min, y_min, x_max, y_min)
        v_line2 = QGraphicsLineItem(x_max, y_min, x_max, y_max)
        h_line2 = QGraphicsLineItem(x_min, y_max, x_max, y_max)
        self.addItem(v_line)
        self.addItem(h_line)
        self.addItem(v_line2)
        self.addItem(h_line2)

    def setSearchRegion(self):
        rect = RectGraphicsItem(
            self.point_model.xRange[0],
            self.point_model.yRange[0],
            self.point_model.xRange[1],
            self.point_model.yRange[1],
            self.point_model,
            self
        )
        rect.setPen(Qt.blue)
        rect.setEnabled(False)
        self.addItem(rect)
        self.rect = rect
        
    def refresh(self):
        if not self.items():
            return
        super().refresh()

        for i in filter(lambda i: isinstance(i, QGraphicsLineItem), self.items()):
            self.removeItem(i)
        
        self.initLines()

        ordered_x = list(enumerate(self.algorithm.stageResults[0], start=1))
        self.enumeratePoints(ordered_x)
        self.makePartition()

        if self.treeScene:
            self.setTreeScene()
    
    def setTreeScene(self):
        tree = self.algorithm.stageResults[1]
        ordered_x = list(enumerate(self.algorithm.stageResults[0], start=1))
        self.algorithm.overwriteTreeNodes(tree.root, ordered_x)

        extraView = self.algorithm.extraViews[0]
        region_points = [p[0] for p in filter(lambda x: x[1] in self.algorithm.stageResults[3], ordered_x)]
        tree_scene = KdTreeScene(tree, extraView.width(), extraView.height(), region_points)
        extraView.setScene(tree_scene)
        extraView.setVisible(True)

        self.treeScene = tree_scene
    
    def enumeratePoints(self, points):
        for p in points:
            text = GraphicsTextItem(str(p[0]))
            text.moveBy(*p[1].coords)
            self.textFields.append(text)
            self.addItem(text)
    
    def makePartition(self):
        medians = self.algorithm.stageResults[1].to_list()
        directions = self.algorithm.stageResults[2]

        for i in range(len(medians)):
            point = medians[i]
            vertical = directions[i]
            line = None

            if vertical:
                lowermostY, uppermostY = self._boundingHorizontalLinesYCoords(*point.data.coords)
                x = point.data.x
                line = QGraphicsLineItem(
                    QLineF(
                        QPointF(x, lowermostY),
                        QPointF(x, uppermostY)
                    )
                )
                line.setPen(Qt.red)
                line.setZValue(-1)
                self.vLinesXCoords.append(x)
                self.vLinesYRanges.append([lowermostY, uppermostY])
            else:
                leftmostX, rightmostX = self._boundingVerticalLinesXCoords(*point.data.coords)
                y = point.data.y
                line = QGraphicsLineItem( 
                    QLineF(
                        QPointF(leftmostX, y),
                        QPointF(rightmostX, y)
                    )
                )
                line.setPen(Qt.green)
                line.setZValue(-2)
                self.hLinesYCoords.append(y)
                self.hLinesXRanges.append([leftmostX, rightmostX])
        
            self.addItem(line)

    def _boundingVerticalLinesXCoords(self, x0, y0):
        lines_data = list(zip(self.vLinesXCoords, self.vLinesYRanges))
        lowermostY = max(filter(lambda y: y <= y0, self.hLinesYCoords))
        uppermostY = min(filter(lambda y: y >= y0, self.hLinesYCoords))

        leftmostX = max(
            [
                x[0] for x in list(
                    filter(
                        lambda e: e[0] <= x0
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
                        lambda e: e[0] >= x0
                        and not self._lineOutOfBounds(e[1], lowermostY, uppermostY),
                        lines_data
                    )
                )
            ]
        )
        return leftmostX, rightmostX
    
    def _boundingHorizontalLinesYCoords(self, x0, y0):
        lines_data = list(zip(self.hLinesYCoords, self.hLinesXRanges))
        leftmostX = max(filter(lambda x: x <= x0, self.vLinesXCoords))
        rightmostX = min(filter(lambda x: x >= x0, self.vLinesXCoords))
        lowermostY = max(
            [
                x[0] for x in list(
                    filter(
                        lambda e: e[0] <= y0
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
                        lambda e: e[0] >= y0
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


class KdTreeScene(BinTreeScene):
    nodeWidth = BinTreeSquareNodeGraphicsItem.width

    def __init__(self, tree, width, height, region_points):
        self.nodeCount = 0
        self.regionPoints = region_points
        super().__init__(tree, width, height)

    def constructTree(self):
        root_item = BinTreeNodeGraphicsItem(str(self.tree.root.data))
        root_item.setBrush(Qt.white)
        if self.tree.root.data in self.regionPoints:
            root_item.setPen(Qt.green)
        self.addItem(root_item)
        x, y = (self.width() - self.nodeWidth) / 2, self.nodeWidth / 2
        root_item.moveBy(x, y)

        text_item = QGraphicsTextItem(root_item.text)
        text_item.moveBy(x-self.nodeWidth/4, y-self.nodeWidth/4)
        self.addItem(text_item)

        self._constructTree(self.tree.root.left, x-self.width()/4, 2*self.nodeWidth, x, y, str(self.tree.root.left.data))
        self._constructTree(self.tree.root.right, x+self.width()/4, 2*self.nodeWidth, x, y, str(self.tree.root.right.data))

    
    def _constructTree(self, node, x, y, par_x, par_y, text, squared=True, depth=1, h_index=0):
        if squared:
            node_item = BinTreeSquareNodeGraphicsItem(text, depth=depth)
        else:
            node_item = BinTreeNodeGraphicsItem(text, depth=depth)
        
        self.nodeCount += 1
        
        node_item.setBrush(Qt.white)
        if node.data in self.regionPoints:
            node_item.setPen(Qt.green)

        self.addItem(node_item)
        node_item.moveBy(x, y)
        dx, dy = self.width() / (2 ** (depth + 2)), 2 * self.nodeWidth

        text_item = QGraphicsTextItem(text)
        text_item.moveBy(x-self.nodeWidth/4, y-self.nodeWidth/4)
        self.addItem(text_item)

        edge = QGraphicsLineItem(x, y, par_x, par_y)
        edge.setZValue(-1)
        self.addItem(edge)

        if node.left:
            self._constructTree(node.left, x-dx, y+dy, x, y, str(node.left.data), not squared, depth+1, 2*h_index)
        if node.right:
            self._constructTree(node.right, x+dx, y+dy, x, y, str(node.right.data), not squared, depth+1, 2*h_index+1)


class KdTreeLayout(AlgorithmLayout):
    algorithmName = "Метод k-d дерева"
    stageCount = 2
    algorithmClass = KdTreeAlgorithm
    initSceneClass = KdTreePointScene

    def __init__(self, point_model, parent=None):
        self.treeView = ExtraView()
        self.treeView.setVisible(False)
        self.extraViews.append(self.treeView)
        super().__init__(point_model, parent)
        self.scene.setSearchRegion(*point_model.xRange, *point_model.yRange)
