from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import Qt
from base.point import PointGraphicsItem, PointScene
from base.algorithm import Algorithm
from base.evaluator import Evaluator
from module.models.bin_tree_node import Node
from module.models.bin_tree import BinTree
from module.algo.quickhull import quickhull_gen


class QuickhullAlgorithm(Algorithm):
    method = quickhull_gen

    def refresh(self):
        self.stageResults = list(quickhull_gen(self.scene.point_model.points))

    def renderStage1(self):
        leftmost = self.stageResults[0][0]
        rightmost = self.stageResults[0][1]
        s1 = self.stageResults[0][2]
        s2 = self.stageResults[0][3]
        
        self.scene.clear()
        self.setScenePoints()
        self.refresh()

        l_point = list(filter(lambda i: i.point == leftmost, self.graphicsView.scene.items()))[0]
        r_point = list(filter(lambda i: i.point == rightmost, self.graphicsView.scene.items()))[0]
        l_point.setBrush(Qt.red)
        r_point.setBrush(Qt.red)

        # TODO: enumerate points s1 and s2-wise

    # TODO: write other stages' rendering

class QuickhullPointGraphicsItem(PointGraphicsItem):
    def __init__(self, point_model, scene, index):
        super().__init__(point_model, scene, index)
        self.setFlag(QGraphicsItem.ItemIsMovablem, False)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, False)


class QuickhullPointScene(PointScene):
    graphicsItemClass = QuickhullPointGraphicsItem

    def mouseDoubleClickEvent(self, event):
        pass


class QuickhullEvaluator(Evaluator):
    fines = [0.25, 0.25, 0.25, 0.25, 1]
    extra_fines = [0, 0.25, 0, 0, 0]
    
    def __init__(self, points, parent=None, *args):
        super(QuickhullEvaluator, self).__init__(points, parent, *args)
        self.res = 2
        self.min = 0
        self.max = 0
        self.s1 = []
        self.s2 = []
        self.h_list = []
        self.tree = BinTree(Node([]))
        self.hull = []
        self.correct_stages = list(quickhull_gen(points))
    
    @property
    def score(self):
        res = 2
        stages = [
            (
                self.min,
                self.max,
                self.s1,
                self.s2
            ),
            self.h_list,
            self.tree.to_list(),
            self.tree.leaves,
            self.hull
        ]

        return self.evaluate(stages, res)
