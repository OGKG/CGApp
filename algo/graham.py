from base.graphics_view import ExtraView
from PyQt5.QtGui import QPen, QStandardItemModel
from PyQt5.QtCore import QModelIndex, Qt
from base.text import GraphicsTextItem
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QTableView, QVBoxLayout
from base.point import PointGraphicsItem, PointScene
from module.algo.graham import graham_gen
from base.algorithm import Algorithm, AlgorithmLayout, AlgorithmScene


class GrahamAlgorithm(Algorithm):
    def __init__(self, view, extraViews=[]):
        super().__init__(view, extraViews)
        self.stagesRenderMethods.extend(
            [
                self.renderStage0,
                self.renderStage1,
                self.renderStage2
            ]
        )
        self.extraViews = []
        self.tableView = None
    
    @staticmethod
    def solve(points):
        return graham_gen(points)

    def renderStage0(self):
        self.view.stageLabel.setText("Етап 0. Умова")
        self.scene = PointScene(self.point_model, self.view)
        self.view.setScene(self.scene)
        self.setScenePoints()
        self.extraViews[0].setVisible(False)
    
    def renderStage1(self):
        self.view.stageLabel.setText("Етап 1. Обхід")
        self.scene = GrahamPointScene(self.point_model, self, self.view)
        self.view.setScene(self.scene)
        self.setScenePoints()
        self.scene.refresh()
    
    def renderStage2(self):
        pass

    def fillTable(self):
        table = self.stageResults[2]
        
        if not self.tableView:
            tableView = QTableView()
            model = QStandardItemModel(len(table), 4)
            model.setHeaderData(0, Qt.Horizontal, "Трійка")
            model.setHeaderData(1, Qt.Horizontal, "Кут")
            model.setHeaderData(2, Qt.Horizontal, "Точка")
            model.setHeaderData(3, Qt.Horizontal, "Дія над точкою")
            tableView.setModel(model)
            self.tableView = tableView
            self.tableLayout.addWidget(tableView)

        model = self.tableView.model() 

        if len(table) > model.rowCount():
            model.insertRows(model.rowCount()-1, len(table)-model.rowCount(), QModelIndex())
        if len(table) < model.rowCount():
            model.removeRows(model.rowCount()-1, model.rowCount()-len(table), QModelIndex())
        

        for row in range(model.rowCount()):
            triple = str(table[row][0][0]) +\
                "-" + str(table[row][0][1]) +\
                "-" + str(table[row][0][2])
            angle = "<π" if table[row][1] else "⩾π"
            point = table[row][2]
            action = "Додати" if table[row][1] else "Видалити"
            data = [triple, angle, point, action]

            for col in range(model.columnCount()):
                index = model.index(row, col)
                model.setData(index, data[col])
            


class GrahamPointScene(AlgorithmScene):
    table = None

    def __init__(self, point_model, algorithm, view):
        super().__init__(point_model, algorithm, view)
        self.originItem = None

    def refresh(self):
        if not self.items():
            return
        super().refresh()

        for i in filter(lambda i: isinstance(i, QGraphicsLineItem), self.items()):
            self.removeItem(i)

        for i in self.items():
            i.setBrush(Qt.blue)

        first3Coords = [p.coords for p in self.point_model.points[:3]] 
        first3Items = list(filter(lambda p: (p.x(), p.y()) in first3Coords, self.items()))

        for i in first3Items:
            i.setBrush(Qt.yellow)
        
        min_point = min(self.items(), key=lambda p: (p.y(), p.x()))
        min_point.setBrush(Qt.green)

        self.setOrigin()
        self.drawLinesFromOriginToPoints()
        self.drawEdges()
        self.enumeratePoints()
        self.algorithm.fillTable()
    
    def setOrigin(self):
        self.removeItem(self.originItem)
        origin = self.algorithm.stageResults[0]
        rad = PointGraphicsItem.rad
        origin_item = QGraphicsEllipseItem(-rad, -rad, 2*rad, 2*rad)
        origin_item.moveBy(*origin.coords)
        origin_item.setBrush(Qt.red)
        self.addItem(origin_item)
        self.originItem = origin_item

    def drawLinesFromOriginToPoints(self):
        points = self.algorithm.stageResults[1]
        for p in points:
            line = QGraphicsLineItem(self.originItem.x(), self.originItem.y(), p.x, p.y)
            pen = QPen()
            pen.setStyle(Qt.DashLine)
            line.setPen(pen)
            line.setZValue(-1)
            self.addItem(line)

    def enumeratePoints(self):
        points = list(enumerate(self.algorithm.stageResults[1], start=1))
        for p in points:
            text = GraphicsTextItem(str(p[0]))
            text.moveBy(*p[1].coords)
            self.textFields.append(text)
            self.addItem(text)

    def drawEdges(self):
        points = self.algorithm.stageResults[1]
        table = self.algorithm.stageResults[2]
        for row in table:
            p1, p2, p3 = points[row[0][0]-1], points[row[0][1]-1], points[row[0][2]-1]
            line1 = QGraphicsLineItem(*p1.coords, *p2.coords)
            line2 = QGraphicsLineItem(*p2.coords, *p3.coords)
            line1.setZValue(-2)
            line2.setZValue(-2)
            
            if row[1]:
                line1.setPen(Qt.green)
                line2.setPen(Qt.green)
            else:
                line1.setPen(Qt.red)
                line2.setPen(Qt.red)
            
            self.addItem(line1)
            self.addItem(line2)


class GrahamLayout(AlgorithmLayout):
    algorithmName = "Метод Грехема"
    stageCount = 3
    algorithmClass = GrahamAlgorithm
    initSceneClass = PointScene

    def __init__(self, point_model, parent=None):
        super().__init__(point_model, parent)
        self.algorithm.tableLayout = QVBoxLayout()
        self.viewLayout.addLayout(self.algorithm.tableLayout)

