from .point import PointScene
from .graphics_view import GraphicsView
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListView, QPushButton, QVBoxLayout


class Algorithm:
    """Represents an algorithm to solve the problem in interactive mode."""
    def __init__(self, view):
        self.stagesRenderMethods = []
        self.stageResults = []
        self.view = view
    
    def setSceneAndPointModel(self, scene):
        self.scene = scene
        self.point_model = scene.point_model

    @staticmethod
    def solve(points):
        pass

    def refresh(self):
        self.stageResults = list(self.solve(self.scene.point_model.points))

    def changeSceneState(self, stage_index):
        self.refresh()
        self.stagesRenderMethods[stage_index]()

    def setScenePoints(self):
        for i in range(self.scene.point_model.rowCount()):
            index = self.scene.point_model.index(i)
            self.scene.addItem(self.scene.graphicsItemClass(self.scene.point_model, self.scene, index))


class AlgorithmScene(PointScene):
    """A point scene that refreshes according to changes in algorithm's input."""
    def __init__(self, point_model, algorithm, view):
        super().__init__(point_model, view)
        self.algorithm = algorithm
        self.textFields = []

    def refresh(self):
        self.algorithm.refresh()
        self.clearTextFields()
    
    def clearTextFields(self):
        for textField in self.textFields:
            self.removeItem(textField)
        self.textFields = []


class AlgorithmLayout(QHBoxLayout):
    stageCount = 0
    algorithmClass = Algorithm
    algorithmName = ""

    def __init__(self, point_model, parent=None):
        super(AlgorithmLayout, self).__init__(parent)
        self.algorithmLabel = QLabel(self.algorithmName)
        self.stageLabel = QLabel("Етап 0. Умова")
        self.view = GraphicsView(self.stageLabel)
        self.point_model = point_model
        self.algorithm = self.algorithmClass(self.view)

        self.vLayoutLeft = QVBoxLayout()
        self.vLayoutRight = QVBoxLayout()
        self.hLayout = QHBoxLayout()

        self.vLayoutLeft.addWidget(self.algorithmLabel)
        self.pointsListView = QListView()
        self.pointsListView.setModel(self.point_model)
        self.vLayoutLeft.addWidget(self.pointsListView)

        self.vLayoutRight.addWidget(self.stageLabel)
        self.scene = PointScene(self.point_model, self.view)
        self.view.setScene(self.scene)
        self.algorithm.setSceneAndPointModel(self.scene)
        self.vLayoutRight.addWidget(self.view)

        btn_layout = QHBoxLayout()
        for i in range(self.stageCount):
            btn = StageButton(i, self)
            btn_layout.addWidget(btn)
        
        self.vLayoutRight.addLayout(btn_layout)
        self.addLayout(self.vLayoutLeft)
        self.addLayout(self.vLayoutRight)


class StageButton(QPushButton):
    def __init__(self, stage_index, layout):
        super().__init__(str(stage_index))
        self.stageIndex = stage_index
        self.layout = layout
        self.clicked.connect(lambda: StageButton.click(self.layout, self.stageIndex))
        
    @staticmethod
    def click(layout, stageIndex):
        layout.algorithm.changeSceneState(stageIndex)
