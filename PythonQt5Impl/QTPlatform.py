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

        # HACK !! For now assume having 'aasetDir' means you're showing a completely new model
        if 'assetDir' in self.appModel:
            self.type = "Model"
            self.meData = {}
            self.partRegistry = {}
            self.layers = {}
            self.fontCache = {}

            self.assetManager = AssetManager.AssetManager(self)
            self.displayManager = DisplayManager.DisplayManager(self)
            self.eventProxy = UIEventProxy.UIEventProxy(self)
        else:
            self.type = "Layer"
            # Inherited attributes
            self.meData = parent.meData   # The model window 'owns' the models elements
            self.partRegistry = self.parent.partRegistry
            self.layers = parent.layers   # All layers belong to the parent
            self.fontCache = parent.fontCache
            self.assetManager = parent.assetManager

            self.displayManager = DisplayManager.DisplayManager(self)
            self.eventProxy = parent.eventProxy

        if 'controllers' in appModel:
            controllerNames = appModel['controllers']
            self.eventProxy.setControllers(controllerNames)

        self.setMouseTracking(True)

    def createChild(self, appModel):
        child = QTPlatform(self.app, appModel, self)
        return child

    def setAppModel(self, newAppModel):
        modelRect = self.getMEData(self.appModel, 'drawRect')

        # Clear out old widgets
        for partName in self.partRegistry:
            part = self.getPart(partName)
            partWidget = self.getMEData(part, 'qtWidget')
            print(f'Removing Widget {partName}')
            partWidget.hide()
            partWidget.deleteLater()
        self.partRegistry = {}

        self.appModel = newAppModel
        self.setMEData(newAppModel, 'drawRect', modelRect)

        # update assets if necessary
        if 'assetDir' in self.appModel:
            self.assetManager = AssetManager.AssetManager(self)

        self.displayManager.refresh()

        print('OK')


    def getModelWindow(self):
        window = self
        while window.type != 'Model':
            window = window.parent
        return window

    def getPos(self):
        geo = self.geometry()
        return R(geo.x(), geo.y(), geo.width(), geo.height())

    def clearLayers(self):
        layerCopy = copy.copy(self.getModelWindow().layers)
        for layerName in layerCopy:
            self.removeLayer(layerName)

    def addLayer(self, name, me):
        window = QTPlatform(self.app, me, self.getModelWindow())
        dr = self.getMEData(me, 'drawRect')
        window.setGeometry(dr.x, dr.y, dr.w, dr.h)
        window.raise_()
        window.show()
        self.getModelWindow().layers[name] = window

    def removeLayer(self, name):
        if name in self.layers:
            window = self.getModelWindow().layers[name]
            del self.getModelWindow().layers[name]
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
        if 'id' not in me:
            return None
        if  key not in self.meData[me['id']]:
            return None

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

    def setTransparentColor(self, pixmap, x, y):
        # Create a mask from the pixmap that matches the color you want to make transparent
        img = pixmap.toImage()
        color = img.pixelColor(x, y)
        mask = pixmap.createMaskFromColor(color)
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
        self.eventProxy.enterWidget(self, event.pos().x(), event.pos().y())

    def leaveEvent(self, event):
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

