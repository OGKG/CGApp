from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPolygonF
from PyQt5.QtWidgets import QGraphicsTextItem
from base.point import PointScene
from base.polygon import PolygonGraphicsItem
from module.algo.jarvis import jarvis
from module.algo.graham import graham
from module.algo.quickhull import quickhull, quickhull_gen


class HullPointScene(PointScene):
    def __init__(self, point_model, view):
        super(HullPointScene, self).__init__(point_model, view)
        self.hull_method = None
        self.polygon = PolygonGraphicsItem([])
        self.polygon.setZValue(-1)
        self.addItem(self.polygon)
        self.textFields = []

    def refresh(self):
        self.clearTextFields()
        self.enumeratePoints()
        self.polygon.setPolygon(
            QPolygonF(
                (QPointF(*point.coords) for point in self.hull_method(self.point_model.points))
            )
        )
    
    def enumeratePoints(self):
        hull = self.hull_method(self.point_model.points)
        for i in range(len(hull)):
            text = QGraphicsTextItem(str(i+1))
            text.moveBy(*hull[i].coords)
            text.setZValue(-2)
            self.textFields.append(text)
            self.addItem(text)
    
    def clearTextFields(self):
        for textField in self.textFields:
            self.removeItem(textField)
        self.textFields = []


class JarvisPointScene(HullPointScene):
    def __init__(self, point_model, view):
        super(JarvisPointScene, self).__init__(point_model, view)
        self.hull_method = jarvis


class GrahamPointScene(HullPointScene):
    def __init__(self, point_model, view):
        super(GrahamPointScene, self).__init__(point_model, view)
        self.hull_method = graham


class QuickhullScene(HullPointScene):
    def __init__(self, point_model, view):
        super(QuickhullScene, self).__init__(point_model, view)
        self.hull_method = quickhull