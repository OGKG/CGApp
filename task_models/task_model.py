from PyQt5.QtCore import QAbstractListModel


class TaskModel(QAbstractListModel):
    def __init__(self, points, parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)
        self.points = points
        self.stages = []
        self.correct_stages = []
        self.fines = []
        self.extra_fines = []
    
    @property
    def score(self):
        pass

    def evaluate(self, stages, res):
        for i in range(len(stages)):
            if stages[i] != self.correct_stages[i]:
                res -= self.fines[i]
                
                if self.extra_fines[i] > 0 and sum(x != y for x, y in zip(stages[i], self.correct_stages[i])) > 1:
                    res -= self.extra_fines[i]
        
        return res