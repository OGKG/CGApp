from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QGraphicsView, QHBoxLayout, QListView, QWidget
from base.point import PointListModel
from algo.hull import JarvisPointScene, GrahamPointScene
from algo.loci import LociPointScene

            

class Main(QWidget):
    def __init__(self):
        super().__init__()
        model = PointListModel()
        listView = QListView()
        listView.setModel(model)

        layout = QHBoxLayout()
        layout.addWidget(listView)

        view = PointGraphicsView()
        view.setScene(LociPointScene(model))
        layout.addWidget(view)
        self.setLayout(layout)


def main():
    app = QApplication([])
    main = Main()
    main.show()
    app.exec_()

if __name__ == "__main__":
    main()