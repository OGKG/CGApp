from module.models.bin_tree_node import Node, NodeWithParent
from module.models.bin_tree import ChainsBinTree
from module.models.graph import OrientedGraph
from .task_model import TaskModel


class ChainTaskModel(TaskModel):
    fines = [0.25, 0.25, 1, 1]
    extra_fines = [0, 0, 0, 0]
    
    def __init__(self, points, x_range, y_range, parent=None, *args):
        super().__init__(points, parent, *args)
        self.yList = []
        self.struct = {}
        self.In = []
        self.Out = []
        self.graph = OrientedGraph()
        self.tree = ChainsBinTree(NodeWithParent([]))
        self.ans_chains = []
    
    @property
    def score(self):
        res = 3
        stages = [
            self.yList,
            self.In,
            self.Out,
            self.struct,
            self.graph.edges,
            self.tree,
            self.ans_chains
        ]

        return self.evaluate(stages, res)

