from task_scene.kd_tree_scene import KdTreePartitionScene, KdTreeScene
from PyQt5.QtWidgets import QGraphicsView, QLineEdit
from .task_layout import TaskLayout


class KdTreeTaskLayout(TaskLayout):
    def __init__(self, point_model, task_model, parent=None):
        super(KdTreeTaskLayout, self).__init__(point_model, task_model, None, parent)
        self.xListInput = QLineEdit()
        self.yListInput = QLineEdit()
        
        self.partitionScene = KdTreePartitionScene(point_model, task_model)
        self.treeScene = KdTreeScene(point_model, task_model)
        
        graphics_view = KdTreeGraphicsView()
        graphics_view.setScene(self.partitionScene)
        self.vlayout_input.addWidget(graphics_view)
        self.vlayout_left.addLayout(self.vlayout_input)
        self.stageLayouts = []

        self.addLayout(self.vlayout_left)
        self.addLayout(self.vlayout_right)

        
class KdTreeGraphicsView(QGraphicsView):
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
        else:
            factor = 0.8
        
        self.scale(factor, factor)