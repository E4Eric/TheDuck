import copy

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QColor, QFont, QFontMetrics, QPainter, QCursor
from PyQt5.QtWidgets import QLabel


class R():
    def __init__(self, x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def offset(self, dx, dy):
        offsetRect = copy.copy(self)
        offsetRect.x += dx
        offsetRect.y += dy
        return offsetRect

    def __str__(self):
        return f'({self.x},{self.y},{self.w},{self.h})'

class QTPlatform(QtWidgets.QWidget):
    def __init__(self, ctx, me, parent):
        super().__init__(parent)

        self.ctx = ctx
        self.me = me
        self.parent = parent

        if parent == None:
            self.fontCache = {}
            self.setGeometry(100, 100, 1200, 750)
            self.layers = {}
        else:
            # self.setWindowFlags(
            #     self.windowFlags() |
            #     QtCore.Qt.FramelessWindowHint |
            #     QtCore.Qt.WindowStaysOnTopHint
            # )
            dr = self.ctx.getMEData(me, 'drawRect')
            self.setGeometry(dr.x, dr.y, dr.w, dr.h)

        # delegate to the runtime context so multiple instances can use the same painting code
        self.ctx.painter = None
        self.layers = {}

        self.setMouseTracking(True)

    def addLayer(self, name, me):
        layer = QTPlatform(self.ctx, me, self)
        layer.raise_()
        layer.show()
        self.layers[name] = layer

    def removeLayer(self, name):
        if name in self.layers:
            label = self.layers[name]
            label.hide()
            label.deleteLater()
            self.ctx.app.processEvents()
            del self.layers[name]

            self.update()
            self.setFocus()
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            pass
        elif event.key() == Qt.Key_Return:
            pass


    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Escape:
            pass
        elif event.key() == Qt.Key_Return:
            pass

    def resizeEvent(self, event):
        size = event.size()
        available = R(0,0, size.width(), size.height())
        self.ctx.displayManager.layout(available, self.me)

    def paintEvent(self, event): 
        self.ctx.painter = QPainter()   # Cache for callbacks...rebderers don't need to know
        self.ctx.painter.begin(self)

        self.ctx.displayManager.drawModelElement(self.me)
        
        self.ctx.painter.end()
        self.ctx.painter = None

    def forceUpdate(self, x, y, w, h):
        self.update()

    def setTransparentColor(self, pixmap, r, g, b):
        # Create a mask from the pixmap that matches the color you want to make transparent
        mask = pixmap.createMaskFromColor(QColor(r, g, b))

        # Set the mask on the pixmap
        pixmap.setMask(mask)

    def loadImage(self, path):
        return QPixmap(path)

    def getImageWidth(self, pixmap):
        return pixmap.rect().width()

    def getImageHeight(self, pixmap):
        return pixmap.rect().height()


    def getFontFromSpec(self, fontSpec):
        if fontSpec in self.fontCache:
            font, palette = self.fontCache[fontSpec]
            return font

        font = QFont()

        # set transparent background in the palette
        font.setStyleHint(QFont.SansSerif)  # default style hint

        textColor = QColor(0,0,0,)
        for attr, value in self.parseStyleSheet(fontSpec):
            if attr == "font-family":
                font.setFamily(value)
            elif attr == "color":
                textColor = QColor(value)
            elif attr == "font-size":
                font.setPointSize(int(value))
            elif attr == "font-weight":
                font.setWeight(int(value))
            elif attr == "font-style":
                if value == "italic":
                    font.setItalic(True)
                if value == "bold":
                    font.setBold(True)

        self.fontCache[fontSpec] = (font, textColor)
        return font

    def parseStyleSheet(self, fontSpec: str):
        """
        Parse a style sheet string into a list of (property, value) tuples.
        """
        properties = []
        for rule in fontSpec.split(";"):
            if not rule:
                continue
            attr, value = rule.split(":")
            properties.append((attr.strip(), value.strip()))
        return properties

    def getTextWidth(self, text, fontSpec):
        font = self.getFontFromSpec(fontSpec)
        font_metrics = QFontMetrics(font)
        bounding_rect = font_metrics.boundingRect(text)
        return bounding_rect.width()

    def getTextHeight(self, text, fontSpec):
        font = self.getFontFromSpec(fontSpec)
        font_metrics = QFontMetrics(font)
        bounding_rect = font_metrics.boundingRect(text)
        return bounding_rect.height()

    def drawText(self, x, y, text, fontSpec):
        font, textColor = self.fontCache[fontSpec]
        self.ctx.painter.setFont(font)
        self.ctx.painter.setPen(QColor(textColor))

        r = QRect(x, y, 1000, 1000)
        self.ctx.painter.drawText(r, Qt.AlignTop | Qt.AlignLeft,  text)

    def drawIcon(self, x, y, image):
        self.ctx.painter.drawPixmap(x, y, image)

    def drawImage(self, dx, dy, dw, dh, image, sx, sy, sw, sh):
        dstRect = QRect(dx, dy, dw, dh)
        srcRect = QRect(sx, sy, sw, sh)
        self.ctx.painter.drawPixmap(srcRect, image, dstRect)

    def crop(self, srcMap, x, y, w, h):
        return srcMap.copy(QRect(x, y, w, h))

    def setPointer(self, pointerName):
        if pointerName == 'Move':
            self.setCursor(QCursor(Qt.PointingHandCursor))
        elif pointerName == 'NS':
            self.setCursor(QCursor(Qt.SizeVerCursor))
        elif pointerName == 'EW':
            self.setCursor(QCursor(Qt.SizeHorCursor))
        else:
            self.setCursor(QCursor(Qt.ArrowCursor))

    def enterEvent(self, event):
        self.ctx.eventProxy.enterWidget(event.pos().x(), event.pos().y())
    def leaveEvent(self, event):
        self.ctx.eventProxy.leaveWidget(0, 0)

    def mouseMoveEvent(self, event):
        self.ctx.eventProxy.mouseMove(event.x(), event.y())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
           self.ctx.eventProxy.mousePressEvent("left")
        if event.button() == Qt.RightButton:
           self.ctx.eventProxy.mousePressEvent("right")
        if event.button() == Qt.MidButton:
           self.ctx.eventProxy.mousePressEvent("middle")

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
           self.ctx.eventProxy.mouseReleaseEvent("left")
        if event.button() == Qt.RightButton:
           self.ctx.eventProxy.mouseReleaseEvent("right")
        if event.button() == Qt.MidButton:
           self.ctx.eventProxy.mouseReleaseEvent("middle")

