from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QTextDocument
from base.text import GraphicsTextItem
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsScene, QGraphicsTextItem

class BinTreeNodeGraphicsItem(QGraphicsEllipseItem):
    rad = 20
    textSize = 10

    def __init__(self, text, content=None, depth=0):
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


class BinTreeSquareNodeGraphicsItem(QGraphicsRectItem):
    width = 40
    textSize = 10

    def __init__(self, text, content=None, depth=0):
        self.text = text
        self.content = content
        self.depth = depth
        super().__init__(-self.width/2, -self.width/2, self.width, self.width)
        self.setToolTip(content)


class BinTreeScene(QGraphicsScene):
    rad = BinTreeNodeGraphicsItem.rad

    def __init__(self, tree, width, height):
        QGraphicsScene.__init__(self)
        rect = QGraphicsRectItem(0, 0, width+100, height)
        rect.setPen(Qt.white)
        self.addItem(rect)
        self.tree = tree
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

    def constructTree(self):
        pass
