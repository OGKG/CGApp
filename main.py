from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QGraphicsView, QHBoxLayout, QListView, QWidget
from base.point import PointListModel, PointScene
from module.models.point import Point


class PointGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(PointGraphicsView, self).__init__(parent)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def wheelEvent(self, event):
        factor = 0.8
        if event.angleDelta().y() > 0:
            self.scale(1/factor, 1/factor)
        else:
            self.scale(factor, factor)
            

class Main(QWidget):
    def __init__(self):
        super().__init__()
        model = PointListModel([Point(1,1), Point(100,100)])
        listView = QListView()
        listView.setModel(model)

        layout = QHBoxLayout()
        layout.addWidget(listView)

        view = PointGraphicsView()
        view.setScene(PointScene(model))
        layout.addWidget(view)
        self.setLayout(layout)


def main():
    app = QApplication([])
    main = Main()
    main.show()
    app.exec_()

if __name__ == "__main__":
    main()