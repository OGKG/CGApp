from PyQt5.QtWidgets import QLineEdit
from .task_layout import TaskLayout


class QuickhullTaskLayout(TaskLayout):
    def __init__(self, points, task_model, parent=None):
        super(QuickhullTaskLayout, self).__init__(points, task_model, parent)
        
