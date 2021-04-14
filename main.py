from PyQt5.QtGui import QPainter
from module.models.point import Point
from module.algo.jarvis import jarvis
from PyQt5.QtWidgets import QApplication, QGraphicsView, QHBoxLayout, QListView, QVBoxLayout, QWidget, QPushButton
from point import PointListModel, PointScene

class GraphicsView(QGraphicsView):
    def mousePressEvent(self, event):
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        return super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        return super().mouseReleaseEvent(event)
    
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
        else:
            factor = 0.8
        
        self.scale(factor, factor)
            

class Main(QWidget):
    def __init__(self):
        super().__init__()
        model = PointListModel([Point(1,1), Point(100,100)])
        listView = QListView()
        listView.setModel(model)
        
        def onClick(scene):
            scene.constructConvexHull(jarvis)

        hullButton = QPushButton("Construct convex hull")

        layout = QHBoxLayout()
        v_layout = QVBoxLayout()
        v_layout.addWidget(listView)
        scene = PointScene(model)
        
        hullButton.clicked.connect(lambda: onClick(scene))
        v_layout.addWidget(hullButton)
        layout.addLayout(v_layout)

        view = GraphicsView()
        view.setScene(scene)
        layout.addWidget(view)
        self.setLayout(layout)


def main():
    app = QApplication([])
    main = Main()
    main.show()
    app.exec_()

if __name__ == "__main__":
    main()