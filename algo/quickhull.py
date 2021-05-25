from PyQt5.QtGui import QPen
from base.graphics_view import ExtraView
from base.tree import BinTreeNodeGraphicsItem, BinTreeScene
from base.text import GraphicsTextItem
from algo.hull import QuickhullScene
from base.tree_scene import TreeScene
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsLineItem, QGraphicsScene, QGraphicsTextItem, QGraphicsView
from PyQt5.QtCore import Qt
from base.point import PointGraphicsItem, PointScene
from base.algorithm import Algorithm, AlgorithmScene, AlgorithmLayout
from module.models.bin_tree_node import Node
from module.models.bin_tree import BinTree
from module.algo.quickhull import quickhull_gen


class QuickhullAlgorithm(Algorithm):
    def __init__(self, view, extraViews=[]):
        super().__init__(view, extraViews)
        self.stagesRenderMethods.extend(
            [
                self.renderStage0,
                self.renderStage1,
                self.renderStage2,
            ]
        )

    @staticmethod
    def solve(points):
        return quickhull_gen(points)

    def renderStage0(self):
        self.view.stageLabel.setText("Етап 0. Умова")
        self.scene = PointScene(self.point_model, self.view)
        self.view.setScene(self.scene)
        self.setScenePoints()
        self.extraViews[0].setVisible(False)

    def renderStage1(self):
        self.view.stageLabel.setText("Етап 1. Розбиття")
        self.scene = QuickhullPointScene(self.point_model, self, self.view)
        self.view.setScene(self.scene)
        self.setScenePoints()
        self.scene.refresh()

        s1 = list(enumerate(self.stageResults[0][2], start=1))
        s2 = list(enumerate(self.stageResults[0][3][1:-1], start=len(s1)+1))
        s = s1 + s2
        tree = self.stageResults[3]
        self.overwriteTreeNodes(tree.root, s)

        extraView = self.extraViews[0]
        tree_scene = QuickhullTreeScene(tree, extraView.width(), extraView.height())
        extraView.setScene(tree_scene)
        extraView.setVisible(True)

        self.scene.treeScene = tree_scene

    def renderStage2(self):
        self.view.stageLabel.setText("Етап 3. Результат")
        self.scene = QuickhullScene(self.point_model, self.view)
        self.view.setScene(self.scene)
        self.setScenePoints()
        self.scene.refresh()
        self.extraViews[0].setVisible(False)
    
    def overwriteTreeNodes(self, node, s):
        point_indices = [list(filter(lambda i: i[1] == p, s))[0][0] for p in node.data]
        node.data = "{"
        for i in point_indices:
            node.data += str(i) + ","
        node.data = node.data[:-1] + "}"

        if node.left:
            self.overwriteTreeNodes(node.left, s)
        if node.right:
            self.overwriteTreeNodes(node.right, s)


class QuickhullPointScene(AlgorithmScene):
    treeScene = None

    def refresh(self):
        if not self.items():
            return
        super().refresh()
        
        for i in filter(lambda i: isinstance(i, QGraphicsLineItem), self.items()):
            self.removeItem(i)
        
        for i in self.items():
            i.setBrush(Qt.blue)

        self.drawLrLine()
        self.drawHlrLines()
        
        s1 = list(enumerate(self.algorithm.stageResults[0][2], start=1))
        s2 = list(enumerate(self.algorithm.stageResults[0][3][1:-1], start=len(s1)+1))

        self.enumeratePoints(s1)
        self.enumeratePoints(s2)

        if self.treeScene:
            self.setTreeScene(s1, s2)

    def drawLrLine(self):
        leftmost = list(filter(lambda i: i.point == self.algorithm.stageResults[0][0], self.items()))[0]
        rightmost = list(filter(lambda i: i.point == self.algorithm.stageResults[0][1], self.items()))[0]
        leftmost.setBrush(Qt.red)
        rightmost.setBrush(Qt.red)
        
        lr_line = QGraphicsLineItem(leftmost.x(), leftmost.y(), rightmost.x(), rightmost.y())
        lr_line.setPen(Qt.red)
        lr_line.setZValue(-1)
        self.addItem(lr_line)

    def drawHlrLines(self):
        hlr = self.algorithm.stageResults[1]
        for h, l, r in hlr:
            pen = QPen()
            pen.setStyle(Qt.PenStyle.DashLine)

            lh_line = QGraphicsLineItem(l.x, l.y, h.x, h.y)
            lh_line.setPen(pen)
            lh_line.setZValue(-1)
            rh_line = QGraphicsLineItem(r.x, r.y, h.x, h.y)
            rh_line.setPen(pen)
            rh_line.setZValue(-1)
            self.addItem(lh_line)
            self.addItem(rh_line)
        
    def enumeratePoints(self, point_set):
        for p in point_set:
            text = GraphicsTextItem(str(p[0]))
            text.moveBy(*p[1].coords)
            self.textFields.append(text)
            self.addItem(text)
    
    def setTreeScene(self, s1, s2):
        s = s1 + s2
        tree = self.algorithm.stageResults[3]
        self.algorithm.overwriteTreeNodes(tree.root, s)
        extraView = self.algorithm.extraViews[0]
        self.treeScene = QuickhullTreeScene(tree, extraView.width(), extraView.height())
        extraView.setScene(self.treeScene)


class QuickhullTreeScene(BinTreeScene):
    def constructTree(self):
        root_item = BinTreeNodeGraphicsItem("S", self.tree.root.data)
        root_item.setBrush(Qt.white)
        self.addItem(root_item)
        x, y = self.width() / 2 - self.rad, self.rad
        root_item.moveBy(x, y)

        text_item = QGraphicsTextItem("S")
        text_item.moveBy(x-self.rad/2, y-self.rad/2)
        self.addItem(text_item)

        self._constructTree(self.tree.root.left, x-self.width()/4, 4*self.rad, x, y, "S<sub>1")
        self._constructTree(self.tree.root.right, x+self.width()/4, 4*self.rad, x, y, "S<sub>2")

    def _constructTree(self, node, x, y, par_x, par_y, text, depth=1, h_index=0):
        node_item = BinTreeNodeGraphicsItem(text, node.data, depth)
        node_item.setBrush(Qt.white)
        self.addItem(node_item)
        node_item.moveBy(x, y)
        dx, dy = self.width() / (2 ** (depth + 2)), 4 * self.rad

        text_item = QGraphicsTextItem()
        text_item.setHtml(text+"</sub>")
        text_item.moveBy(x-self.rad/2, y-self.rad/2)
        self.addItem(text_item)

        edge = QGraphicsLineItem(x, y, par_x, par_y)
        edge.setZValue(-1)
        self.addItem(edge)

        if node.left:
            new_text = text + "1"
            self._constructTree(node.left, x-dx, y+dy, x, y, new_text, depth+1, 2*h_index)
        if node.right:
            new_text = text + "2"
            self._constructTree(node.right, x+dx, y+dy, x, y, new_text, depth+1, 2*h_index+1)            


class QuickhullLayout(AlgorithmLayout):
    algorithmName = "Метод Швидкобол"
    stageCount = 3
    algorithmClass = QuickhullAlgorithm
    initSceneClass = PointScene

    def __init__(self, point_model, parent=None):
        self.treeView = ExtraView()
        self.treeView.setVisible(False)
        self.extraViews.append(self.treeView)
        super().__init__(point_model, parent)
