import os

from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem, QIcon, QPixmap, QPainter
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QTextEdit, QWidget


class FakeView(QWidget):
    def __init__(self, window, imagePath):
        super().__init__(window)

        self.fakeImage = QPixmap(imagePath)
        self.window = window

    def paintEvent(self, event):
        rect = event.rect()
        croppedImage = self.window.crop(self.fakeImage, rect.x(), rect.y(), rect.width(), rect.height() )
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), croppedImage)

def createPart(window, me):
    qtWidget = window.getMEData(me, 'qtWidget')
    if qtWidget is not None:
        return

    print('create Part: ', me['partType'])

    # Create a tree view
    imagePath = me['imagePath']
    widget = FakeView(window, imagePath)
    window.setMEData(me, 'qtWidget', widget)
    if 'partName' in me:
        window.registerPart(me, me['partName'])

    widget.show()

def setFocus(window, me):
    print('Set Focus:', me['label'])
