from module.models.point import Point
from PyQt5.QtWidgets import QApplication, QGraphicsView, QHBoxLayout, QListView, QWidget
from point import PointListModel, PointScene


class Main(QWidget):
    def __init__(self):
        super().__init__()
        model = PointListModel([Point(1,1), Point(100,100)])
        listView = QListView()
        listView.setModel(model)

        layout = QHBoxLayout()
        layout.addWidget(listView)
        scene = PointScene(model)
        view = QGraphicsView()
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