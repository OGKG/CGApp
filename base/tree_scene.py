from PyQt5.QtWidgets import QGraphicsScene

class TreeScene(QGraphicsScene):
    def __init__(self, tree_model):
        self.tree_model = tree_model