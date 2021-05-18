from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QTextDocument
from base.text import GraphicsTextItem
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsScene, QGraphicsTextItem

class BinTreeNodeGraphicsItem(QGraphicsEllipseItem):
    rad = 20
    textSize = 10

    def __init__(self, text, content, depth=0):
        """
            Initializes a binary tree node as the circle.
            Text is shown inside the circle,
            content is revealed in the tooltip on mouse hover.
        """
        self.text = text
        self.content = content
        self.depth = depth
        super().__init__(-self.rad, -self.rad, 2*self.rad, 2*self.rad)
        self.setToolTip(content)


class BinTreeScene(QGraphicsScene):
    rad = BinTreeNodeGraphicsItem.rad

    def __init__(self, tree, point_model, width, height):
        QGraphicsScene.__init__(self)
        rect = QGraphicsRectItem(0, 0, width+100, height)
        rect.setPen(Qt.white)
        self.addItem(rect)
        self.tree = tree
        self.point_model = point_model
        self.constructTree()
    
    def paint(self, painter, option, widget):
        font = painter.font()
        font.setPointSize(self.textSize)
        painter.setFont(font)
        painter.translate(QPointF(self.pos().x(), self.pos().y()))
        td = QTextDocument()
        td.setHtml(self.text)
        td.drawContents(painter)
        super().paint(painter, option, widget)

    def constructTree(self, depth_list):
        pass

    def nodeText():
        pass

