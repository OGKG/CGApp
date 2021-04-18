from main import PointGraphicsView
from point import PointListModel, PointScene
from PyQt5.QtWidgets import QHBoxLayout, QListView, QPushButton, QVBoxLayout


class TaskLayout(QHBoxLayout):
    currentStageIndex = 0
    stageLayouts = []

    def __init__(self, point_model, task_model, next_layout, parent=None):
        super(TaskLayout, self).__init__(parent)
        self.task_model = task_model
        self.point_model = point_model
        self.next_layout = next_layout

        self.stage_widgets = []
        self.vlayout_left = QVBoxLayout()
        self.vlayout_right = QVBoxLayout()
        self.vlayout_input = QVBoxLayout()
        self.hlayout = QHBoxLayout()

        self.points_list_view = QListView()
        self.points_list_view.setModel(self.point_model)
        self.vlayout_left.addWidget(self.points_list_view)

        self.point_scene = PointScene(self.point_model)
        self.points_view = PointGraphicsView()
        self.points_view.setScene(self.point_scene)
        self.vlayout_right.addWidget(self.points_view)

        self.btn_next = QPushButton("Далі")
        self.btn_next.clicked.connect(self.onBtnNextClick)
        self.vlayout_right.addWidget(self.btn_next)
    
    def onBtnNextClick(self):
        pass
