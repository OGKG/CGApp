


from module.algo.jarvis import jarvis
from algo.hull import JarvisPointScene
from base.algorithm import Algorithm, AlgorithmLayout
from base.point import PointScene


class JarvisAlgorithm(Algorithm):
    def __init__(self, view, extraViews=[]):
        super().__init__(view, extraViews)
        self.stagesRenderMethods.extend(
            [
                self.renderStage0,
                self.renderStage1
            ]
        )
    
    @staticmethod
    def solve(points):
        return jarvis(points)

    def renderStage0(self):
        self.view.stageLabel.setText("Етап 0. Умова")
        self.scene = PointScene(self.point_model, self.view)
        self.view.setScene(self.scene)
        self.setScenePoints()
    
    def renderStage1(self):
        self.view.stageLabel.setText("Етап 1. Результат")
        self.scene = JarvisPointScene(self.point_model, self.view)
        self.view.setScene(self.scene)
        self.setScenePoints()
        self.scene.refresh()


class JarvisLayout(AlgorithmLayout):
    algorithmName = "Метод Джарвіса"
    stageCount = 2
    algorithmClass = JarvisAlgorithm
    initSceneClass = PointScene
