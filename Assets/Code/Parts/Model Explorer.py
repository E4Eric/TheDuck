import json
import os

from PyQt5.QtCore import Qt, QRect
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem, QIcon, QPainter, QBrush, QColor, QPalette
from PyQt5.QtWidgets import QTreeView, QWidget, QLabel


class Overlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.modelWindow = parent
        self.curME = None

        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self.mainMenuPane = None

        geo = self.modelWindow.geometry()
        self.setGeometry(0, 0, geo.width(), geo.height())
        self.show()

    def paintEvent(self, event):
        rect = QRect(0, 0, 0, 0)
        if self.curME is not None:
            dr = self.modelWindow.getMEData(self.curME, 'drawRect')
            rect = QRect(dr.x, dr.y, dr.w, dr.h)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor(0, 255, 0, 127)))
        center = rect.center()
        painter.drawEllipse(rect.x(), rect.y(), rect.width(), rect.height())

    def createModelJSONPane(self, me):
        if self.mainMenuPane is None:
            self.mainMenuPane = QLabel(self)

            # Set background color to blue
            palette = QPalette()
            palette.setColor(QPalette.Background, QColor(0, 0, 255))
            self.mainMenuPane.setPalette(palette)
            self.mainMenuPane.setAutoFillBackground(True)

            # Set style sheet to include 3-pixel margin, white border, and yellow text color
            self.mainMenuPane.setStyleSheet(
                "background-color: blue;"
                "border: 2px solid white;"
                "color: yellow;"
                "font-size: 16pt;"
                "margin: 5px;"
            )

        meJSON = json.dumps(me)
        self.mainMenuPane.setText(meJSON)

        dr = self.parent().getMEData(me, 'drawRect')

        # Adjust size to fit text
        self.mainMenuPane.adjustSize()
        self.mainMenuPane.move(dr.x, dr.y + dr.h + 10)
        self.mainMenuPane.show()

    def createMEPane(self, me):
        self.createModelJSONPane(me)

    def setModelCurME(self, newME):
        self.curME = newME
        self.createMEPane(self.curME)
        self.update()

class ModelEventHook():
    def __init__(self, modelExplorer):
        self.modelExplorer = modelExplorer

        self.curME = None

    def enter(self, window, me, x ,y):
        print("enter")
        self.modelExplorer.overlay.setModelCurME(me)

    def leave(self, window, me):
        print("leave")

    def resizeEvent(self, window, w, h):
        print("editor resized")
        self.modelExplorer.overlay.setGeometry(0, 0, w, h)

class ModelExplorer(QTreeView):
    def __init__(self, window):
        super().__init__(window)

        self.window = window
        self.appModel = window.appModel
        self.editorModel = None
        self.setAnimated(True)
        self.overlay = None

        # Tree Icons
        self.rootIcon = window.assetManager.getIconImage("Python Folder")
        self.fieldIcon = window.assetManager.getIconImage("Markdown File")
        self.pyFile = window.assetManager.getIconImage("Python File")
        self.imgFile =  window.assetManager.getIconImage("Image File")
        self.itemIcon = window.assetManager.getIconImage('Data File')
        self.assetsIcon = window.assetManager.getIconImage("Assets")
        self.folderClosed = window.assetManager.getIconImage("Folder (empty)")
        self.folderOpen = window.assetManager.getIconImage("Folder (open)")

        # create the model
        self.treeModel = QStandardItemModel()
        self.treeModel.setHorizontalHeaderLabels([self.appModel['appTitle']])
        self.setModel(self.treeModel)

        # add root item to the model
        self.root = QStandardItem(self.appModel['appname'])
        self.treeModel.appendRow(self.root)
        self.fillTree(self.appModel)

    def setCurEditorElement(self, newEditorME):
        self.curEditorME = newEditorME
    def curEditorResized(self, w, h):
        self.overlay.setGeometry(0, 0, w, h)

    def addEditorHook(self, editor):
        mve = ModelEventHook(self)
        editor.eventProxy.controllers.append(mve)

    def setEditorModel(self, editorModel):
        self.editorModel = editorModel

        part = self.window.getPart("Model Editor")
        editorWindow = self.window.getMEData(part, "qtWidget")
        editorWindow.setAppModel(self.editorModel)
        if self.overlay is not None:
            self.overlay.hide()
            self.overlay.deleteLater()
            self.overlay = None

        self.overlay = Overlay(editorWindow)
        self.addEditorHook(editorWindow)

        # re-fill the tree from the new Model
        self.treeModel.clear()
        self.root = QStandardItem(self.appModel['appname'])
        self.treeModel.appendRow(self.root)
        self.fillTree(self.editorModel)

    def addItem(self, parent, label, icon):
        child = QStandardItem(label)
        qicon = QIcon(icon)
        child.setIcon(qicon)
        parent.appendRow(child)
        return child

    def addControllersSubTree(self, parent, appModel):
        subTreeRoot = self.addItem(parent, "Controllers", self.rootIcon)
        kids = appModel['controllers']
        for kid in kids:
            self.addItem(subTreeRoot, kid, self.itemIcon)

    def formatElement(self, parent, me):
        icon = self.itemIcon
        label = me['label'] if 'label' in me else me['style']

        if 'Menu Item' in me['style']:
            return self.addItem(parent, me['label'], icon)
        elif 'Tool Item' in me['style']:
            icon = self.window.assetManager.getIconImage(me['icon'])
            if 'tooltip' in me:
                label += me['tooltip']
            else:
                label = "< Add a Tooltip >"
            return self.addItem(parent, label, icon)
        else:
            return self.addItem(parent, label, self.itemIcon)

    def loadStyleAssets(self, parent, assetManager):
        for styleName in assetManager.styleCache:
            styleRoot = self.addItem(parent, styleName, self.imgFile)

            styleSheet = assetManager.styleCache[styleName]
            styles = styleSheet['Styles']
            for style in styles:
                self.addItem(styleRoot, style, self.imgFile)
            #
            # styleSheet = assetManager.styleCache[styleName]
            # sheetImage = assetManager.imageCache['Style Sheet/' + styleName]
            # style = styleSheet['Styles'][styleName]
            # self.addItem(parent, styleName, sheetImage)
            # # styleImage = self.window.crop(sheetImage, style['srcX'], style['srcY'], style['srcW'], style['srcH'])

    def loadIconAssets(self, parent, assetManager):
        iconNames = [key.replace('Icon/', '') for key in assetManager.imageCache.keys() if key.startswith('Icon/')]
        for iconName in iconNames:
            iconImage = assetManager.getIconImage(iconName)
            self.addItem(parent, iconName, iconImage)

    def addChildren(self, parent, me, kidsListName):
        if kidsListName in me:
            for kid in me[kidsListName]:
                kidItem = self.formatElement(parent, kid)
                if 'contents' in kid:
                    self.addChildren(kidItem, kid, 'contents')

    def loadCodeAssets(self, parent, assetCache):
        for actionName in assetCache:
            self.addItem(parent, actionName, self.pyFile)

    def loadAssetSubTree(self, parent):
        assetManager = self.window.assetManager
        assetRoot = self.addItem(parent, "Assets", self.assetsIcon)

        # Code Assets
        codeRoot = self.addItem(assetRoot, "Code", self.folderOpen)

        actionsRoot = self.addItem(codeRoot, "Actions", self.folderClosed)
        self.loadCodeAssets(actionsRoot, assetManager.actionCodeCache)
        controllersRoot = self.addItem(codeRoot, "Controllers", self.folderOpen)
        self.loadCodeAssets(controllersRoot, assetManager.controllerCodeCache)
        renderersRoot = self.addItem(codeRoot, "Renderers", self.folderOpen)
        self.loadCodeAssets(renderersRoot, assetManager.rendererCodeCache)
        layoutsRoot = self.addItem(codeRoot, "Layouts", self.folderOpen)
        self.loadCodeAssets(layoutsRoot, assetManager.layoutCodeCache)
        partsRoot = self.addItem(codeRoot, "Parts", self.folderOpen)
        self.loadCodeAssets(partsRoot, assetManager.partCodeCache)

        # Image Assets
        imagesRoot = self.addItem(assetRoot, "Image", self.folderOpen)

        stylesRoot = self.addItem(imagesRoot, "Styles", self.imgFile)
        self.loadStyleAssets(stylesRoot, assetManager)

        iconsRoot = self.addItem(imagesRoot, "Icons", self.imgFile)
        self.loadIconAssets(iconsRoot, assetManager)

    def fillTree(self, model):
        # Show Application-specific params
        self.addItem(self.root, model['appTitle'], self.fieldIcon)
        self.addItem(self.root, model['curStyleSheet'], self.fieldIcon)
        self.addControllersSubTree(self.root, model)
        self.loadAssetSubTree(self.root)

        self.addChildren(self.root, model, "contents")

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)

    def on_double_clicked(self, index: QModelIndex, event):
        super().mouseDoubleClickEvent(event)

def createPart(window, me):
    qtWidget = window.getMEData(me, 'qtWidget')
    if qtWidget is not None:
        return

    print('create Part: ', me['partType'])

    # Create a tree view
    widget = ModelExplorer(window)
    font = QFont('Arial', 14)
    widget.setFont(font)
    window.setMEData(me, 'qtWidget', widget)
    if 'partName' in me:
        window.registerPart(me, me['partName'])

    widget.show()

def setFocus(window, me):
    print('Set Focus:', me['label'])
