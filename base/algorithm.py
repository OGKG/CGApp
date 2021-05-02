from base.point import PointScene


class Algorithm:
    """Represents an algorithm to solve the problem in interactive mode."""
    method = None

    def __init__(self, scene):
        self.scene = scene
        self.stagesRenderMethods = []
        self.stageResults = []
    
    def refresh(self):
        self.stageResults = list(self.method(self.scene.point_model.points))

    def changeSceneState(self, stage_index):
        self.refresh()
        self.scene.clear()
        self.stagesRenderMethods[stage_index]()

    def setScenePoints(self):
        for i in range(self.scene.point_model.rowCount()):
            self.addItem(self.scene.graphicsItemClass(self.scene.point_model, self, i))


class AlgorithmScene(PointScene):
    """A point scene that changes according to algorithm's input changes."""
    algorithmClass = Algorithm
    stageIndex = 0
    
    def __init__(self, point_model):
        super().__init__(point_model)
        self.algorithm = self.algorithmClass()
    
    def refresh(self):
        self.algorithm.changeSceneState(self.stageIndex)
