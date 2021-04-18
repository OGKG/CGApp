from operator import imod
from PyQt5.QtWidgets import QApplication, QFrame, QHBoxLayout, QWidget
from module.models.point import Point
from task_models.kd_tree_task_model import KdTreeTaskModel
from task_layout.kd_tree_task_layout import KdTreeTaskLayout
from point import PointListModel

class Main(QWidget):
    def __init__(self):
        super().__init__()
        points = [
            Point(1, 9),
            Point(2, 3),
            Point(3, 6),
            Point(5, 8),
            Point(6, 1),
            Point(8, 13),
            Point(10, 2),
            Point(12, 4),
            Point(14, 11),
            Point(15, 5),
            Point(17, 10),
        ]
        points = [Point(p.x*20, p.y*20) for p in points]
        rx = [30, 140]
        ry = [0, 80]
        point_model = PointListModel(points)
        task_model = KdTreeTaskModel(points, rx, ry)
        task_layout = KdTreeTaskLayout(point_model, task_model)
        layout = QHBoxLayout()
        frame = QFrame()
        frame.setLayout(task_layout)
        layout.addWidget(frame)
        self.setLayout(layout)
    
def main():
    app = QApplication([])
    main = Main()
    main.show()
    app.exec_()

if __name__ == "__main__":
    main()