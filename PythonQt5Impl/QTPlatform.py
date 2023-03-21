import builtins
import copy

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPixmap, QColor, QFont, QFontMetrics, QPainter, QCursor

import AssetManager, DisplayManager,  UIEventProxy


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
    def __init__(self, app, appModel, parent=None):
        super().__init__(parent)

        self.app = app
        self.appModel = appModel
        self.parent = parent

        self.listeners = {}
        self.partRegistry = {}

        self.layers = {}

        self.displayManager = DisplayManager.DisplayManager(self)

        if 'assetDir' in self.appModel:
            self.assetManager = AssetManager.AssetManager(self)
            self.fontCache = {}
        else:
            self.assetManager = parent.assetManager
            self.fontCache = parent.fontCache

        # HACK !! the following code needs refactoring...it relies on 'model' windows all having 'controllers'
        # it also assumes that a 'appModel' with no controllers is a 'layer' and inherits caches and such from its parent
        if 'controllers' in appModel:
            self.eventProxy = UIEventProxy.UIEventProxy(self)
            controllerNames = appModel['controllers']
            self.eventProxy.setControllers(controllerNames)
            self.meData = {}
        else:
            self.meData = parent.meData
            self.eventProxy = parent.eventProxy

        self.setMouseTracking(True)

    def createChild(self, appModel):
        child = QTPlatform(self.app, appModel, self)
        return child

    def getTopWindow(self):
        window = self
        while window.parent != None:
            window = window.parent
        return window

    def getPos(self):
        geo = self.geometry()
        return R(geo.x(), geo.y(), geo.width(), geo.height())

    def clearLayers(self):
        layerCopy = copy.copy(self.getTopWindow().layers)
        for layerMane in layerCopy:
            self.removeLayer(layerMane)
        print("done")

    def addLayer(self, name, me):
        topWindow = self.getTopWindow()
        window = QTPlatform(topWindow.app, me, topWindow)
        dr = self.getMEData(me, 'drawRect')
        window.setGeometry(dr.x, dr.y, dr.w, dr.h)
        window.raise_()
        window.show()
        topWindow.layers[name] = window

    def removeLayer(self, name):
        print(f' *** removeLayer {name} ***')
        topWindow = self.getTopWindow()
        if name in topWindow.layers:
            window = topWindow.layers[name]
            del topWindow.layers[name]
            window.hide()
            window.deleteLater()

    def setMEData(self, me, key, value):
        if 'id' not in me:
            me['id'] = builtins.id(me)
        id = me['id']
        if id not in self.meData:
            self.meData[id] = {}
        self.meData[id][key] = value

    def getMEData(self, me, key):
        value = self.meData[me['id']][key]
        return value

    def subscribe(self, name, listener):
        self.listeners[name] = listener

    def removeListener(self, name):
        del self.listeners[name]

    def publish(self, me, attName, oldVal, newVal):
        for listenerName in self.listeners:
            listener = self.listeners[listenerName]
            listener(self, me, attName, oldVal, newVal)

    def registerPart(self, me, partName):
        if 'partName' not in me:
            return

        partName = me['partName']
        self.partRegistry[partName] = me

    def getPart(self, partName):
        if partName in self.partRegistry:
            return self.partRegistry[partName]
        return None

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
        self.displayManager.layout(available, self.appModel)

    def paintEvent(self, event): 
        self.painter = QPainter()   # Cache for callbacks...rebderers don't need to know
        self.painter.begin(self)

        self.displayManager.drawModelElement(self.appModel)
        
        self.painter.end()
        self.painter = None

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
        self.painter.setFont(font)
        self.painter.setPen(QColor(textColor))

        r = QRect(x, y, 1000, 1000)
        self.\
            painter.drawText(r, Qt.AlignTop | Qt.AlignLeft,  text)

    def drawIcon(self, x, y, image):
        self.painter.drawPixmap(x, y, image)

    def drawImage(self, dx, dy, dw, dh, image, sx, sy, sw, sh):
        dstRect = QRect(dx, dy, dw, dh)
        srcRect = QRect(sx, sy, sw, sh)
        self.painter.drawPixmap(srcRect, image, dstRect)

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
        print('@@@ Enter Widget @@@')
        self.eventProxy.enterWidget(self, event.pos().x(), event.pos().y())

    def leaveEvent(self, event):
        print('!!! Leave Widget !!!')
        self.eventProxy.leaveWidget(self)

    def mouseMoveEvent(self, event):
        self.eventProxy.mouseMove(self, event.x(), event.y())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
           self.eventProxy.mousePressEvent(self, "left")
        if event.button() == Qt.RightButton:
           self.eventProxy.mousePressEvent(self, "right")
        if event.button() == Qt.MidButton:
           self.eventProxy.mousePressEvent(self, "middle")

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
           self.eventProxy.mouseReleaseEvent(self, "left")
        if event.button() == Qt.RightButton:
           self.eventProxy.mouseReleaseEvent(self, "right")
        if event.button() == Qt.MidButton:
           self.eventProxy.mouseReleaseEvent(self, "middle")

