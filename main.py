from PyQt5.QtWidgets import QApplication, QToolBar, QWidget
from algo.kd_tree import KdTreeLayout, KdTreePointListModel
from algo.quickhull import QuickhullLayout
from base.point import PointListModel


class Main(QWidget):
    layoutClasses = [KdTreeLayout, QuickhullLayout]

    def __init__(self):
        super().__init__()
        toolbar = QToolBar()
        toolbar.addAction("Метод")

        model = KdTreePointListModel()
        layout = KdTreeLayout(model)
        self.setLayout(layout)


def main():
    app = QApplication([])
    app.setApplicationName("CGApp")
    main = Main()
    main.show()
    app.exec_()

if __name__ == "__main__":
    main()