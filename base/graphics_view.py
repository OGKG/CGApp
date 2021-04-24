from PyQt5.QtWidgets import QGraphicsView


class GraphicsView(QGraphicsView):
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
        else:
            factor = 0.8
        
        self.scale(factor, factor)