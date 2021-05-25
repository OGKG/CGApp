from algo.jarvis import JarvisLayout
from algo.graham import GrahamLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QApplication, QHBoxLayout, QMenu, QMenuBar, QToolBar, QVBoxLayout, QWidget
from algo.kd_tree import KdTreeLayout, KdTreePointListModel
from algo.quickhull import QuickhullLayout
from base.point import PointListModel


class Main(QWidget):

    def __init__(self):
        super().__init__()
        self.menuBar = QMenuBar(self)
        methodMenu = self.menuBar.addMenu('Метод')
        
        kdTreeAction = QAction('k-D дерева', self)
        jarvisAction = QAction('Джарвіса', self)
        grahamAction = QAction('Грехема', self)
        quickhullAction = QAction('Швидкобол', self)
        kdTreeAction.triggered.connect(self.startKdTreeAction)
        jarvisAction.triggered.connect(self.startJarvisAction)
        grahamAction.triggered.connect(self.startGrahamAction)
        quickhullAction.triggered.connect(self.startQuickhullAction)

        methodActions = [
            kdTreeAction,
            jarvisAction,
            grahamAction,
            quickhullAction
        ]
        methodMenu.addActions(methodActions)

        self.mainLayout = QHBoxLayout()
        self.layouts = [
            KdTreeLayout(KdTreePointListModel()),
            JarvisLayout(PointListModel()),
            GrahamLayout(PointListModel()),
            QuickhullLayout(PointListModel())
        ]
        self.mainLayout.setMenuBar(self.menuBar)
        self.layoutWidgets = []
        for l in self.layouts:
            w = QWidget()
            w.setLayout(l)
            self.layoutWidgets.append(w)
            self.mainLayout.addWidget(w)

        self.setLayout(self.mainLayout)
        self.startKdTreeAction()

    def startKdTreeAction(self):
        self.layoutWidgets[0].setVisible(True)
        self.layoutWidgets[1].setVisible(False)
        self.layoutWidgets[2].setVisible(False)
        self.layoutWidgets[3].setVisible(False)
        
    def startJarvisAction(self):
        self.layoutWidgets[0].setVisible(False)
        self.layoutWidgets[1].setVisible(True)
        self.layoutWidgets[2].setVisible(False)
        self.layoutWidgets[3].setVisible(False)

    def startGrahamAction(self):
        self.layoutWidgets[0].setVisible(False)
        self.layoutWidgets[1].setVisible(False)
        self.layoutWidgets[2].setVisible(True)
        self.layoutWidgets[3].setVisible(False)

    def startQuickhullAction(self):
        self.layoutWidgets[0].setVisible(False)
        self.layoutWidgets[1].setVisible(False)
        self.layoutWidgets[2].setVisible(False)
        self.layoutWidgets[3].setVisible(True)
        

def main():
    app = QApplication([])
    app.setApplicationName("CGApp")
    main = Main()
    main.showMaximized()
    app.exec_()

if __name__ == "__main__":
    main()