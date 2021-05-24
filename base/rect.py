'''
    https://stackoverflow.com/a/34442054
'''

from enum import Enum
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QBrush, QPainterPath, QPainter, QColor, QPen, QPixmap
from PyQt5.QtWidgets import QGraphicsRectItem, QApplication, QGraphicsView, QGraphicsScene, QGraphicsItem

class Handle(Enum):
    TopLeft = 1
    TopMiddle = 2
    TopRight = 3
    MiddleLeft = 4
    MiddleRight = 5
    BottomLeft = 6
    BottomMiddle = 7
    BottomRight = 8

class RectGraphicsItem(QGraphicsRectItem):
    handleSize = +8.0
    handleSpace = -4.0

    handleCursors = {
        Handle.TopLeft: Qt.SizeBDiagCursor,
        Handle.TopMiddle: Qt.SizeVerCursor,
        Handle.TopRight: Qt.SizeFDiagCursor,
        Handle.MiddleLeft: Qt.SizeHorCursor,
        Handle.MiddleRight: Qt.SizeHorCursor,
        Handle.BottomLeft: Qt.SizeFDiagCursor,
        Handle.BottomMiddle: Qt.SizeVerCursor,
        Handle.BottomRight: Qt.SizeBDiagCursor,
    }

    def __init__(self, x, y, width, height, point_model, scene=None):
        """
        Initialize the shape.
        """
        super().__init__(x, y, width, height)
        self.pointModel = point_model
        self.scene = scene
        self.handles = {}
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.updateHandlesPos()
        self.setZValue(-0.5)

    def isCursorInMoveAllowedArea(self, x, y):
        width, height = self.boundingRect().width(), self.boundingRect().height()
        dx, dy = 0.1 * width, 0.1 * height

        return (
            0 < x < width
            and (0 < y < dy or height - dy < y < height)
            or 0 < y < height
            and (0 < x < dx or width - dx < x < width)
        )

    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        handle = self.handleAt(moveEvent.pos())
        cursor = Qt.OpenHandCursor if handle is None else self.handleCursors[handle]
        if self.isCursorInMoveAllowedArea(moveEvent.pos().x(), moveEvent.pos().y()):
            cursor = Qt.SizeAllCursor
        self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(Qt.OpenHandCursor)
        super().hoverLeaveEvent(moveEvent)

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()

        if not self.isCursorInMoveAllowedArea(mouseEvent.pos().x(), mouseEvent.pos().y()):
            self.setFlag(QGraphicsItem.ItemIsMovable, False)
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.handleSelected:
            self.interactiveResize(mouseEvent.pos())
        elif self.isCursorInMoveAllowedArea(mouseEvent.pos().x(), mouseEvent.pos().y()):
            self.setCursor(Qt.ClosedHandCursor)
            super().mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        super().mouseReleaseEvent(mouseEvent)
        self.setCursor(Qt.OpenHandCursor)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()

    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.handleSize + self.handleSpace
        return self.rect().adjusted(-o, -o, o, o)

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handleSize
        b = self.boundingRect()
        self.handles[Handle.TopLeft] = QRectF(b.left(), b.top(), s, s)
        self.handles[Handle.TopMiddle] = QRectF(b.center().x()-s/2, b.top(), s, s)
        self.handles[Handle.TopRight] = QRectF(b.right()-s, b.top(), s, s)
        self.handles[Handle.MiddleLeft] = QRectF(b.left(), b.center().y()-s/2, s, s)
        self.handles[Handle.MiddleRight] = QRectF(b.right()-s, b.center().y()-s/2, s, s)
        self.handles[Handle.BottomLeft] = QRectF(b.left(), b.bottom()-s, s, s)
        self.handles[Handle.BottomMiddle] = QRectF(b.center().x()-s/2, b.bottom()-s, s, s)
        self.handles[Handle.BottomRight] = QRectF(b.right()-s, b.bottom()-s, s, s)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        offset = self.handleSize + self.handleSpace
        boundingRect = self.boundingRect()
        rect = self.rect()
        diff = QPointF(0, 0)

        self.prepareGeometryChange()

        if self.handleSelected == Handle.TopLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX-fromX)
            diff.setY(toY-fromY)
            boundingRect.setLeft(toX)
            boundingRect.setTop(toY)
            rect.setLeft(boundingRect.left()+offset)
            rect.setTop(boundingRect.top()+offset)
            self.setRect(rect)

        elif self.handleSelected == Handle.TopMiddle:

            fromY = self.mousePressRect.top()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY-fromY)
            boundingRect.setTop(toY)
            rect.setTop(boundingRect.top()+offset)
            self.setRect(rect)

        elif self.handleSelected == Handle.TopRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.top()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX-fromX)
            diff.setY(toY-fromY)
            boundingRect.setRight(toX)
            boundingRect.setTop(toY)
            rect.setRight(boundingRect.right()-offset)
            rect.setTop(boundingRect.top()+offset)
            self.setRect(rect)

        elif self.handleSelected == Handle.MiddleLeft:

            fromX = self.mousePressRect.left()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX-fromX)
            boundingRect.setLeft(toX)
            rect.setLeft(boundingRect.left()+offset)
            self.setRect(rect)

        elif self.handleSelected == Handle.MiddleRight:
            fromX = self.mousePressRect.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX-fromX)
            boundingRect.setRight(toX)
            rect.setRight(boundingRect.right()-offset)
            self.setRect(rect)

        elif self.handleSelected == Handle.BottomLeft:

            fromX = self.mousePressRect.left()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX-fromX)
            diff.setY(toY-fromY)
            boundingRect.setLeft(toX)
            boundingRect.setBottom(toY)
            rect.setLeft(boundingRect.left()+offset)
            rect.setBottom(boundingRect.bottom()-offset)
            self.setRect(rect)

        elif self.handleSelected == Handle.BottomMiddle:

            fromY = self.mousePressRect.bottom()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY-fromY)
            boundingRect.setBottom(toY)
            rect.setBottom(boundingRect.bottom()-offset)
            self.setRect(rect)

        elif self.handleSelected == Handle.BottomRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX-fromX)
            diff.setY(toY-fromY)
            boundingRect.setRight(toX)
            boundingRect.setBottom(toY)
            rect.setRight(boundingRect.right()-offset)
            rect.setBottom(boundingRect.bottom()-offset)
            self.setRect(rect)

        self.updateHandlesPos()

        self.pointModel.xRange = [self.x(), self.x() + self.boundingRect().width()]
        self.pointModel.yRange = [self.y(), self.y() + self.boundingRect().height()]

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addRect(shape)
        return path

    def paint(self, painter, option, widget=None):
        """
        Paint the node in the graphic view.
        """
        pen = QPen()
        pen.setColor(Qt.blue)
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        painter.drawRect(self.rect())

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.white)
        painter.setPen(QPen(QColor(0, 0, 0, 255), 1.0, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        for handle, rect in self.handles.items():
            if self.handleSelected is None or handle == self.handleSelected:
                painter.drawRect(rect)