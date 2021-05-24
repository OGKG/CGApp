from base.algorithm import Algorithm


class GrahamAlgorithm(Algorithm):
    def __init__(self, view, extraViews=[]):
        super().__init__(view, extraViews=extraViews)