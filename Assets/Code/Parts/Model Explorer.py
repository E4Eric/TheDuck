import os

from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QTextEdit


class ModelExplorer(QTreeView):
    def __init__(self, window):
        super().__init__(window)

        self.window = window
        self.appModel = window.appModel

        self.setAnimated(True)

        # create the model
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Title'])
        self.setModel(self.model)

        # Tree Icons
        self.rootIcon = window.assetManager.getIconImage("Python Folder")
        self.fieldIcon = window.assetManager.getIconImage("Markdown File")
        self.pyFile = window.assetManager.getIconImage("Python File")
        self.imgFile =  window.assetManager.getIconImage("Image File")
        self.itemIcon = window.assetManager.getIconImage('Data File')
        self.assetsIcon = window.assetManager.getIconImage("Assets")
        self.folderClosed = window.assetManager.getIconImage("Folder (empty)")
        self.folderOpen = window.assetManager.getIconImage("Folder (open)")

        # add root item to the model
        self.root = root_item = QStandardItem(self.appModel['appname'])
        self.model.appendRow(root_item)
        self.fillTree(self.appModel)

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
        codeRoot = self.addItem(assetRoot, "Code", self.folderOpen)
        actionsRoot = self.addItem(codeRoot, "Actions", self.folderClosed)
        self.loadCodeAssets(actionsRoot, assetManager.actionCodeCache)
        controllersRoot = self.addItem(codeRoot, "Controllers", self.folderOpen)
        self.loadCodeAssets(controllersRoot, assetManager.controllerCodeCache)
        controllersRoot = self.addItem(codeRoot, "Renderers", self.folderOpen)
        self.loadCodeAssets(controllersRoot, assetManager.rendererCodeCache)
        controllersRoot = self.addItem(codeRoot, "Layouts", self.folderOpen)
        self.loadCodeAssets(controllersRoot, assetManager.layoutCodeCache)
        controllersRoot = self.addItem(codeRoot, "Parts", self.folderOpen)
        self.loadCodeAssets(controllersRoot, assetManager.partCodeCache)

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
