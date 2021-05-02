from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtCore import Qt
from base.point import PointGraphicsItem, PointScene
from base.algorithm import Algorithm, AlgorithmScene
from base.evaluator import Evaluator
from module.models.bin_tree_node import Node
from module.models.bin_tree import BinTree
from module.algo.quickhull import quickhull_gen


class QuickhullAlgorithm(Algorithm):
    method = quickhull_gen

    def __init__(self, scene):
        super().__init__(scene)
        self.stagesRenderMethods.extend(
            [
                self.renderStage0,
                self.renderStage1,
                self.renderStage2,
                self.renderStage3
            ]
        )

    def renderStage0(self):
        self.scene = PointScene(self.scene.point_model)
        self.setScenePoints()

    def renderStage1(self):
        self.scene = QuickhullPointScene(self.scene.point_model)
        self.setScenePoints()

        leftmost = self.stageResults[0][0]
        rightmost = self.stageResults[0][1]
        s1 = self.stageResults[0][2]
        s2 = self.stageResults[0][3]

        items = self.scene.items()
        l_point = list(filter(lambda i: i.point == leftmost, items))[0]
        r_point = list(filter(lambda i: i.point == rightmost, items))[0]
        l_point.setBrush(Qt.red)
        r_point.setBrush(Qt.red)

        s1_points = list(filter(lambda i: i.point in s1, items))
        s2_points = list(filter(lambda i: i.point in s2, items))

        # TODO: enumerate points s1 and s2-wise

    # TODO: write other stages' rendering
    def renderStage2(self):
        pass

    def renderStage3(self):
        pass

class QuickhullPointScene(AlgorithmScene):
    algorithmClass = QuickhullAlgorithm
    stageIndex = 1


class QuickhullResultScene(AlgorithmScene):
    algorithmClass = QuickhullAlgorithm
    stageIndex = 3


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
