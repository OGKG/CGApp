from module.models.bin_tree_node import Node
from module.models.bin_tree import KdTree
from base.task_model import TaskModel


class KdTreeTaskModel(TaskModel):
    fines = [0.25, 0.75, 1, 1]
    extra_fines = [0, 0, 0, 0]
    
    def __init__(self, points, x_range, y_range, parent=None, *args):
        super(KdTreeTaskModel, self).__init__(points, parent, *args)
        self.xList = []
        self.yList = []
        self.tree = KdTree(Node(None), x_range, y_range)
        self.ans_points = []
    
    @property
    def score(self):
        res = 3
        stages = [
            (
                self.xList,
                self.yList
            ),
            self.tree.directions,
            self.tree,
            self.ans_points
        ]

        return self.evaluate(stages, res)


