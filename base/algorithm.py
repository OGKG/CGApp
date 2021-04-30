class Algorithm:
    method = None

    def __init__(self, scene):
        self.scene = scene
        self.stagesRenderMethods = []
        self.stageResults = []
    
    def changeSceneState(self, stage_index):
        self.stagesRenderMethods[stage_index]()

    def setScenePoints(self):
        for i in range(self.point_model.rowCount()):
            self.addItem(self.scene.graphicsItemClass(self.point_model, self, i))