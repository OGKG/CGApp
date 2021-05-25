from base.text import GraphicsTextItem
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPen, QPolygonF
from PyQt5.QtWidgets import QGraphicsLineItem, QGraphicsTextItem
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
            text = GraphicsTextItem(str(i+1))
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
    
    def refresh(self):
        if not self.items():
            return
        super().refresh()
        
        for i in self.items():
            if isinstance(i, QGraphicsLineItem):
                self.removeItem(i)

        hull = self.hull_method(self.point_model.points)
        pts = hull + [hull[0]]
        for i in range(len(pts)-1):
            dx, dy = pts[i+1].x - pts[i].x, pts[i+1].y - pts[i].y
            line = QGraphicsLineItem(pts[i+1].x, pts[i+1].y, pts[i+1].x+dx, pts[i+1].y+dy)
            pen = QPen()
            pen.setStyle(Qt.DashLine)
            line.setPen(pen)
            line.setZValue(-2)
            self.addItem(line)
            h_line = QGraphicsLineItem(pts[i].x, pts[i].y, pts[i+1].x, pts[i+1].y)
            h_line.setPen(Qt.red)
            h_line.setZValue(-1)
        
        self.enumeratePoints()
        


class GrahamPointScene(HullPointScene):
    def __init__(self, point_model, view):
        super(GrahamPointScene, self).__init__(point_model, view)
        self.hull_method = graham


class QuickhullScene(HullPointScene):
    def __init__(self, point_model, view):
        super(QuickhullScene, self).__init__(point_model, view)
        self.hull_method = quickhull