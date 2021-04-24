from module.algo.quickhull import quickhull_gen
from module.models.bin_tree_node import Node
from module.models.bin_tree import BinTree
from base.task_model import TaskModel


class QuickhullTaskModel(TaskModel):
    fines = [0.25, 0.25, 0.25, 0.25, 1]
    extra_fines = [0, 0.25, 0, 0, 0]
    
    def __init__(self, points, parent=None, *args):
        super(QuickhullTaskModel, self).__init__(points, parent, *args)
        self.res = 2
        self.min = 0
        self.max = 0
        self.s1 = []
        self.s2 = []
        self.h_list = []
        self.tree = BinTree(Node([]))
        self.hull = []
        self.correct_stages = list(quickhull_gen(points))
    
    @property
    def score(self):
        res = 2
        stages = [
            (
                self.min,
                self.max,
                self.s1,
                self.s2
            ),
            self.h_list,
            self.tree.to_list(),
            self.tree.leaves,
            self.hull
        ]

        return self.evaluate(stages, res)
