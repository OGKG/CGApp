from algo.hull import QuickhullScene
from base.tree_scene import TreeScene
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsTextItem
from PyQt5.QtCore import Qt
from base.point import PointGraphicsItem, PointScene
from base.algorithm import Algorithm, AlgorithmScene, AlgorithmLayout
from base.evaluator import Evaluator
from module.models.bin_tree_node import Node
from module.models.bin_tree import BinTree
from module.algo.quickhull import quickhull_gen


class QuickhullAlgorithm(Algorithm):
    def __init__(self, view):
        super().__init__(view)
        self.stagesRenderMethods.extend(
            [
                self.renderStage0,
                self.renderStage1,
                self.renderStage2,
                self.renderStage3
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

    def renderStage1(self):
        self.view.stageLabel.setText("Етап 1. Розбиття")
        self.scene = QuickhullPointScene(self.point_model, self, self.view)
        self.view.setScene(self.scene)
        self.setScenePoints()
        self.scene.refresh()

    def renderStage2(self):
        self.view.stageLabel.setText("Етап 2. Злиття (<b>TBD</b>)")
        self.scene = QGraphicsScene() # dummy
        self.view.setScene(self.scene)
        # TODO: tree construction

    def renderStage3(self):
        self.view.stageLabel.setText("Етап 3. Результат")
        self.scene = QuickhullScene(self.point_model, self.view)
        self.view.setScene(self.scene)
        self.setScenePoints()
        self.scene.refresh()


class QuickhullPointScene(AlgorithmScene):
    def refresh(self):
        if not self.items():
            return
        super().refresh()
        
        for i in self.items():
            i.setBrush(Qt.blue)

        leftmost = list(filter(lambda i: i.point == self.algorithm.stageResults[0][0], self.items()))[0]
        rightmost = list(filter(lambda i: i.point == self.algorithm.stageResults[0][1], self.items()))[0]
        leftmost.setBrush(Qt.red)
        rightmost.setBrush(Qt.red)
        
        s1 = list(enumerate(self.algorithm.stageResults[0][2], start=1))
        s2 = list(enumerate(self.algorithm.stageResults[0][3][1:-1], start=len(s1)+1))

        self.enumeratePoints(s1)
        self.enumeratePoints(s2)
        
    def enumeratePoints(self, point_set):
        for p in point_set:
            text = QGraphicsTextItem(str(p[0]))
            text.moveBy(*p[1].coords)
            self.textFields.append(text)
            self.addItem(text)






class QuickhullTreeScene(TreeScene):
    pass


class QuickhullLayout(AlgorithmLayout):
    algorithmName = "Метод Швидкобол"
    stageCount = 4
    algorithmClass = QuickhullAlgorithm


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
