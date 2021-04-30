from .point import PointScene
from .graphics_view import GraphicsView
from PyQt5.QtWidgets import QHBoxLayout, QListView, QPushButton, QVBoxLayout


class AlgorithmLayout(QHBoxLayout):
    def __init__(self, point_model, parent=None):
        super(AlgorithmLayout, self).__init__(parent)
        self.point_model = point_model

        self.vLayoutLeft = QVBoxLayout()
        self.vLayoutRight = QVBoxLayout()
        self.hLayout = QHBoxLayout()

        self.pointsListView = QListView()
        self.pointsListView.setModel(self.point_model)
        self.vLayoutLeft.addWidget(self.points_list_view)

        self.pointScene = PointScene(self.point_model)
        self.pointsView = GraphicsView()
        self.pointsView.setScene(self.point_scene)
        self.vLayoutLeft.addWidget(self.points_view)

        # TODO: stage buttons
