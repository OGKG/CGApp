from base.algorithm import AlgorithmLayout
from algo.quickhull import QuickhullAlgorithm, QuickhullLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QGraphicsView, QHBoxLayout, QListView, QWidget
from base.point import PointListModel, PointScene
from base.graphics_view import GraphicsView
from algo.hull import JarvisPointScene, GrahamPointScene
from algo.loci import LociPointScene

            

class Main(QWidget):
    def __init__(self):
        super().__init__()
        model = PointListModel()
        layout = QuickhullLayout(model)
        self.setLayout(layout)


def main():
    app = QApplication([])
    app.setApplicationName("CGApp")
    main = Main()
    main.show()
    app.exec_()

if __name__ == "__main__":
    main()