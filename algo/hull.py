from base.algo_scene import AlgorithmPointScene
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF
from base.point import PointScene
from base.polygon import PolygonGraphicsItem
from module.algo.jarvis import jarvis
from module.algo.graham import graham
from module.algo.quickhull import quickhull_gen


class HullPointScene(PointScene):
    def __init__(self, point_model):
        super(HullPointScene, self).__init__(point_model)
        self.hull_method = None
        self.polygon = PolygonGraphicsItem([])
        self.polygon.setZValue(-1)
        self.addItem(self.polygon)


    def refresh(self):
        self.polygon.setPolygon(
            QPolygonF(
                (QPointF(*point.coords) for point in self.hull_method(self.point_model.points))
            )
        )


class JarvisPointScene(HullPointScene):
    def __init__(self, point_model):
        super(JarvisPointScene, self).__init__(point_model)
        self.hull_method = jarvis


class GrahamPointScene(HullPointScene):
    def __init__(self, point_model):
        super(GrahamPointScene, self).__init__(point_model)
        self.hull_method = graham


